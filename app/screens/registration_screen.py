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

from db.crud import create_user, get_doctors
from db.database import get_session
from db.hash_password import get_hash
from db.models import User
from enums import AppColor, UserType, AppScreen

PATRONYMIC_PLACEHOLDER = "Отчество (необязательно)"


def get_doctors_list():
    with get_session() as session:
        doctors = get_doctors(session)
    doctors_list = []
    for doctor in doctors:
        item = f"{doctor.id} {doctor.last_name} {doctor.first_name} "
        if doctor.patronymic:
            item += f"{doctor.patronymic}"
        doctors_list.append(item)

    return doctors_list


def get_doctor_id(doctor_str) -> int:
    return int(doctor_str.split()[0])


class RegistrationScreen(ctk.CTkFrame):
    def __init__(self, controller, parent):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.controller = controller

        self.password_entry = None
        self.login_entry = None
        self.patronymic_entry = None
        self.surname_entry = None
        self.name_entry = None
        self.email_entry = None
        self.user_type = IntVar()
        self.doctors = get_doctors_list()

        # region Frames
        reg_area = make_frame(self, AppColor.SUBMAIN.value, 20, 750, 750)
        # region reg_area elements
        self.surname_entry = make_entry(reg_area, "Фамилия")
        self.name_entry = make_entry(reg_area, "Имя")
        self.patronymic_entry = make_entry(reg_area, PATRONYMIC_PLACEHOLDER)
        self.login_entry = make_entry(reg_area, "Логин")
        self.password_entry = make_entry(reg_area, "Пароль")
        self.email_entry = make_entry(reg_area, "Email")
        self.doctor_list = ctk.CTkComboBox(
            reg_area,
            values=self.doctors,
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
            command=self.on_combo_doctors,
        )
        doctor_rbtn = make_rbtn(
            reg_area,
            "врач",
            self.user_type,
            UserType.Doctor.value,
            command=self.off_combo_doctors,
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

    # TODO: в связи со сменой Entry на CTkEntry передалать код с patronymic_entry
    def reg(self):
        patronymic = None
        if self.patronymic_entry.get() != PATRONYMIC_PLACEHOLDER:
            patronymic = self.patronymic_entry.get()

        user = User(
            first_name=self.name_entry.get(),
            last_name=self.surname_entry.get(),
            patronymic=patronymic,
            login=self.login_entry.get(),
            password=get_hash(self.password_entry.get()),
            email=self.email_entry.get(),
            user_type=self.user_type.get(),
        )

        if user.user_type == UserType.Patient.value:
            user.doctor_id = get_doctor_id(self.doctor_list.get())

        with get_session() as session:
            create_user(session, user)
        # self.reload_doctor_list()
        self.doctor_list.configure(values=get_doctors_list())
        self.controller.show_frame(AppScreen.AUTH.value)

    def off_combo_doctors(self):
        self.doctor_list.grid_forget()

    def on_combo_doctors(self):
        self.doctor_list.grid(
            row=6,
            column=1,
            columnspan=5,
            padx=40,
            sticky="ew",
        )
