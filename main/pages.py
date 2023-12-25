import flet as ft

from main.setting import app_info_text
from main.func import File_is_img, rembgimg
from main.config import NO_IMAGE_PATH
from main.db import db, Settings

def app_navigate(app: ft.Page) -> object:
    def navigate(e):
        index = app.navigation_bar.selected_index
        app.clean()
        if index == 0: 
            page_main(app)
        elif index == 1: 
            page_setting(app) 
 
    if app.navigation_bar == None:
        app.navigation_bar = ft.NavigationBar(
            destinations = [
                ft.NavigationDestination(icon = ft.icons.IMAGE_ROUNDED, label = 'Главная', selected_icon = ft.icons.IMAGE_OUTLINED),
                ft.NavigationDestination(icon = ft.icons.SETTINGS_APPLICATIONS, label = 'Настройки', selected_icon = ft.icons.SETTINGS_APPLICATIONS_OUTLINED), 
            ], on_change = navigate
        )
    
    return app.navigation_bar

def page_main(app: ft.Page) -> object:
    page_title = "Remove BG"
    app.title = page_title

    def app_isTheme(e):
        app.theme_mode = "light" if app.theme_mode == "dark" else "dark"
        theme_btn.icon = ft.icons.SUNNY if app.theme_mode == "dark" else ft.icons.SUNNY_SNOWING
        btn_downloud.color = ft.colors.GREY_100 if app.theme_mode == "dark" else ft.colors.ON_PRIMARY_CONTAINER
        if selected_files.color != ft.colors.RED:
            selected_files.color = ft.colors.GREY_100 if app.theme_mode == "dark" else ft.colors.ON_PRIMARY_CONTAINER
        app.update()
    
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
           ", ".join(map(lambda f: f.path, e.files)) if e.files else "Файл не выбран!"
        )
   
        selected_icon.name = ft.icons.DRIVE_FILE_MOVE_ROUNDED

        if File_is_img(selected_files.value) and selected_files.value != "Файл не выбран!":
            selected_files.color = ft.colors.GREY_100 if app.theme_mode == "dark" else ft.colors.ON_PRIMARY_CONTAINER
            btn_start.disabled = False
            image_load[0].src = selected_files.value 
            print(image_load[0].src)
            image_load[0].update()
        else: 
            selected_files.color = ft.colors.RED 
            btn_start.disabled = True
            image_load[0].src = NO_IMAGE_PATH
            print(image_load[0].src)
            image_load[0].update()

        selected_icon.update()
        btn_start.update()
        selected_files.update()
    
    def open_dlg(e):
        app.dialog = dlg
        dlg.open = True
        app.update()

    def btn_start_func(e):
        btn_downloud.disabled, btn_start.disabled = True, True
        btn_start.icon = ft.icons.DOWNLOADING_ROUNDED
        btn_downloud.value = "Идёт обработка картинки..."
       
        app.update()

        rembgimg(input_path = selected_files.value) 
            
        open_dlg(e)

        btn_downloud.disabled, btn_start.disabled = False, False
        btn_start.icon = ft.icons.NOT_STARTED
        btn_downloud.value = "Загрузить image..."

        app.update()
    

    theme_btn = ft.IconButton(icon = ft.icons.SUNNY, on_click = app_isTheme)
    image_load = ft.Image(
        src = NO_IMAGE_PATH,
        width = 200,
        height = 200,
    ),

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_icon = ft.Icon()
    selected_files = ft.Text(width=350)

    btn_downloud = ft.ElevatedButton("Загрузить image...", icon=ft.icons.FILE_DOWNLOAD_ROUNDED, on_click=lambda _: pick_files_dialog.pick_files(), color = ft.colors.GREY_100 if app.theme_mode == "dark" else ft.colors.GREY)  
    btn_start = ft.IconButton(icon = ft.icons.NOT_STARTED ,disabled = True, on_click = btn_start_func)

    dlg = ft.AlertDialog(
        title=ft.Text("Всё усепшно прошло !")
    )

    app_navigate(app)

    return app.add(
        ft.Column(
            [
                ft.Row(
                    [   
                        ft.Text(value = page_title),
                        theme_btn
                    ], alignment = ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        pick_files_dialog,
                        
                        btn_downloud,
                        image_load[0]
                        
                    ], alignment = ft.MainAxisAlignment.CENTER,
                ),

                ft.Row(
                    [
                       selected_icon, selected_files
                    ], alignment = ft.MainAxisAlignment.CENTER,
                ),

                ft.Row(
                    [
                        btn_start
                    ], alignment = ft.MainAxisAlignment.CENTER,
                ),
            ], alignment = ft.MainAxisAlignment.CENTER
        ),
    )


def page_setting(app: ft.Page):
    page_title = "Настройки"
    app.title = page_title

    def app_isTheme(e):
        app.theme_mode = "light" if app.theme_mode == "dark" else "dark"
        theme_btn.icon = ft.icons.SUNNY if app.theme_mode == "dark" else ft.icons.SUNNY_SNOWING
        help_btn.color = ft.colors.GREY_100 if app.theme_mode == "dark" else ft.colors.ON_PRIMARY_CONTAINER
        app.update()
    

    def open_dlg(e):
        app.dialog = dlg
        dlg.open = True
        app.update()


    def path_save_img_func(e: ft.FilePickerResultEvent):
        save_file.value = e.path if e.path else "Вы не выюрали деректорию!"
        new = e.path if e.path else "Вы не выюрали деректорию!"
        edit = db.edit_object(old = "path_save_img", new = new) 
        app.update()

    theme_btn = ft.IconButton(icon = ft.icons.SUNNY, on_click = app_isTheme)
    pick_files_dialog_save_img = ft.FilePicker(on_result=path_save_img_func)
    save_file = ft.TextField(label = "Места сохранения картинки", width = 300, value = db.find_object(find = "path_save_img").path_img_save)
    place_save_img = ft.IconButton(icon=ft.icons.DOWNLOADING_ROUNDED, on_click=lambda _: pick_files_dialog_save_img.get_directory_path())  
    help_btn = ft.ElevatedButton("Помощь", on_click=open_dlg, color = ft.colors.GREY_100 if app.theme_mode == "dark" else ft.colors.ON_PRIMARY_CONTAINER)

    dlg = ft.AlertDialog(
        title=ft.Text(app_info_text)
    )

    return app.add(
        ft.Row(
            [   
                ft.Text(value = page_title),
                theme_btn
            ], alignment = ft.MainAxisAlignment.CENTER
        ),
       

        ft.Row(
            [
                save_file, place_save_img, pick_files_dialog_save_img
            ], alignment = ft.MainAxisAlignment.CENTER,
        ),

        ft.Row(
            [
                dlg, help_btn,
            ], alignment = ft.MainAxisAlignment.CENTER
        ),
    )
   



