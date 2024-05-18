import customtkinter as ctk

from app.ctk_helper import make_frame
from enums import AppColor


class MainPatientScreen(ctk.CTkFrame):
    def __init__(self, controller, parent, session):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.session = session

        choose_area = make_frame(self, AppColor.SUBMAIN.value, 20, 750, 450)
        choose_area.pack(anchor="center", expand=True)
