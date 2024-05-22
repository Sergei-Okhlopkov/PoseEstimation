from pathlib import Path

import customtkinter as ctk
from PIL import Image

from app.ctk_helper import make_frame, make_btn
from enums import AppColor, AppScreen

FONT = "Inter"


class MainDoctorScreen(ctk.CTkFrame):
    def __init__(self, controller, parent, session):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.session = session

        cross = get_btn_image()

        choose_area = make_frame(self, AppColor.SUBMAIN.value, 20, 750, 450)
        choose_area.pack(anchor="center", expand=True)
        choose_area.pack_propagate(False)

        cross_btn = ctk.CTkButton(
            choose_area,
            text=None,
            image=cross,
            width=20,
            fg_color="transparent",
            command=lambda: controller.logout(),
        ).pack(side="right", anchor="n", pady=10, padx=10)

        header_lbl = ctk.CTkLabel(
            choose_area,
            text="Список пациентов",
            font=(FONT, 42, "bold"),
            text_color=AppColor.WHITE.value,
        ).pack(side="top", padx=(70, 0), pady=(20, 0))


def get_btn_image():
    # Получаем путь к директории скрипта
    script_dir = Path(__file__).parent.parent

    # Формируем путь к файлу изображения
    path = script_dir / "images"

    return ctk.CTkImage(Image.open(path / "cross.png"), size=(20, 20))
