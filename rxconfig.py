"""Reflex configuration."""
import reflex as rx

config = rx.Config(
    app_name="app",
    # Enable Tailwind CSS
    tailwind={},
    # Add Jazz as frontend dependency (optional - only if using Jazz in frontend)
    # Note: These packages are not actively used in this template yet
    # Remove these if you're not implementing Jazz integration
    frontend_packages=[
        # "jazz-tools@latest",
        # "jazz-react@latest",
    ],
    # Database (if needed in future)
    # db_url="sqlite:///reflex.db",
)
