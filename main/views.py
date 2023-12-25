import flet as ft 

from main.setting import app_setting
from main.pages import page_main, page_setting

def App(app: ft.Page) -> bool:
    app_setting(app)
    page_views_main(app)
    return True


def page_views_main(app: ft.Page) -> bool:
    page_main(app)
    return True







