"""Tests for the environment check tool."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from unittest.mock import patch

from voicereach.tools.env_check import (
    CheckResult,
    _format_results,
    check_api_keys,
    check_disk_space,
    check_fastapi_uvicorn,
    check_numpy_scipy,
    check_pydantic,
    check_python_version,
    run_all_checks,
)


class TestCheckResult:
    """Verify the CheckResult dataclass."""

    def test_minimal_fields(self):
        r = CheckResult(name="test", status="ok")
        assert r.name == "test"
        assert r.status == "ok"
        assert r.version is None
        assert r.detail is None

    def test_all_fields(self):
        r = CheckResult(name="pkg", status="warn", version="1.2.3", detail="heads up")
        assert r.version == "1.2.3"
        assert r.detail == "heads up"

    def test_to_dict(self):
        r = CheckResult(name="foo", status="fail", version="0.1", detail="broken")
        d = asdict(r)
        assert d == {
            "name": "foo",
            "status": "fail",
            "version": "0.1",
            "detail": "broken",
        }

    def test_json_serialization(self):
        r = CheckResult(name="bar", status="ok", version="2.0")
        raw = json.dumps(asdict(r))
        loaded = json.loads(raw)
        assert loaded["name"] == "bar"
        assert loaded["status"] == "ok"
        assert loaded["version"] == "2.0"
        assert loaded["detail"] is None


class TestPythonVersion:
    """The test runner itself must be >= 3.11, so this should always pass."""

    def test_returns_ok(self):
        result = check_python_version()
        assert result.status == "ok"
        assert result.name == "Python"
        assert result.version is not None


class TestInstalledPackages:
    """These packages are in the dev/core deps so they must be importable."""

    def test_pydantic_ok(self):
        result = check_pydantic()
        assert result.status == "ok"
        assert result.version is not None
        assert result.version.startswith("2")

    def test_fastapi_uvicorn_ok(self):
        result = check_fastapi_uvicorn()
        assert result.status == "ok"
        assert "fastapi=" in (result.version or "")
        assert "uvicorn=" in (result.version or "")

    def test_numpy_scipy_ok(self):
        result = check_numpy_scipy()
        assert result.status == "ok"
        assert "numpy=" in (result.version or "")


class TestApiKeys:
    """Test API key checks without revealing any real values."""

    def test_all_keys_set(self):
        env = {
            "GEMINI_API_KEY": "fake-gemini",
            "ANTHROPIC_API_KEY": "fake-anthropic",
            "OPENAI_API_KEY": "fake-openai",
        }
        with patch.dict(os.environ, env, clear=False):
            result = check_api_keys()
        assert result.status == "ok"
        # Verify we never leak the actual value
        assert "fake-gemini" not in (result.detail or "")
        assert "fake-anthropic" not in (result.detail or "")
        assert "fake-openai" not in (result.detail or "")

    def test_missing_required_key(self):
        env = {
            "GEMINI_API_KEY": "",
            "ANTHROPIC_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        }
        with patch.dict(os.environ, env, clear=False):
            result = check_api_keys()
        assert result.status == "warn"
        assert "GEMINI_API_KEY" in (result.detail or "")

    def test_only_optional_missing(self):
        env = {
            "GEMINI_API_KEY": "g",
            "ANTHROPIC_API_KEY": "a",
            "OPENAI_API_KEY": "",
        }
        with patch.dict(os.environ, env, clear=False):
            result = check_api_keys()
        # OPENAI is optional, so should still be "ok"
        assert result.status == "ok"
        assert "optional" in (result.detail or "")


class TestDiskSpace:
    def test_returns_result(self):
        result = check_disk_space()
        assert result.name == "Disk space"
        assert result.status in ("ok", "warn")
        assert result.detail is not None
        assert "tmpdir" in result.detail
        assert "cwd" in result.detail


class TestRunAllChecks:
    """Integration-style test for the top-level runner."""

    def test_returns_list_of_results(self):
        results = run_all_checks(skip_camera=True, skip_server=True)
        assert isinstance(results, list)
        assert all(isinstance(r, CheckResult) for r in results)

    def test_has_expected_check_count(self):
        results = run_all_checks(skip_camera=True, skip_server=True)
        # 14 checks total
        assert len(results) == 14

    def test_skipped_checks_marked(self):
        results = run_all_checks(skip_camera=True, skip_server=True)
        by_name = {r.name: r for r in results}
        assert by_name["Camera"].status == "skip"
        assert by_name["vllm-mlx server"].status == "skip"

    def test_no_exceptions_propagated(self):
        """Even if individual checks fail, run_all_checks must not raise."""
        # This implicitly tests the try/except wrapping; if any check
        # throws an unhandled exception, this test will fail.
        results = run_all_checks(skip_camera=True, skip_server=True)
        statuses = {r.status for r in results}
        # All statuses must be valid
        assert statuses <= {"ok", "warn", "fail", "skip"}


class TestFormatResults:
    """Test the pretty-print formatter produces sensible output."""

    def test_contains_header(self):
        results = [CheckResult("Test", "ok")]
        output = _format_results(results)
        assert "VoiceReach Environment Check" in output

    def test_contains_all_statuses(self):
        results = [
            CheckResult("A", "ok"),
            CheckResult("B", "warn", detail="be careful"),
            CheckResult("C", "fail", detail="broken"),
            CheckResult("D", "skip"),
        ]
        output = _format_results(results)
        assert "OK" in output
        assert "WARN" in output
        assert "FAIL" in output
        assert "SKIP" in output
        assert "1 passed" in output
        assert "1 warnings" in output
        assert "1 failed" in output
        assert "1 skipped" in output

    def test_version_shown(self):
        results = [CheckResult("Pkg", "ok", version="3.2.1")]
        output = _format_results(results)
        assert "3.2.1" in output
