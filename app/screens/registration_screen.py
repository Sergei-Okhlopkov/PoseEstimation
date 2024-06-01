import customtkinter as ctk
from tkinter import IntVar

from app.ctk_helper import (
    make_frame,
    make_entry,
    make_rbtn,
    make_btn,
    make_clickable_lbl,
    FONT,
)
from db.crud import create_user
from db.models import User
from enums import AppColor, UserType, AppScreen


class RegistrationScreen(ctk.CTkFrame):
    def __init__(self, controller, parent, session):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.session = session
        self.auth_password_entry = None
        self.auth_login_entry = None

        self.password_entry = None
        self.login_entry = None
        self.patronymic_entry = None
        self.surname_entry = None
        self.name_entry = None
        self.email_entry = None
        self.user_type = IntVar()
        self.doctor_combo = True
        doctors = [
            "Здоровьев",
            "Неболеев",
            "Физиков",
            "Машустов",
            "Кедров",
        ]  # предзагрузка всех зарегистрированных врачей перед появлением фрейма

        # region Frames
        reg_area = make_frame(self, AppColor.SUBMAIN.value, 20, 750, 750)
        # region reg_area elements
        self.surname_entry = make_entry(reg_area, "Фамилия")
        self.name_entry = make_entry(reg_area, "Имя")
        self.patronymic_entry = make_entry(reg_area, "Отчество (необязательно)")
        self.login_entry = make_entry(reg_area, "Логин")
        self.password_entry = make_entry(reg_area, "Пароль")
        self.email_entry = make_entry(reg_area, "Email")
        self.doctor_list = ctk.CTkComboBox(
            reg_area,
            values=doctors,
            corner_radius=20,
            height=60,
            button_color=AppColor.BUTTON.value,
            button_hover_color=AppColor.BUTTON_HOVER.value,
            font=(FONT, 36),
            dropdown_font=(FONT, 36),
            fg_color=AppColor.WHITE.value,
            border_width=0,
            dropdown_fg_color=AppColor.WHITE.value,
            text_color=AppColor.BLACK.value,
            dropdown_text_color=AppColor.BLACK.value,
        )

        patient_rbtn = make_rbtn(
            reg_area,
            "пациент",
            self.user_type,
            UserType.Patient.value,
            command=self.switch_combo_doctors,
        )
        doctor_rbtn = make_rbtn(
            reg_area,
            "врач",
            self.user_type,
            UserType.Doctor.value,
            command=self.switch_combo_doctors,
        )

        reg_btn = make_btn(reg_area, "Регистрация", command=self.reg)
        to_enter_btn = make_clickable_lbl(
            reg_area, "Вход", (controller.show_frame, AppScreen.AUTH.value)
        )
        # endregion
        # endregion

        # region Pack|GRID
        reg_area.pack(anchor="center", expand=True)
        reg_area.grid_propagate(False)

        self.surname_entry.grid(
            row=0,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        self.name_entry.grid(
            row=1,
            column=1,
            columnspan=5,
            padx=40,
            ipadx=5,
            sticky="ew",
        )
        self.patronymic_entry.grid(
            row=2,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        self.login_entry.grid(
            row=3,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        self.password_entry.grid(
            row=4,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        self.email_entry.grid(
            row=5,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        self.doctor_list.grid(
            row=6,
            column=1,
            columnspan=5,
            padx=40,
            sticky="ew",
        )
        patient_rbtn.grid(
            row=7,
            column=2,
        )
        doctor_rbtn.grid(
            row=7,
            column=4,
        )
        reg_btn.grid(row=8, column=3)
        to_enter_btn.grid(row=9, column=5)
        # endregion

        # region GRID CONFIG
        # main
        reg_area.grid_columnconfigure(list(range(7)), weight=1)
        reg_area.grid_rowconfigure(list(range(11)), weight=1)

        # endregion

    def reg(self):

        user = User(
            first_name=self.name_entry.get(),
            last_name=self.surname_entry.get(),
            patronymic=self.patronymic_entry.get(),
            login=self.login_entry.get(),
            password=self.password_entry.get(),
            email=self.email_entry.get(),
            user_type=self.user_type.get(),
        )
        create_user(self.session(), user)

    def switch_combo_doctors(self):
        if self.doctor_combo:
            self.doctor_list.grid_forget()
            self.doctor_combo = False
        else:
            self.doctor_list.grid(
                row=6,
                column=1,
                columnspan=5,
                padx=40,
                sticky="ew",
            )
            self.doctor_combo = True
