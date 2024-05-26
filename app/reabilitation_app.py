import customtkinter as ctk

from app.screens.auth_screen import AuthScreen
from app.screens.exercises_screen import ExerciseScreen
from app.screens.main_doctor_screen import MainDoctorScreen
from app.screens.main_patient_screen import MainPatientScreen
from app.screens.registration_screen import RegistrationScreen
from app.screens.statistics_doctor_screen import StatisticsDoctorScreen
from app.screens.statistics_patient_screen import StatisticsPatientScreen
from enums import AppScreen

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")


class ReabilitationApp(ctk.CTk):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.title("Нейро-реабилитация")
        self.geometry("400x300")
        self.after(0, lambda: self.state("zoomed"))  # На весь экран

        # Основной фрейм
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Создание дочерних фреймов
        self.frames = {}
        self.frames_to_update = {}  # фреймы, состояние которых необходимо обновлять
        self.create_frames()

        # Отображение первого фрейма
        self.show_frame(AppScreen.STATISTICS_DOCTOR.value)

    def create_frames(self):

        main_patient = MainPatientScreen(self, self.main_frame, self.session)
        self.frames[AppScreen.MAIN_PATIENT.value] = main_patient

        main_doctor = MainDoctorScreen(self, self.main_frame, self.session)
        self.frames[AppScreen.MAIN_DOCTOR.value] = main_doctor

        exercises = ExerciseScreen(self, self.main_frame, self.session)
        self.frames[AppScreen.EXERCISES.value] = exercises

        registration = RegistrationScreen(self, self.main_frame, self.session)
        self.frames[AppScreen.REGISTRATION.value] = registration

        auth = AuthScreen(self, self.main_frame, self.session)
        self.frames[AppScreen.AUTH.value] = auth

        statistics_patient = StatisticsPatientScreen(
            self, self.main_frame, self.session
        )
        self.frames[AppScreen.STATISTICS_PATIENT.value] = statistics_patient

        statistics_doctor = StatisticsDoctorScreen(self, self.main_frame, self.session)
        self.frames[AppScreen.STATISTICS_DOCTOR.value] = statistics_doctor

    def show_frame(self, frame_name):
        # Скрываем все фреймы
        for frame in self.frames.values():
            frame.pack_forget()

        # Отображаем нужный фрейм
        self.frames[frame_name].pack(fill="both", expand=True)

    def logout(self):
        self.show_frame(AppScreen.AUTH.value)
        # разлогинимся
