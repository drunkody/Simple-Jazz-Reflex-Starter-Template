"""Reflex configuration."""
import os
from pathlib import Path

import reflex as rx

config = rx.Config(
    app_name="app",
    
    # Enable Tailwind CSS
    tailwind={},
    
    # Use system Bun on NixOS
    bun_path=Path(os.getenv("BUN_PATH", "/usr/bin/bun")),
    
    # Add Jazz as frontend dependency (optional - only if using Jazz in frontend)
    # Note: These packages are not actively used in this template yet
    # Remove these if you're not implementing Jazz integration
    frontend_packages=[
        # "jazz-tools@latest",
        # "jazz-react@latest",
    ],
    
    # Disable the sitemap plugin warning
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    
    # Database (if needed in future)
    # db_url="sqlite:///reflex.db",
)