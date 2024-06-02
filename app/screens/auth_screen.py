import customtkinter as ctk

from app.ctk_helper import make_frame, make_entry, make_btn, make_clickable_lbl
from db.crud import get_user_by_login
from db.database import get_session
from db.hash_password import verify_password
from enums import AppColor, AppScreen, UserType


class AuthScreen(ctk.CTkFrame):
    def __init__(self, controller, parent):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.login_entry = None
        self.password_entry = None
        self.controller = controller

        # region Frames
        auth_area = make_frame(self, AppColor.SUBMAIN.value, 20, 750, 450)
        # region auth_area elements
        self.login_entry = make_entry(auth_area, "Логин")
        self.password_entry = make_entry(auth_area, "Пароль")
        auth_btn = make_btn(auth_area, "Вход", command=self.login)
        to_reg_btn = make_clickable_lbl(
            auth_area,
            "Регистрация",
            (controller.show_frame, AppScreen.REGISTRATION.value),
        )
        # endregion
        # endregion

        # region Pack|GRID
        auth_area.pack(anchor="center", expand=True)
        auth_area.grid_propagate(False)

        self.login_entry.grid(
            row=1,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        self.password_entry.grid(
            row=2,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )

        auth_btn.grid(row=3, column=4)
        to_reg_btn.grid(row=4, column=5, sticky="e")
        # endregion

        # region GRID CONFIG
        # main
        auth_area.grid_columnconfigure(list(range(7)), weight=1)
        auth_area.grid_rowconfigure(list(range(6)), weight=1)

        # endregion

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        with get_session() as session:
            user = get_user_by_login(session, login)

        if verify_password(password, user.password):
            self.controller.user = user

            if user.user_type == UserType.Patient.value:
                self.controller.show_frame(AppScreen.MAIN_PATIENT.value)

            if user.user_type == UserType.Doctor.value:
                self.controller.show_frame(AppScreen.MAIN_DOCTOR.value)
