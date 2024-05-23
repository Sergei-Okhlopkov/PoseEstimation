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

        choose_area = make_frame(self, AppColor.SUBMAIN.value, 20, 750, 560)
        choose_area.pack(anchor="center", expand=True)
        choose_area.pack_propagate(False)

        # cross_btn = ctk.CTkButton(
        #     choose_area,
        #     text=None,
        #     image=cross,
        #     width=20,
        #     fg_color="transparent",
        #     command=lambda: controller.logout(),
        # ).pack(side="right", anchor="n", pady=10, padx=10)

        cross_btn = ctk.CTkButton(
            choose_area,
            text=None,
            image=cross,
            width=20,
            fg_color="transparent",
            command=lambda: controller.logout(),
        ).place(relx=0.94, rely=0.02)

        header_lbl = ctk.CTkLabel(
            choose_area,
            text="Список пациентов",
            font=(FONT, 42, "bold"),
            text_color=AppColor.WHITE.value,
        ).pack(side="top", pady=(20, 0))

        scrollable_frame = ctk.CTkScrollableFrame(
            choose_area,
            height=300,
            scrollbar_button_color=AppColor.BUTTON.value,
            scrollbar_button_hover_color=AppColor.BUTTON_HOVER.value,
            corner_radius=20,
            border_color=AppColor.BLACK.value,
            border_width=2,
            fg_color=AppColor.SUBMAIN.value,
        )
        scrollable_frame.pack(side="top", fill="x", padx=40, pady=(20, 0))

        view_btn = ctk.CTkButton(
            choose_area,
            text="Просмотр",
            fg_color=AppColor.BUTTON.value,
            text_color=AppColor.WHITE.value,
            corner_radius=20,
            font=(FONT, 40, "bold"),
        ).pack(side="top", ipady=10, pady=(30, 0))


def get_btn_image():
    # Получаем путь к директории скрипта
    script_dir = Path(__file__).parent.parent

    # Формируем путь к файлу изображения
    path = script_dir / "images"

    return ctk.CTkImage(Image.open(path / "cross.png"), size=(20, 20))
