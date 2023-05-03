
from . import load_tools
main_tool_name, tool_data = load_tools("screnshorts")

from fastapi.responses import FileResponse
from app.api.base.libraries.storage import save_in_database, __random_name, create_user_sub_folders
import os
from .selenium_driver import setup_selenium_driver


async def capture_site_view(url, current_user, db):
    dir = await create_user_sub_folders(current_user.id, tool_data['system_folder_name'])
    filename = await __random_name()
    
    real_name = f"{filename}{tool_data['output_file_format']}"
    filePath = os.path.join(dir[0], real_name)
    
    driver, wait = await setup_selenium_driver(url)
    driver.set_window_size(width=1920, height=1080)
    
    driver.save_screenshot(filePath) 
    driver.quit()
    
    # Get the size of the screenshot file in bytes
    file_size = os.path.getsize(filePath)
    
    await save_in_database(
        filename, 
        file_size, 
        db, 
        current_user, 
        tool_data['mime_type'], 
        real_name, 
        tool_name=main_tool_name, 
        file_path=filePath, 
        file_description=f"Screnshort of {url}"
    )
    
    
    return FileResponse(filePath, media_type=tool_data['mime_type'])
