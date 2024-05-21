import customtkinter as ctk

from app.ctk_helper import make_frame, make_btn
from enums import AppColor, AppScreen

BTN_SIZE = 300


class MainPatientScreen(ctk.CTkFrame):
    def __init__(self, controller, parent, session):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.session = session

        choose_area = make_frame(self, AppColor.SUBMAIN.value, 20, 750, 450)
        choose_area.pack(anchor="center", expand=True)
        choose_area.pack_propagate(False)

        btns_frame = make_frame(choose_area, "transparent")

        exercises_btn = make_btn(
            btns_frame,
            "Упражнения",
            BTN_SIZE,
            BTN_SIZE,
            command=lambda: controller(AppScreen.EXERCISES.value),
        )
        statistics_btn = make_btn(
            btns_frame,
            "Статистика",
            BTN_SIZE,
            BTN_SIZE,
            command=lambda: controller(AppScreen.STATISTICS_PATIENT.value),
        )

        btns_frame.place(relx=0.5, rely=0.5, anchor="center")
        exercises_btn.pack(side="left", padx=[0, 60])
        statistics_btn.pack(side="left")
