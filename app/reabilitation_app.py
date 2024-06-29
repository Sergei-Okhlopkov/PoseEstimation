from typing import Optional

import customtkinter as ctk

from app.screens.auth_screen import AuthScreen
from app.screens.exercises_screen import ExerciseScreen
from app.screens.main_doctor_screen import MainDoctorScreen
from app.screens.main_patient_screen import MainPatientScreen
from app.screens.registration_screen import RegistrationScreen
from app.screens.statistics_doctor_screen import StatisticsDoctorScreen
from app.screens.statistics_patient_screen import StatisticsPatientScreen
from db.models import User
from enums import AppScreen

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")


class ReabilitationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Нейро-реабилитация")
        self.geometry("400x300")
        self.after(0, lambda: self.state("zoomed"))  # На весь экран

        # Данные о пользователе
        self.user: User = None
        self.selected_exercise: int = None
        self.selected_patient_id: int = None
        self.selected_patient: User = None

        # Основной фрейм
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Создание дочерних фреймов
        self.cur_screen = None
        self.frames = {
            AppScreen.REGISTRATION.value: RegistrationScreen,
            AppScreen.AUTH.value: AuthScreen,
            AppScreen.EXERCISES.value: ExerciseScreen,
            AppScreen.MAIN_PATIENT.value: MainPatientScreen,
            AppScreen.MAIN_DOCTOR.value: MainDoctorScreen,
            AppScreen.STATISTICS_PATIENT.value: StatisticsPatientScreen,
            AppScreen.STATISTICS_DOCTOR.value: StatisticsDoctorScreen,
        }

        # Отображение первого фрейма
        self.show_frame(AppScreen.AUTH.value)

    def show_frame(self, frame_name):
        frame_class = self.frames[frame_name]
        if self.cur_screen is None or not isinstance(self.main_frame, frame_class):
            if self.cur_screen:
                self.cur_screen.pack_forget()
            self.cur_screen = frame_class(self, self.main_frame)
            self.cur_screen.pack(fill="both", expand=True)

    def logout(self):
        self.show_frame(AppScreen.AUTH.value)
        # разлогинимся
