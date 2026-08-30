"""
Unit tests for Project Scaffolding Generator (scripts/bootstrap_project.py).
"""
import tempfile
from pathlib import Path
import pytest
from scripts.bootstrap_project import scaffold_project


def test_scaffold_project_success():
    """Verify scaffolding generator creates new target directory and replaces string identifiers."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        dest_path = Path(tmp_dir) / "demo-ai-service"

        scaffold_project(
            project_name="demo-ai-service",
            description="Test AI Service",
            destination=dest_path,
            force=True
        )

        assert dest_path.exists()
        assert (dest_path / "app" / "main.py").exists()
        assert (dest_path / "README.md").exists()

        # Verify excluded directories were not copied
        assert not (dest_path / ".venv").exists()
        assert not (dest_path / ".git").exists()
        assert not (dest_path / "__pycache__").exists()

        # Verify string replacements
        readme_content = (dest_path / "README.md").read_text(encoding="utf-8")
        assert "demo-ai-service" in readme_content
        assert "agent-mesh" not in readme_content


def test_scaffold_project_force_flag_required():
    """Verify generator raises SystemExit when destination directory exists and is non-empty without force=True."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        dest_path = Path(tmp_dir) / "existing-dir"
        dest_path.mkdir()
        (dest_path / "dummy.txt").write_text("existing content")

        with pytest.raises(SystemExit):
            scaffold_project(
                project_name="demo-service",
                description="Test",
                destination=dest_path,
                force=False
            )
