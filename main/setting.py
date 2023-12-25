import flet as ft 
import getpass 

def app_setting(app: ft.Page) -> bool:
    app.window_resizable = False
    app.window_center()
    app.window_width = 500
    app.window_height = 500
    app.window_to_front()
    app.vertical_alignment = ft.MainAxisAlignment.CENTER
    app.theme_mode = "dark"
    app.window_max_width = 500
    app.window_max_height = 500
    
    return True

app_info_text = f"""
    Привет {getpass.getuser() if getpass.getuser() else "Пользователь"}.

    Это Приложение для 
    удаления заднего
    фона у картинок.
    """
