from pathlib import Path

import customtkinter as ctk
from PIL import Image


def get_btn_image():
    # Получаем путь к директории скрипта
    script_dir = Path(__file__).parent.parent.parent

    # Формируем путь к файлу изображения
    path = script_dir / "images"

    return ctk.CTkImage(Image.open(path / "cross.png"), size=(20, 20))
