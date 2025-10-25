"""
Pytest configuration and fixtures for all tests.
"""
import json
import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_minimal_index():
    """
    Create a minimal index file for tests that need it.
    This runs once per test session before any tests execute.
    """
    # Create .cicada directory if it doesn't exist
    os.makedirs('.cicada', exist_ok=True)

    # Create minimal index
    minimal_index = {
        'modules': {},
        'metadata': {
            'total_modules': 0,
            'repo_path': '.'
        }
    }

    index_path = '.cicada/index.json'
    with open(index_path, 'w') as f:
        json.dump(minimal_index, f)

    yield

    # Cleanup happens after all tests complete
    # Note: Individual tests may create their own index files,
    # but we don't clean up the main one as it's needed by multiple tests
