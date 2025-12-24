"""PHP repository indexer using SCIP protocol.

This indexer uses scip-php to generate type-aware semantic indexes
of PHP codebases.
"""

from pathlib import Path

from cicada.languages.scip.indexer import GenericSCIPIndexer


class PhpSCIPIndexer(GenericSCIPIndexer):
    """Index PHP repositories using scip-php."""

    def __init__(self, verbose: bool = False):
        """Initialize the PHP SCIP indexer."""
        super().__init__(verbose)
        self.excluded_dirs = {
            "vendor",
            ".git",
            "node_modules",
            "cache",
            "storage",
        }

    def get_language_name(self) -> str:
        """Return language identifier."""
        return "php"

    def get_file_extensions(self) -> list[str]:
        """Return PHP file extensions."""
        return [".php"]

    def get_excluded_dirs(self) -> list[str]:
        """Return directories to exclude from indexing."""
        return list(self.excluded_dirs)

    def _run_scip_indexer(self, repo_path: Path) -> Path:
        """Run scip-php indexer."""
        import shutil

        scip_file = repo_path / "index.scip"

        # Use global scip-php (local vendor/bin version has dependency issues)
        if shutil.which("scip-php"):
            cmd = ["scip-php", "index", "--output", "index.scip"]
        else:
            raise RuntimeError(
                "scip-php not found. Install via: git clone https://github.com/davidrjenni/scip-php && cd scip-php && composer install"
            )

        return self._run_scip_command(
            repo_path=repo_path, command=cmd, output_path=scip_file, timeout=600
        )
