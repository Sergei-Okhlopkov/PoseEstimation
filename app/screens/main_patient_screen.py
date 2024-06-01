from pathlib import Path

import customtkinter as ctk
from PIL import Image

from app.ctk_helper import make_frame, make_btn
from enums import AppColor, AppScreen

BTN_SIZE = 300


class MainPatientScreen(ctk.CTkFrame):
    def __init__(self, controller, parent):
        super().__init__(parent, fg_color=AppColor.MAIN.value)

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
        )

        btns_frame = make_frame(choose_area, "transparent")

        exercises_btn = make_btn(
            btns_frame,
            "Упражнения",
            BTN_SIZE,
            BTN_SIZE,
            command=lambda: controller.show_frame(AppScreen.EXERCISES.value),
        )
        statistics_btn = make_btn(
            btns_frame,
            "Статистика",
            BTN_SIZE,
            BTN_SIZE,
            command=lambda: controller.show_frame(AppScreen.STATISTICS_PATIENT.value),
        )

        cross_btn.pack(anchor="ne", pady=10, padx=10)
        btns_frame.place(relx=0.5, rely=0.5, anchor="center")
        exercises_btn.pack(side="left", padx=[0, 60])
        statistics_btn.pack(side="left")


def get_btn_image():
    # Получаем путь к директории скрипта
    script_dir = Path(__file__).parent.parent

    # Формируем путь к файлу изображения
    path = script_dir / "images"

    return ctk.CTkImage(Image.open(path / "cross.png"), size=(20, 20))
