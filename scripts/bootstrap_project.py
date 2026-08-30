#!/usr/bin/env python3
"""
Carassco Labs - Project Bootstrap Generator
Scaffolds new microservices and AI applications from agent-mesh template.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".coverage",
    "htmlcov",
    "build",
    "dist",
    ".idea",
    ".vscode",
}

EXCLUDE_FILES = {
    ".DS_Store",
    "*.pyc",
    "*.pyo",
}


def sanitize_name(name: str) -> str:
    return name.strip().lower().replace("_", "-")


def scaffold_project(
    project_name: str,
    description: str,
    destination: Path,
    author: str = "Carassco Labs Engineering",
    force: bool = False
) -> None:
    source_root = Path(__file__).resolve().parent.parent
    dest_path = destination.resolve()

    clean_name = sanitize_name(project_name)
    clean_snake = clean_name.replace("-", "_")
    clean_title = clean_name.replace("-", " ").title()

    print(f"🚀 Initializing Carassco Labs Project Generator...")
    print(f"  • Source Template: {source_root}")
    print(f"  • Target Project:  {clean_name}")
    print(f"  • Destination:     {dest_path}")

    if dest_path.exists() and any(dest_path.iterdir()):
        if not force:
            print(f"❌ Error: Destination path '{dest_path}' exists and is not empty. Use --force to overwrite.")
            sys.exit(1)
        else:
            print(f"⚠️ Warning: Overwriting destination path '{dest_path}'")

    dest_path.mkdir(parents=True, exist_ok=True)

    copied_files_count = 0

    for root, dirs, files in os.walk(source_root):
        current_dir = Path(root).resolve()
        
        # Prevent copying destination into itself if destination is inside source directory
        if dest_path in current_dir.parents or current_dir == dest_path:
            continue

        # Filter out excluded directories in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not (dest_path in (current_dir / d).parents or (current_dir / d) == dest_path)]

        rel_path = current_dir.relative_to(source_root)
        target_dir = dest_path / rel_path

        target_dir.mkdir(parents=True, exist_ok=True)

        for file_name in files:
            if file_name in EXCLUDE_FILES or file_name.endswith(".pyc"):
                continue

            src_file = current_dir / file_name
            dst_file = target_dir / file_name

            # Copy file
            shutil.copy2(src_file, dst_file)
            copied_files_count += 1

            # Perform string replacement on text files
            if dst_file.suffix in {".py", ".md", ".json", ".yml", ".yaml", ".sh", ".example"}:
                try:
                    content = dst_file.read_text(encoding="utf-8")
                    updated_content = (
                        content.replace("agent-mesh", clean_name)
                        .replace("agent_mesh", clean_snake)
                        .replace("Agent Mesh", clean_title)
                    )
                    if content != updated_content:
                        dst_file.write_text(updated_content, encoding="utf-8")
                except UnicodeDecodeError:
                    pass  # Skip binary files

    print(f"✅ Successfully copied and configured {copied_files_count} files into {dest_path}")
    print(f"\nNext Steps:")
    print(f"  1. cd {dest_path}")
    print(f"  2. bash scripts/setup.sh")
    print(f"  3. bash scripts/validate.sh")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bootstrap a new Carassco Labs service from agent-mesh."
    )
    parser.add_argument("--project-name", required=True, help="Target project identifier (e.g. claims-service)")
    parser.add_argument("--description", required=True, help="Short project description")
    parser.add_argument("--destination", required=True, help="Destination directory path")
    parser.add_argument("--author", default="Carassco Labs Engineering", help="Author/Team name")
    parser.add_argument("--force", action="store_true", help="Force overwrite destination if directory exists")

    args = parser.parse_args()

    scaffold_project(
        project_name=args.project_name,
        description=args.description,
        destination=Path(args.destination),
        author=args.author,
        force=args.force
    )


if __name__ == "__main__":
    main()
