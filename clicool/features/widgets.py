"""Terminal widgets for prompts."""

import subprocess
import os
from typing import Optional


class WidgetRenderer:
    """Render terminal widgets."""

    @staticmethod
    def render_git_branch() -> str:
        """Render git branch widget."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                timeout=2,
                cwd=os.getcwd(),
            )
            if result.returncode == 0:
                branch = result.stdout.strip()
                return f" {branch}"
        except Exception:
            pass
        return ""

    @staticmethod
    def render_git_status() -> str:
        """Render git status indicators."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=2,
                cwd=os.getcwd(),
            )
            if result.returncode == 0:
                status = result.stdout.strip()
                if status:
                    indicators = []
                    if "M" in status:
                        indicators.append("*")
                    if "A" in status:
                        indicators.append("+")
                    if "??" in status:
                        indicators.append("?")
                    return "".join(indicators)
        except Exception:
            pass
        return ""

    @staticmethod
    def render_exit_code(exit_code: int) -> str:
        """Render exit code widget."""
        if exit_code != 0:
            return f"✗ {exit_code}"
        return ""

    @staticmethod
    def render_time(format_str: str = "%H:%M:%S") -> str:
        """Render time widget."""
        from datetime import datetime
        return datetime.now().strftime(format_str)

    @staticmethod
    def render_k8s_context() -> str:
        """Render Kubernetes context widget."""
        try:
            result = subprocess.run(
                ["kubectl", "config", "current-context"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            if result.returncode == 0:
                context = result.stdout.strip()
                return f"☸️  {context}"
        except Exception:
            pass
        return ""

    @staticmethod
    def render_docker_status() -> str:
        """Render Docker status widget."""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.ID}}"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            if result.returncode == 0:
                containers = result.stdout.strip().split("\n")
                count = len([c for c in containers if c])
                if count > 0:
                    return f"🐳 {count}"
        except Exception:
            pass
        return ""

    @staticmethod
    def render_aws_profile() -> str:
        """Render AWS profile widget."""
        profile = os.environ.get("AWS_PROFILE") or os.environ.get("AWS_DEFAULT_PROFILE")
        if profile:
            return f"☁️  {profile}"
        return ""

    @staticmethod
    def render_venv() -> str:
        """Render virtualenv widget."""
        venv = os.environ.get("VIRTUAL_ENV")
        if venv:
            import os.path
            return f"🐍 {os.path.basename(venv)}"
        return ""

    @staticmethod
    def render_node_version() -> str:
        """Render Node.js version widget."""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return f"⬢ {version}"
        except Exception:
            pass
        return ""

    @staticmethod
    def render_python_version() -> str:
        """Render Python version widget."""
        import sys
        return f"🐍 {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


__all__ = ["WidgetRenderer"]
