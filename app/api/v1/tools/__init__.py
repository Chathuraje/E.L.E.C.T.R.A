import os
import importlib
from fastapi import APIRouter

router = APIRouter(
    prefix="/tools",
)

# Find all tool directories
tool_directories = []
rootdir = 'app/api/v1/tools'
for item in os.listdir(rootdir):
    dir = os.path.join(rootdir, item)
    if item.startswith("__"):
        continue
    if os.path.isdir(dir):
        tool_directories.append(item)

router_dirs = [os.path.join(os.path.dirname(__file__), subfolder, "routers") for subfolder in tool_directories].sort()

# Dynamically import each router module in the subfolders
for router_dir in tool_directories:
    module_name = f".{router_dir}.routers"
    module = importlib.import_module(module_name, package=__package__)
    router_str = module.router
    router.include_router(router_str)


