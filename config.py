"""Simple configuration for Jazz-only mode."""
import os
import logging
from dotenv import load_dotenv

load_dotenv()


_config_instance = None


class Config:
    """Application configuration."""

    # Jazz Sync Configuration
    JAZZ_SYNC_SERVER: str = os.getenv("JAZZ_SYNC_SERVER", "wss://cloud.jazz.tools")
    JAZZ_AUTH_PROVIDER: str = os.getenv("JAZZ_AUTH_PROVIDER", "anonymous")

    @property
    def JAZZ_ENABLE_P2P(self) -> bool:
        return os.getenv("JAZZ_ENABLE_P2P", "true").lower() == "true"

    # Application Settings
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    def setup_logging(self) -> None:
        """Configure logging."""
        logging.basicConfig(
            level=getattr(logging, self.LOG_LEVEL),
            format='[JAZZ-ONLY] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        logger.info("🎺 Jazz-Only Mode")
        logger.info(f" Sync Server: {self.JAZZ_SYNC_SERVER or 'Local-only'}")
        logger.info(f" P2P Enabled: {'✅' if self.JAZZ_ENABLE_P2P else '❌'}")


def get_config() -> Config:
    """Get or create global config instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
        _config_instance.setup_logging()
    return _config_instance


# Create global config
config = get_config()
