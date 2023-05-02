import os
from app.libraries.tool_config import load_json


def load_tools(tool_name):
    path = os.path.abspath(__file__)
    main_tool_name, tool_data = load_json(tool_name, path)
    
    return main_tool_name, tool_data
    