import customtkinter as ctk
from tkinter import IntVar

from app.ctk_helper import make_frame, make_entry, make_rbtn, make_btn
from app.videoplayer import VideoPlayer
from enums import AppColor, UserType

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")


class ReabilitationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
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
        self.show_frame("registrtaion")

    def update_shoulders_angle(self, values):
        self.l_shoulder_angle.configure(text=f"{values[0]}")
        self.r_shoulder_angle.configure(text=f"{values[1]}")

    def update_elbows_angle(self, values):
        self.l_elbow_angle.configure(text=f"{values[0]}")
        self.r_elbow_angle.configure(text=f"{values[1]}")

    # TODO: переписать все ctk.CTkFrame на make_frame()
    def create_frames(self):
        exercises = ctk.CTkFrame(self.main_frame)
        self.frames["exercises"] = exercises
        # region Frames
        # Main
        fl = make_frame(exercises, AppColor.MAIN.value)
        fc = make_frame(exercises, AppColor.MAIN.value)
        fr = make_frame(exercises, AppColor.MAIN.value)
        fb = make_frame(exercises, AppColor.MAIN.value)

        # Subframes
        fb_up = make_frame(fb, AppColor.SUBMAIN.value)
        fb_down = make_frame(fb, AppColor.MAIN.value)

        # Elements
        video_tool_stripe = make_frame(fb_up, AppColor.SUBMAIN.value)
        # region Text
        l_shoulder = ctk.CTkLabel(
            fl, text="Левое плечо", font=("Arial", 22), text_color=AppColor.WHITE.value
        )
        l_elbow = ctk.CTkLabel(
            fl, text="Левый локоть", font=("Arial", 22), text_color=AppColor.WHITE.value
        )
        r_shoulder = ctk.CTkLabel(
            fr, text="Правое плечо", font=("Arial", 22), text_color=AppColor.WHITE.value
        )
        r_elbow = ctk.CTkLabel(
            fr,
            text="Правый локоть",
            font=("Arial", 22),
            text_color=AppColor.WHITE.value,
        )
        # endregion

        self.l_shoulder_angle = ctk.CTkLabel(
            fl, text="0", font=("Arial", 22), text_color=AppColor.WHITE.value, width=100
        )
        self.l_elbow_angle = ctk.CTkLabel(
            fl, text="0", font=("Arial", 22), text_color=AppColor.WHITE.value, width=100
        )
        self.r_shoulder_angle = ctk.CTkLabel(
            fr, text="0", font=("Arial", 22), text_color=AppColor.WHITE.value, width=100
        )
        self.r_elbow_angle = ctk.CTkLabel(
            fr, text="0", font=("Arial", 22), text_color=AppColor.WHITE.value, width=100
        )

        canvas = ctk.CTkCanvas(  # Виджет Canvas для отображения видео
            fc, highlightthickness=0, bg=AppColor.MAIN.value
        )
        # endregion

        # region Pack|Grid
        fl.grid(row=0, column=0, columnspan=2, rowspan=3, sticky="nsew")
        fc.grid(row=0, column=2, columnspan=6, rowspan=3, sticky="nsew")
        fr.grid(row=0, column=8, columnspan=2, rowspan=3, sticky="nsew")
        fb.grid(row=3, column=0, columnspan=10, sticky="nsew")

        # Pack|Grid subframes
        fb_up.grid(row=0, column=0, columnspan=6, rowspan=1, sticky="nsew")
        fb_down.grid(row=1, column=0, columnspan=6, rowspan=3, sticky="nsew")

        # Pack|Grid elements
        video_tool_stripe.pack(fill="both", expand=True)
        l_shoulder.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=(20, 0))
        l_elbow.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=(20, 0))
        r_elbow.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=(20, 0))
        r_shoulder.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=(20, 0))
        self.l_shoulder_angle.grid(row=0, column=1, sticky="w")
        self.l_elbow_angle.grid(row=1, column=1, sticky="w")
        self.r_shoulder_angle.grid(row=0, column=1, sticky="w")
        self.r_elbow_angle.grid(row=1, column=1, sticky="w")
        canvas.pack(fill="both", expand=True, padx=70)
        # endregion

        # region GRID CONFIG
        # main
        for c in range(10):
            exercises.grid_columnconfigure(c, weight=1)
        for r in range(4):
            exercises.grid_rowconfigure(r, weight=1)

        # subframes
        fb.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        fb.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # endregion

        registrtaion = ctk.CTkFrame(self.main_frame, fg_color=AppColor.MAIN.value)
        self.frames["registrtaion"] = registrtaion
        # region Frames
        reg_area = make_frame(registrtaion, AppColor.SUBMAIN.value, 20, 750, 650)
        # region reg_area elements
        name_entry = make_entry(reg_area, "Имя")
        surname_entry = make_entry(reg_area, "Фамилия")
        patronimic_entry = make_entry(reg_area, "Отчество (необязательно)")
        login_entry = make_entry(reg_area, "Логин")
        password_entry = make_entry(reg_area, "Пароль")

        rbtn_value = IntVar(value=UserType.Patient.value)
        patient_rbtn = make_rbtn(
            reg_area, "пациент", rbtn_value, UserType.Patient.value
        )
        doctor_rbtn = make_rbtn(reg_area, "врач", rbtn_value, UserType.Doctor.value)

        reg_btn = make_btn(reg_area, "Регистрация")
        # endregion
        # endregion

        # region Pack|GRID
        reg_area.pack(anchor="center", expand=True)
        reg_area.grid_propagate(False)

        name_entry.grid(
            row=0,
            column=1,
            columnspan=5,
            padx=40,
            ipadx=5,
            sticky="ew",
        )
        surname_entry.grid(
            row=1,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        patronimic_entry.grid(
            row=2,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        login_entry.grid(
            row=3,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        password_entry.grid(
            row=4,
            column=1,
            columnspan=5,
            padx=40,
            ipady=5,
            sticky="ew",
        )
        patient_rbtn.grid(
            row=5,
            column=2,
        )
        doctor_rbtn.grid(
            row=5,
            column=4,
        )
        reg_btn.grid(row=6, column=3)
        # endregion

        # region GRID CONFIG
        # main
        for c in range(7):
            reg_area.grid_columnconfigure(c, weight=1)
        for r in range(9):
            reg_area.grid_rowconfigure(r, weight=1)

        # endregion

        callbacks = {
            "update_shoulders_angle": self.update_shoulders_angle,
            "update_elbows_angle": self.update_elbows_angle,
        }
        # Создаем экземпляр класса VideoPlayer
        video_player = VideoPlayer(exercises, canvas, video_tool_stripe, callbacks)

    def show_frame(self, frame_name):
        # Скрываем все фреймы
        for frame in self.frames.values():
            frame.pack_forget()

        # Отображаем нужный фрейм
        self.frames[frame_name].pack(fill="both", expand=True)

    # user = User(
    #     first_name="Сергей",
    #     last_name="Охлопков",
    #     patronymic="",
    #     login="myrza",
    #     password="123",
    #     email="s_okhlopkov@mail.ru",
    # )
    # create_user(SessionLocal(), user)
    # app.mainloop()
