"""
Tests for local (in-repo) storage feature in cicada/utils/storage.py

This tests the ability to store indexes in .cicada/ directory inside the repository
instead of the global ~/.cicada/projects/<hash>/ directory.
"""

from pathlib import Path

import pytest

from cicada.utils.storage import (
    create_storage_dir,
    get_global_storage_dir,
    get_local_storage_dir,
    get_storage_dir,
    has_local_storage,
)


class TestLocalStorageDir:
    """Tests for get_local_storage_dir function"""

    def test_returns_cicada_dir_inside_repo(self, tmp_path):
        """Should return .cicada directory path inside the repository"""
        repo = tmp_path / "my_repo"
        repo.mkdir()

        local_dir = get_local_storage_dir(repo)

        assert local_dir == repo / ".cicada"

    def test_path_is_resolved(self, tmp_path):
        """Should resolve relative paths"""
        repo = tmp_path / "my_repo"
        repo.mkdir()

        # Use relative-style path
        local_dir = get_local_storage_dir(str(repo))

        assert local_dir.is_absolute()
        assert local_dir == repo / ".cicada"


class TestGlobalStorageDir:
    """Tests for get_global_storage_dir function"""

    def test_returns_home_cicada_projects_path(self, tmp_path, mock_home_dir):
        """Should return path under ~/.cicada/projects/<hash>/"""
        repo = tmp_path / "my_repo"
        repo.mkdir()

        global_dir = get_global_storage_dir(repo)

        # Should be under the mocked home directory
        # Structure: mock_home/.cicada/projects/<hash>
        assert global_dir.parent == mock_home_dir / ".cicada" / "projects"
        assert global_dir.name  # Should have a hash name


class TestHasLocalStorage:
    """Tests for has_local_storage function"""

    def test_returns_false_when_no_cicada_dir(self, tmp_path):
        """Should return False when .cicada directory doesn't exist"""
        repo = tmp_path / "my_repo"
        repo.mkdir()

        assert has_local_storage(repo) is False

    def test_returns_false_when_cicada_dir_empty(self, tmp_path):
        """Should return False when .cicada exists but has no index.json"""
        repo = tmp_path / "my_repo"
        repo.mkdir()
        (repo / ".cicada").mkdir()

        assert has_local_storage(repo) is False

    def test_returns_true_when_index_exists(self, tmp_path):
        """Should return True when .cicada/index.json exists"""
        repo = tmp_path / "my_repo"
        repo.mkdir()
        cicada_dir = repo / ".cicada"
        cicada_dir.mkdir()
        (cicada_dir / "index.json").write_text('{"modules": {}}')

        assert has_local_storage(repo) is True


class TestGetStorageDir:
    """Tests for get_storage_dir function with local storage support"""

    def test_returns_global_by_default(self, tmp_path, mock_home_dir):
        """Should return global storage when no local storage exists"""
        repo = tmp_path / "my_repo"
        repo.mkdir()

        storage_dir = get_storage_dir(repo)

        # Should be under ~/.cicada/projects/
        assert ".cicada" in str(storage_dir)
        assert "projects" in str(storage_dir)

    def test_auto_detects_local_storage(self, tmp_path):
        """Should auto-detect and use local storage when it exists"""
        repo = tmp_path / "my_repo"
        repo.mkdir()
        cicada_dir = repo / ".cicada"
        cicada_dir.mkdir()
        (cicada_dir / "index.json").write_text('{"modules": {}}')

        storage_dir = get_storage_dir(repo)

        assert storage_dir == cicada_dir

    def test_prefer_local_creates_local_path(self, tmp_path):
        """Should return local path when prefer_local=True even if no index exists"""
        repo = tmp_path / "my_repo"
        repo.mkdir()

        storage_dir = get_storage_dir(repo, prefer_local=True)

        assert storage_dir == repo / ".cicada"

    def test_local_storage_takes_precedence_over_global(self, tmp_path, mock_home_dir):
        """When both exist, local storage should take precedence"""
        repo = tmp_path / "my_repo"
        repo.mkdir()

        # Create global storage first
        global_dir = get_global_storage_dir(repo)
        global_dir.mkdir(parents=True)
        (global_dir / "index.json").write_text('{"modules": {}, "source": "global"}')

        # Now create local storage
        local_dir = repo / ".cicada"
        local_dir.mkdir()
        (local_dir / "index.json").write_text('{"modules": {}, "source": "local"}')

        storage_dir = get_storage_dir(repo)

        # Should prefer local
        assert storage_dir == local_dir


class TestCreateStorageDir:
    """Tests for create_storage_dir function with local storage support"""

    def test_creates_global_by_default(self, tmp_path, mock_home_dir):
        """Should create global storage directory by default"""
        repo = tmp_path / "my_repo"
        repo.mkdir()

        storage_dir = create_storage_dir(repo)

        assert storage_dir.exists()
        assert "projects" in str(storage_dir)

    def test_creates_local_when_prefer_local(self, tmp_path):
        """Should create local .cicada directory when prefer_local=True"""
        repo = tmp_path / "my_repo"
        repo.mkdir()

        storage_dir = create_storage_dir(repo, prefer_local=True)

        assert storage_dir.exists()
        assert storage_dir == repo / ".cicada"

    def test_uses_existing_local_storage(self, tmp_path):
        """Should use existing local storage even without prefer_local"""
        repo = tmp_path / "my_repo"
        repo.mkdir()
        cicada_dir = repo / ".cicada"
        cicada_dir.mkdir()
        (cicada_dir / "index.json").write_text('{"modules": {}}')

        storage_dir = create_storage_dir(repo)

        assert storage_dir == cicada_dir


class TestLocalStoragePortability:
    """Tests for portability aspects of local storage"""

    def test_local_storage_path_is_relative_to_repo(self, tmp_path):
        """Local storage path should always be relative to repo root"""
        # Create repo in one location
        repo1 = tmp_path / "location1" / "my_repo"
        repo1.mkdir(parents=True)

        # Create repo in another location with same name
        repo2 = tmp_path / "location2" / "my_repo"
        repo2.mkdir(parents=True)

        # Local storage should be .cicada in each repo
        local1 = get_local_storage_dir(repo1)
        local2 = get_local_storage_dir(repo2)

        # Both should end with .cicada but be different absolute paths
        assert local1.name == ".cicada"
        assert local2.name == ".cicada"
        assert local1 != local2
        assert local1.parent == repo1
        assert local2.parent == repo2

    def test_moving_repo_preserves_local_storage(self, tmp_path):
        """Moving a repo with local storage should preserve the index"""
        import shutil

        # Create repo with local storage
        original_path = tmp_path / "original" / "my_repo"
        original_path.mkdir(parents=True)
        cicada_dir = original_path / ".cicada"
        cicada_dir.mkdir()
        (cicada_dir / "index.json").write_text('{"modules": {"Test": {}}}')

        # "Move" the repo (simulate by copying)
        new_path = tmp_path / "new_location" / "my_repo"
        shutil.copytree(original_path, new_path)

        # Local storage should be detected in new location
        assert has_local_storage(new_path)
        storage_dir = get_storage_dir(new_path)
        assert storage_dir == new_path / ".cicada"

        # Index content should be preserved
        import json

        index = json.loads((storage_dir / "index.json").read_text())
        assert "Test" in index["modules"]
