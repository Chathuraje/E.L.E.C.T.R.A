from . import load_tools
main_tool_name, tool_data = load_tools("reddit_screnshorts")


import zipfile, os
from ..schemas import ScreenShot, ScreenShotReddit
from fastapi.responses import FileResponse
from selenium.webdriver.support import expected_conditions as EC
from .selenium_driver import setup_selenium_driver
from selenium.webdriver.common.by import By
from app.api.base.libraries.storage import save_in_database, __random_name, create_user_sub_folders
from app.libraries import temp_storage

async def __zip_images(file_paths, name, dir, temp_dir):
    zip_file = zipfile.ZipFile(f"{dir}/{name}", "a")
    for file_path in file_paths:
        if file_path.startswith(temp_dir):
            rel_path = os.path.relpath(file_path, temp_dir)
            zip_file.write(file_path, rel_path)
        
    zip_file.close()
    
    return f"{dir}/{name}"


async def __capture_reddit(driver, wait, method, handle, filePath):
    
    search = wait.until(EC.presence_of_element_located((method, handle)))
            
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});", search)
    driver.execute_script("window.focus();")

    fp = open(filePath, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()

async def capture_reddit_text_based_post(screenshot: ScreenShotReddit, current_user, db):
    driver, wait = await setup_selenium_driver(screenshot.url)
    driver.set_window_size(width=400, height=800)
    
    temp_dir = temp_storage.get_temp_storage(current_user.id)
    
    name = await __random_name()
    
    file_paths = []
    method = By.CLASS_NAME
    handle="Post"
    filePath = os.path.join(temp_dir, f"{name}_title.png")
    await __capture_reddit(driver, wait, method, handle, filePath)
    file_paths.append(filePath)
    
    for comment in screenshot.commentsid:
        method = By.ID
        handle=f"t1_{comment}"
        filePath = os.path.join(temp_dir, f"{name}_{comment}.png")
        await __capture_reddit(driver, wait, method, handle, filePath)
        file_paths.append(filePath)
        
    driver.quit()
    
    file_name = f"{name}{tool_data['output_file_format']}"
    dir = await create_user_sub_folders(current_user.id, tool_data['system_folder_name'])
    
    
    zip_path = await __zip_images(file_paths, file_name, dir[0], temp_dir)
    
    # Get the size of the screenshot file in bytes
    file_size = os.path.getsize(zip_path)
    
    await save_in_database(
        name, 
        file_size, 
        db, 
        current_user, 
        tool_data['mime_type'], 
        file_name,  
        sub_tool_name=tool_data['sub_tool_name'],
        tool_name=main_tool_name, 
        file_path=zip_path, 
        file_description=f"Screnshort of reddit {screenshot.url} and the ids of comments are {screenshot.commentsid}"
    )
    
    return FileResponse(f"{dir[0]}/{file_name}", media_type=tool_data['mime_type'], filename=file_name)