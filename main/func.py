from rembg import remove 
from PIL import Image
import random

from main.db import db

def File_is_img(img_path: str) -> bool:
    type_img = ["png", "jpg", "ico", "svg" ,"PNG" ,"JPEG", "ICO", "SVG", "JPG"] 
  
    for el in type_img:
        if el in img_path: return True

    return False


def rembgimg(input_path: str) -> bool:
    try: 
        path = db.find_object(find = "path_save_img")
        input_user = Image.open(input_path)
        output = remove(input_user)
        output.save(path.path_img_save + "\\" + f"result{random.randint(1, 100)}.png")
        return True
    except:
        return False














