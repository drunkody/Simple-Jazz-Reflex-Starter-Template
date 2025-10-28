"""Tests for configuration."""
import os
import pytest
from config import Config


class TestConfig:
    """Test configuration loading."""

    def test_default_values(self):
        """Test default configuration values."""
        config = Config()
        assert config.JAZZ_SYNC_SERVER == os.getenv("JAZZ_SYNC_SERVER", "wss://cloud.jazz.tools")
        assert config.APP_ENV == os.getenv("APP_ENV", "development")
        assert config.LOG_LEVEL == os.getenv("LOG_LEVEL", "INFO")

    def test_jazz_enable_p2p_parsing(self):
        """Test P2P boolean parsing."""
        # Save original
        original = os.getenv("JAZZ_ENABLE_P2P")

        try:
            os.environ["JAZZ_ENABLE_P2P"] = "true"
            config = Config()
            assert config.JAZZ_ENABLE_P2P is True

            os.environ["JAZZ_ENABLE_P2P"] = "false"
            config = Config()
            assert config.JAZZ_ENABLE_P2P is False

            os.environ["JAZZ_ENABLE_P2P"] = "TRUE"
            config = Config()
            assert config.JAZZ_ENABLE_P2P is True
        finally:
            # Restore
            if original:
                os.environ["JAZZ_ENABLE_P2P"] = original
            elif "JAZZ_ENABLE_P2P" in os.environ:
                del os.environ["JAZZ_ENABLE_P2P"]
