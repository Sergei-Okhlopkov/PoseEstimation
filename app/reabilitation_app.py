import customtkinter as ctk

from app.ctk_helper import make_frame
from app.videoplayer import VideoPlayer

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

        # Переменные для выывода
        self.l_shoulder_angle = None
        self.r_shoulder_angle = None

        self.l_elbow_angle = None
        self.r_elbow_angle = None

        # Создание дочерних фреймов
        self.frames = {}
        self.frames_to_update = {}  # фреймы, состояние которых необходимо обновлять
        self.create_frames()

        # Отображение первого фрейма
        self.show_frame("home")

    # def update_shoulders_angle(self, values):
    #     self.l_shoulder_angle.configure(text=f"{values[0]}")
    #     self.r_shoulder_angle.configure(text=f"{values[1]}")
    #
    # def update_elbows_angle(self, values):
    #     self.l_elbow_angle.configure(text=f"{values[0]}")
    #     self.r_elbow_angle.configure(text=f"{values[1]}")

    def create_frames(self):
        home_frame = ctk.CTkFrame(self.main_frame)
        self.frames["home"] = home_frame
        # region Frames
        # Main
        fl = make_frame(home_frame, "#2A2A2C")
        fc = make_frame(home_frame, "#2A2A2C")
        fr = make_frame(home_frame, "#2A2A2C")
        fb = make_frame(home_frame, "#2A2A2C")

        # Subframes
        fb_up = make_frame(fb, "#424C58")
        fb_down = make_frame(fb, "#2A2A2C")

        # Elements
        video_tool_stripe = make_frame(fb_up, "#424C58")
        # region Text
        l_shoulder = ctk.CTkLabel(
            fl, text="Левое плечо", font=("Arial", 22), text_color="white"
        )
        l_elbow = ctk.CTkLabel(
            fl, text="Левый локоть", font=("Arial", 22), text_color="white"
        )
        r_shoulder = ctk.CTkLabel(
            fr, text="Правое плечо", font=("Arial", 22), text_color="white"
        )
        r_elbow = ctk.CTkLabel(
            fr, text="Правый локоть", font=("Arial", 22), text_color="white"
        )
        # endregion

        l_shoulder_angle = ctk.CTkLabel(
            fl, text="0", font=("Arial", 22), text_color="white", width=100
        )
        l_elbow_angle = ctk.CTkLabel(
            fl, text="0", font=("Arial", 22), text_color="white", width=100
        )
        r_shoulder_angle = ctk.CTkLabel(
            fr, text="0", font=("Arial", 22), text_color="white", width=100
        )
        r_elbow_angle = ctk.CTkLabel(
            fr, text="0", font=("Arial", 22), text_color="white", width=100
        )

        canvas = ctk.CTkCanvas(  # Виджет Canvas для отображения видео
            fc, highlightthickness=0, bg="#2A2A2C"
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
        l_shoulder_angle.grid(row=0, column=1, sticky="w")
        l_elbow_angle.grid(row=1, column=1, sticky="w")
        r_shoulder_angle.grid(row=0, column=1, sticky="w")
        r_elbow_angle.grid(row=1, column=1, sticky="w")
        canvas.pack(fill="both", expand=True, padx=70)
        # endregion

        # region GRID CONFIG
        # main
        home_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        home_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # subframes
        fb.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        fb.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # endregion

        # frame_bottom.grid_forget() TODO: использовать для сокрытия элементов

        # callbacks = {
        #     "update_shoulders_angle": self.update_shoulders_angle,
        #     "update_elbows_angle": self.update_elbows_angle,
        # }
        # Создаем экземпляр класса VideoPlayer
        video_player = VideoPlayer(self, canvas, video_tool_stripe)  # , callbacks

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
