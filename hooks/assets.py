"""Publish slide & diagram assets from top-level assets/ into site/assets/ without duplicating files."""

from pathlib import Path
from mkdocs.structure.files import File


def on_files(files, config):
    assets = Path(config.config_file_path).parent / "assets"
    for ext in ("*.svg", "*.png"):
        for image in sorted(assets.glob(ext)):
            files.append(
                File(
                    f"assets/{image.name}",
                    str(assets.parent),
                    config.site_dir,
                    config.use_directory_urls,
                )
            )
    return files
