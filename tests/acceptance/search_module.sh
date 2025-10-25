#!/bin/bash
# Usage: ./test/acceptance/search_module.sh ModuleName

MODULE="${1:-AB.Generators}"

python -c "import asyncio; from cicada.mcp_server import CicadaServer; print(asyncio.run(CicadaServer()._search_module('$MODULE', 'markdown'))[0].text)"
