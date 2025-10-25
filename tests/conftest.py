"""
Pytest configuration and fixtures for all tests.
"""
import json
import os
import yaml
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Create minimal index and config files for tests that need them.
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

    # Create config.yaml file
    config = {
        'repository': {'path': '.'},
        'storage': {'index_path': '.cicada/index.json'}
    }

    config_path = 'config.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(config, f)

    yield

    # Cleanup happens after all tests complete
    # Note: Individual tests may create their own index/config files,
    # but we don't clean up the main ones as they're needed by multiple tests
