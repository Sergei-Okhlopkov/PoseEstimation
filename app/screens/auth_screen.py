import customtkinter as ctk

from app.ctk_helper import make_frame, make_entry, make_btn, make_clickable_lbl
from enums import AppColor, AppScreen


class AuthScreen(ctk.CTkFrame):
    def __init__(self, controller, parent, session):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.session = session
        self.auth_login_entry = None
        self.auth_password_entry = None

        # region Frames
        auth_area = make_frame(self, AppColor.SUBMAIN.value, 20, 750, 450)
        # region auth_area elements
        self.auth_login_entry = make_entry(auth_area, "Логин")
        self.auth_password_entry = make_entry(auth_area, "Пароль")
        auth_btn = make_btn(auth_area, "Вход")
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

        self.auth_login_entry.grid(
            row=1,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        self.auth_password_entry.grid(
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
        for c in range(7):
            auth_area.grid_columnconfigure(c, weight=1)
        for r in range(6):
            auth_area.grid_rowconfigure(r, weight=1)

        # endregion
