import tempfile
import os

def get_temp_storage(user_id):
    temp_dir = tempfile.gettempdir()
    
    user_dir = os.path.join(temp_dir, f"electra_{user_id}")
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
        
    return user_dir