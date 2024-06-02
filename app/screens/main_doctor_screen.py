from pathlib import Path
from typing import List

import customtkinter as ctk
from PIL import Image

from app.ctk_helper import make_frame, SelectableLabel, SelectScrollFrame
from db.crud import get_patients_by_doctor_id
from db.database import get_session
from db.schemas import SelectPatient
from enums import AppColor

FONT = "Inter"


class MainDoctorScreen(ctk.CTkFrame):
    def __init__(self, controller, parent):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.controller = controller
        self.patients: List[SelectPatient] = self.get_patients()
        self.labels = []
        self.selected_patient: int

        cross = self.get_btn_image()

        choose_area = make_frame(self, AppColor.SUBMAIN.value, 20, 750, 560)
        choose_area.pack(anchor="center", expand=True)
        choose_area.pack_propagate(False)

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

        scrollable_frame = SelectScrollFrame(
            choose_area,
            self,
            self.patients,
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

    def get_patients(self):
        if self.controller.user:
            doctor_id = self.controller.user.id
            with get_session() as session:
                return get_patients_by_doctor_id(session, doctor_id)

    @staticmethod
    def get_btn_image():
        # Получаем путь к директории скрипта
        script_dir = Path(__file__).parent.parent

        # Формируем путь к файлу изображения
        path = script_dir / "images"

        return ctk.CTkImage(Image.open(path / "cross.png"), size=(20, 20))
