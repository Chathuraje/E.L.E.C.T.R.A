import json
import os

def load_json(sub_tool_name, path):
    dir_path = os.path.dirname(os.path.dirname(path))
    config_path = os.path.join(dir_path, 'config.json')
    
    with open(config_path) as f:
        config_data = json.load(f)
        
    main_tool = config_data['main_tool']
    data = config_data[sub_tool_name]

    return main_tool, data