import { useState, useEffect, useCallback } from "react";

export function usePushNotification() {
  const [isSupported] = useState(() => "Notification" in window);
  const [isPermissionGranted, setIsPermissionGranted] = useState(
    () => "Notification" in window && Notification.permission === "granted",
  );

  // Sync permission state if it changes externally
  useEffect(() => {
    if (!isSupported) return;
    setIsPermissionGranted(Notification.permission === "granted");
  }, [isSupported]);

  const requestPermission = useCallback(async (): Promise<boolean> => {
    if (!isSupported) return false;

    try {
      const result = await Notification.requestPermission();
      const granted = result === "granted";
      setIsPermissionGranted(granted);
      return granted;
    } catch {
      return false;
    }
  }, [isSupported]);

  const showNotification = useCallback(
    (title: string, options?: NotificationOptions) => {
      if (!isSupported || !isPermissionGranted) return;

      const isEmergency =
        options?.tag === "emergency" ||
        title.toLowerCase().includes("緊急") ||
        title.toLowerCase().includes("emergency");

      const notificationOptions: NotificationOptions = {
        ...options,
        // Tag-based deduplication: same tag replaces previous notification
        tag: options?.tag ?? `voicereach-${Date.now()}`,
        icon: "/icon-192.png",
        badge: "/icon-192.png",
        requireInteraction: isEmergency,
      };

      try {
        const notification = new Notification(title, notificationOptions);

        // Vibrate for emergencies if the Vibration API is available
        if (isEmergency && "vibrate" in navigator) {
          navigator.vibrate([200, 100, 200, 100, 400]);
        }

        return notification;
      } catch {
        // Notification creation can fail in some contexts (e.g., service worker required)
      }
    },
    [isSupported, isPermissionGranted],
  );

  return {
    isSupported,
    isPermissionGranted,
    requestPermission,
    showNotification,
  };
}
