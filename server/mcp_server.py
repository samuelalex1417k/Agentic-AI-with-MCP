from mcp.server.fastmcp import FastMCP

from tools.filesystem import (
    list_directory,
    read_file,
)

from tools.search import (
    search_files,
)

from tools.project import (
    get_project_files,
    find_project_config,
    analyze_file,
)
mcp = FastMCP(
    "AI Project Analyzer"
)


# -----------------------
# Filesystem Tools
# -----------------------

mcp.tool()(list_directory)

mcp.tool()(read_file)

mcp.tool()(search_files)

mcp.tool()(get_project_files)

mcp.tool()(find_project_config)

mcp.tool()(analyze_file)


if __name__ == "__main__":
    mcp.run()