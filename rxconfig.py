"""Reflex configuration."""
import reflex as rx

config = rx.Config(
    app_name="app",
    tailwind={},
    # Add Jazz as frontend dependency
    frontend_packages=[
        "jazz-tools@^0.8.0",
        "jazz-react@^0.8.0",
        "cojson@^0.8.0",
    ],
)
