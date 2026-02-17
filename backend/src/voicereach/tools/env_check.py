"""Development environment verification for VoiceReach.

Checks that all required ML/AI dependencies, hardware, and services
are available and correctly configured on the developer's machine.
"""

from __future__ import annotations

import importlib
import json
import os
import platform
import shutil
import sys
import tempfile
from dataclasses import asdict, dataclass, field


@dataclass
class CheckResult:
    """Result of a single environment check."""

    name: str
    status: str  # "ok", "warn", "fail", "skip"
    version: str | None = None
    detail: str | None = None


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------


def check_python_version() -> CheckResult:
    """Verify Python >= 3.11."""
    vi = sys.version_info
    version_str = f"{vi.major}.{vi.minor}.{vi.micro}"
    if (vi.major, vi.minor) >= (3, 11):
        return CheckResult("Python", "ok", version=version_str)
    return CheckResult(
        "Python",
        "fail",
        version=version_str,
        detail="Python >= 3.11 is required",
    )


def check_mediapipe() -> CheckResult:
    """Import MediaPipe and verify Face Mesh can initialize."""
    try:
        mp = importlib.import_module("mediapipe")
        version = getattr(mp, "__version__", "unknown")
    except Exception as exc:
        return CheckResult("MediaPipe", "fail", detail=str(exc))

    try:
        face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
        )
        face_mesh.close()
        return CheckResult("MediaPipe", "ok", version=version, detail="FaceMesh OK")
    except Exception as exc:
        return CheckResult(
            "MediaPipe", "warn", version=version, detail=f"FaceMesh init failed: {exc}"
        )


def check_onnxruntime() -> CheckResult:
    """Import ONNX Runtime and report available execution providers."""
    try:
        ort = importlib.import_module("onnxruntime")
        version = getattr(ort, "__version__", "unknown")
        providers = ort.get_available_providers()
    except Exception as exc:
        return CheckResult("ONNX Runtime", "fail", detail=str(exc))

    is_mac = platform.system() == "Darwin"
    is_linux = platform.system() == "Linux"

    detail_parts = [f"providers: {', '.join(providers)}"]

    status = "ok"
    if is_mac and "CoreMLExecutionProvider" not in providers:
        detail_parts.append("CoreMLExecutionProvider not available")
        status = "warn"
    elif is_linux and "CUDAExecutionProvider" not in providers:
        detail_parts.append("CUDAExecutionProvider not available (CPU only)")
        status = "warn"

    return CheckResult("ONNX Runtime", status, version=version, detail="; ".join(detail_parts))


def check_opencv() -> CheckResult:
    """Import OpenCV and report version."""
    try:
        cv2 = importlib.import_module("cv2")
        version = getattr(cv2, "__version__", "unknown")
        return CheckResult("OpenCV", "ok", version=version)
    except Exception as exc:
        return CheckResult("OpenCV", "fail", detail=str(exc))


def check_numpy_scipy() -> CheckResult:
    """Import NumPy and SciPy."""
    try:
        np = importlib.import_module("numpy")
        np_version = getattr(np, "__version__", "unknown")
    except Exception as exc:
        return CheckResult("NumPy/SciPy", "fail", detail=f"numpy: {exc}")

    try:
        sp = importlib.import_module("scipy")
        sp_version = getattr(sp, "__version__", "unknown")
    except Exception as exc:
        return CheckResult(
            "NumPy/SciPy",
            "warn",
            version=f"numpy={np_version}",
            detail=f"scipy import failed: {exc}",
        )

    return CheckResult(
        "NumPy/SciPy",
        "ok",
        version=f"numpy={np_version}, scipy={sp_version}",
    )


def check_fastapi_uvicorn() -> CheckResult:
    """Import FastAPI and Uvicorn."""
    versions: list[str] = []
    try:
        fa = importlib.import_module("fastapi")
        versions.append(f"fastapi={getattr(fa, '__version__', '?')}")
    except Exception as exc:
        return CheckResult("FastAPI/Uvicorn", "fail", detail=f"fastapi: {exc}")

    try:
        uv = importlib.import_module("uvicorn")
        versions.append(f"uvicorn={getattr(uv, '__version__', '?')}")
    except Exception as exc:
        return CheckResult(
            "FastAPI/Uvicorn",
            "warn",
            version=versions[0] if versions else None,
            detail=f"uvicorn: {exc}",
        )

    return CheckResult("FastAPI/Uvicorn", "ok", version=", ".join(versions))


def check_audio_libs() -> CheckResult:
    """Import soundfile and librosa."""
    versions: list[str] = []
    try:
        sf = importlib.import_module("soundfile")
        versions.append(f"soundfile={getattr(sf, '__version__', '?')}")
    except Exception as exc:
        return CheckResult("soundfile/librosa", "fail", detail=f"soundfile: {exc}")

    try:
        lr = importlib.import_module("librosa")
        versions.append(f"librosa={getattr(lr, '__version__', '?')}")
    except Exception as exc:
        return CheckResult(
            "soundfile/librosa",
            "warn",
            version=versions[0] if versions else None,
            detail=f"librosa: {exc}",
        )

    return CheckResult("soundfile/librosa", "ok", version=", ".join(versions))


def check_mlx() -> CheckResult:
    """Import MLX (optional, macOS only)."""
    if platform.system() != "Darwin":
        return CheckResult("MLX", "skip", detail="macOS only")

    try:
        mlx = importlib.import_module("mlx.core")
        version_mod = importlib.import_module("mlx")
        version = getattr(version_mod, "__version__", "unknown")
    except Exception:
        return CheckResult("MLX", "warn", detail="Not installed (optional)")

    try:
        device = mlx.default_device()
        device_str = str(device)
    except Exception:
        device_str = "unknown"

    return CheckResult("MLX", "ok", version=version, detail=f"device: {device_str}")


def check_vllm_mlx_server(
    base_url: str = "http://127.0.0.1:8000/v1",
) -> CheckResult:
    """Check if a local vllm-mlx server is running."""
    try:
        httpx = importlib.import_module("httpx")
    except Exception as exc:
        return CheckResult("vllm-mlx server", "fail", detail=f"httpx not available: {exc}")

    try:
        url = f"{base_url.rstrip('/')}/models"
        resp = httpx.get(url, timeout=2.0)
        if resp.status_code == 200:
            data = resp.json()
            models = [m.get("id", "?") for m in data.get("data", [])]
            detail = f"models: {', '.join(models)}" if models else "running (no models listed)"
            return CheckResult("vllm-mlx server", "ok", detail=detail)
        return CheckResult(
            "vllm-mlx server",
            "warn",
            detail=f"HTTP {resp.status_code} at {url}",
        )
    except Exception:
        return CheckResult(
            "vllm-mlx server",
            "warn",
            detail=f"Not reachable at {base_url}",
        )


def check_cosyvoice() -> CheckResult:
    """Try to import CosyVoice (optional)."""
    try:
        importlib.import_module("cosyvoice")
        return CheckResult("CosyVoice", "ok")
    except Exception:
        return CheckResult("CosyVoice", "warn", detail="Not installed (optional)")


def check_pydantic() -> CheckResult:
    """Verify Pydantic v2 is installed."""
    try:
        pd = importlib.import_module("pydantic")
        version = getattr(pd, "__version__", "unknown")
    except Exception as exc:
        return CheckResult("Pydantic", "fail", detail=str(exc))

    if version.startswith("2"):
        return CheckResult("Pydantic", "ok", version=version)
    return CheckResult(
        "Pydantic",
        "fail",
        version=version,
        detail="Pydantic v2 is required",
    )


def check_api_keys() -> CheckResult:
    """Check for API key environment variables (never reveal values)."""
    keys = {
        "GEMINI_API_KEY": False,
        "ANTHROPIC_API_KEY": False,
        "OPENAI_API_KEY": False,  # optional
    }
    optional_keys = {"OPENAI_API_KEY"}

    for key in keys:
        keys[key] = bool(os.environ.get(key))

    set_keys = [k for k, v in keys.items() if v]
    missing_required = [k for k, v in keys.items() if not v and k not in optional_keys]
    missing_optional = [k for k, v in keys.items() if not v and k in optional_keys]

    parts: list[str] = []
    if set_keys:
        parts.append(f"set: {', '.join(set_keys)}")
    if missing_required:
        parts.append(f"missing: {', '.join(missing_required)}")
    if missing_optional:
        parts.append(f"missing (optional): {', '.join(missing_optional)}")

    detail = "; ".join(parts) if parts else None

    if missing_required:
        return CheckResult("API keys", "warn", detail=detail)
    return CheckResult("API keys", "ok", detail=detail)


def check_camera() -> CheckResult:
    """Try to open camera 0 and read one frame."""
    try:
        cv2 = importlib.import_module("cv2")
    except Exception as exc:
        return CheckResult("Camera", "fail", detail=f"OpenCV not available: {exc}")

    cap = None
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return CheckResult("Camera", "warn", detail="Could not open camera 0")
        ret, frame = cap.read()
        if not ret or frame is None:
            return CheckResult("Camera", "warn", detail="Camera opened but read failed")
        h, w = frame.shape[:2]
        return CheckResult("Camera", "ok", detail=f"resolution: {w}x{h}")
    except Exception as exc:
        return CheckResult("Camera", "warn", detail=str(exc))
    finally:
        if cap is not None:
            cap.release()


def check_disk_space() -> CheckResult:
    """Check available disk space in tmp and working directory."""
    threshold_gb = 5.0
    warnings: list[str] = []

    for label, path in [("tmpdir", tempfile.gettempdir()), ("cwd", os.getcwd())]:
        try:
            usage = shutil.disk_usage(path)
            free_gb = usage.free / (1024**3)
            if free_gb < threshold_gb:
                warnings.append(f"{label}: {free_gb:.1f} GB free (< {threshold_gb:.0f} GB)")
            else:
                warnings.append(f"{label}: {free_gb:.1f} GB free")
        except Exception as exc:
            warnings.append(f"{label}: error ({exc})")

    detail = "; ".join(warnings)
    has_warning = any("< " in w or "error" in w for w in warnings)
    return CheckResult(
        "Disk space",
        "warn" if has_warning else "ok",
        detail=detail,
    )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all_checks(
    *,
    skip_camera: bool = False,
    skip_server: bool = False,
) -> list[CheckResult]:
    """Execute all environment checks and return results.

    Parameters
    ----------
    skip_camera:
        If True, skip the camera check (useful in headless / CI).
    skip_server:
        If True, skip the vllm-mlx server reachability check.
    """
    results: list[CheckResult] = []

    checks: list[tuple[str, object]] = [
        ("python", check_python_version),
        ("mediapipe", check_mediapipe),
        ("onnxruntime", check_onnxruntime),
        ("opencv", check_opencv),
        ("numpy_scipy", check_numpy_scipy),
        ("fastapi", check_fastapi_uvicorn),
        ("audio", check_audio_libs),
        ("mlx", check_mlx),
        ("vllm_server", check_vllm_mlx_server),
        ("cosyvoice", check_cosyvoice),
        ("pydantic", check_pydantic),
        ("api_keys", check_api_keys),
        ("camera", check_camera),
        ("disk", check_disk_space),
    ]

    for tag, fn in checks:
        if tag == "camera" and skip_camera:
            results.append(CheckResult("Camera", "skip", detail="Skipped via --skip-camera"))
            continue
        if tag == "vllm_server" and skip_server:
            results.append(
                CheckResult("vllm-mlx server", "skip", detail="Skipped via --skip-server")
            )
            continue

        try:
            results.append(fn())
        except Exception as exc:
            results.append(CheckResult(tag, "fail", detail=f"Unexpected error: {exc}"))

    return results


# ---------------------------------------------------------------------------
# Pretty printer
# ---------------------------------------------------------------------------

_STATUS_SYMBOLS = {
    "ok": ("\033[32m\u2713\033[0m", "OK"),
    "warn": ("\033[33m\u26a0\033[0m", "WARN"),
    "fail": ("\033[31m\u2717\033[0m", "FAIL"),
    "skip": ("\033[90m-\033[0m", "SKIP"),
}


def _format_results(results: list[CheckResult]) -> str:
    """Format check results as a human-readable, color-coded report."""
    lines: list[str] = []
    lines.append("")
    lines.append("\033[1mVoiceReach Environment Check\033[0m")
    lines.append("=" * 40)

    for r in results:
        symbol, label = _STATUS_SYMBOLS.get(r.status, ("?", r.status.upper()))
        version_part = f"  [{r.version}]" if r.version else ""
        detail_part = f"  -- {r.detail}" if r.detail else ""
        lines.append(f"  {symbol} {label:4s}  {r.name}{version_part}{detail_part}")

    lines.append("=" * 40)

    counts = {"ok": 0, "warn": 0, "fail": 0, "skip": 0}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1

    summary_parts = []
    if counts["ok"]:
        summary_parts.append(f"\033[32m{counts['ok']} passed\033[0m")
    if counts["warn"]:
        summary_parts.append(f"\033[33m{counts['warn']} warnings\033[0m")
    if counts["fail"]:
        summary_parts.append(f"\033[31m{counts['fail']} failed\033[0m")
    if counts["skip"]:
        summary_parts.append(f"\033[90m{counts['skip']} skipped\033[0m")

    lines.append("  " + ", ".join(summary_parts))
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point for voicereach-env-check."""
    import argparse

    parser = argparse.ArgumentParser(
        description="VoiceReach development environment checker",
    )
    parser.add_argument(
        "--skip-camera",
        action="store_true",
        help="Skip the camera hardware check",
    )
    parser.add_argument(
        "--skip-server",
        action="store_true",
        help="Skip the vllm-mlx server reachability check",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    args = parser.parse_args()

    results = run_all_checks(
        skip_camera=args.skip_camera,
        skip_server=args.skip_server,
    )

    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2, ensure_ascii=False))
    else:
        print(_format_results(results))

    has_failures = any(r.status == "fail" for r in results)
    raise SystemExit(1 if has_failures else 0)


if __name__ == "__main__":
    main()
