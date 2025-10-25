#!/usr/bin/env python
"""
Test script for AB project functions.
"""
import asyncio
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent))

from cicada.mcp_server import CicadaServer


@pytest.mark.asyncio
async def test_ab_function():
    """Test searching for a function in the AB project."""
    server = CicadaServer(config_path="config.yaml")

    print("Test 1: Searching for 'validate_struct' (local calls)")
    print("=" * 80)
    result = await server._search_function("validate_struct", "markdown")
    print(result[0].text)

    print("\n" + "=" * 80)
    print("Test 2: Searching for 'create_input_generator/2' (aliased calls)")
    print("=" * 80)
    result = await server._search_function("create_input_generator/2", "markdown")
    print(result[0].text)


if __name__ == "__main__":
    asyncio.run(test_ab_function())
