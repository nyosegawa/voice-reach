import { expect, test, type Page } from "@playwright/test";

async function installBrowserMocks(page: Page): Promise<void> {
  await page.addInitScript(() => {
    type MockSocket = {
      onopen: ((event: Event) => void) | null;
      onmessage: ((event: MessageEvent<string>) => void) | null;
      onclose: ((event: CloseEvent) => void) | null;
      sent: string[];
      readyState: number;
    };

    const wsRegistry: MockSocket[] = [];
    const globalWithMocks = window as Window & {
      __wsMock?: {
        instances: MockSocket[];
        emit: (index: number, message: unknown) => void;
        lastIndex: () => number;
        sent: (index: number) => string[];
      };
    };

    class MockNotification {
      static permission: NotificationPermission = "granted";

      static async requestPermission(): Promise<NotificationPermission> {
        return "granted";
      }

      constructor(_title: string, _options?: NotificationOptions) {}
      close() {}
    }

    class MockWebSocket {
      static CONNECTING = 0;
      static OPEN = 1;
      static CLOSING = 2;
      static CLOSED = 3;

      url: string;
      readyState = MockWebSocket.CONNECTING;
      onopen: ((event: Event) => void) | null = null;
      onmessage: ((event: MessageEvent<string>) => void) | null = null;
      onclose: ((event: CloseEvent) => void) | null = null;
      sent: string[] = [];

      constructor(url: string) {
        this.url = url;
        wsRegistry.push(this);

        queueMicrotask(() => {
          this.readyState = MockWebSocket.OPEN;
          this.onopen?.(new Event("open"));
        });
      }

      send(data: string) {
        this.sent.push(data);
      }

      close() {
        this.readyState = MockWebSocket.CLOSED;
        this.onclose?.(new CloseEvent("close"));
      }
    }

    Object.defineProperty(window, "Notification", {
      configurable: true,
      writable: true,
      value: MockNotification,
    });

    Object.defineProperty(window, "WebSocket", {
      configurable: true,
      writable: true,
      value: MockWebSocket,
    });

    if (!("vibrate" in navigator)) {
      Object.defineProperty(navigator, "vibrate", {
        configurable: true,
        value: () => true,
      });
    }

    globalWithMocks.__wsMock = {
      instances: wsRegistry,
      emit: (index, message) => {
        const socket = wsRegistry[index];
        socket?.onmessage?.(
          new MessageEvent("message", {
            data: JSON.stringify(message),
          }),
        );
      },
      lastIndex: () => wsRegistry.length - 1,
      sent: (index) => wsRegistry[index]?.sent ?? [],
    };
  });
}

async function emitWsMessage(page: Page, message: unknown): Promise<void> {
  await page.evaluate((payload) => {
    const globalWithMocks = window as Window & {
      __wsMock: {
        emit: (index: number, message: unknown) => void;
        lastIndex: () => number;
      };
    };
    const lastIndex = globalWithMocks.__wsMock.lastIndex();
    globalWithMocks.__wsMock.emit(lastIndex, payload);
  }, message);
}

test.beforeEach(async ({ page }) => {
  await installBrowserMocks(page);
  await page.goto("/");
});

test("dashboard and log tabs render with baseline state", async ({ page }) => {
  await expect(page.getByRole("heading", { name: "VoiceReach" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "患者ステータス" })).toBeVisible();
  await expect(page.getByText("接続中")).toBeVisible();

  await page.getByRole("button", { name: "発話ログ" }).click();
  await expect(page.getByRole("heading", { name: "発話ログ" })).toBeVisible();
  await expect(page.getByText("まだ発話がありません")).toBeVisible();
});

test("patient status updates are reflected in dashboard cards", async ({ page }) => {
  await emitWsMessage(page, {
    type: "patient_status_update",
    payload: {
      is_online: true,
      last_activity: "2026-02-25T09:30:00.000Z",
      utterances_today: 12,
      avg_selection_time_ms: 680,
      current_emotion: "安定",
      active_input: "視線",
    },
  });

  await expect(page.getByText("患者: オンライン")).toBeVisible();
  await expect(page.getByText("12")).toBeVisible();
  await expect(page.getByText("安定")).toBeVisible();
  await expect(page.getByText("視線")).toBeVisible();
});

test("speech log entries appear with stage badge and unspoken marker", async ({ page }) => {
  await emitWsMessage(page, {
    type: "speech_log_entry",
    payload: {
      text: "お水をください",
      timestamp: "2026-02-25T09:30:00.000Z",
      generation_stage: 2,
      was_spoken: false,
      emotion_valence: -0.2,
    },
  });

  await page.getByRole("button", { name: "発話ログ" }).click();
  await expect(page.getByText("お水をください")).toBeVisible();
  await expect(page.getByText("標準")).toBeVisible();
  await expect(page.getByText("(未発声)")).toBeVisible();
});

test("emergency flow can be acknowledged and dismissed", async ({ page }) => {
  await emitWsMessage(page, {
    type: "notification",
    payload: {
      level: "emergency",
      title: "呼吸が苦しい",
      body: "患者から緊急通知",
      timestamp: "2026-02-25T09:30:00.000Z",
      requires_ack: true,
    },
  });

  await expect(page.getByRole("heading", { name: "緊急通報" })).toBeVisible();
  await expect(page.getByText("呼吸が苦しい")).toBeVisible();

  await page.getByRole("button", { name: "確認しました" }).click();
  await expect.poll(async () => {
    const sentPayload = await page.evaluate(() => {
      const globalWithMocks = window as Window & {
        __wsMock: {
          sent: (index: number) => string[];
          lastIndex: () => number;
        };
      };
      return globalWithMocks.__wsMock.sent(globalWithMocks.__wsMock.lastIndex());
    });
    return sentPayload.some((message) =>
      message.includes('"type":"acknowledge_emergency"'),
    );
  }).toBeTruthy();

  await emitWsMessage(page, { type: "emergency_ack" });
  await expect(page.getByText("緊急対応完了")).toBeVisible();

  await page.getByRole("button", { name: "ダッシュボードに戻る" }).click();
  await expect(page.getByRole("heading", { name: "患者ステータス" })).toBeVisible();
});
