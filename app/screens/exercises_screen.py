import customtkinter as ctk

from app.ctk_helper import make_frame
from app.videoplayer import VideoPlayer
from enums import AppColor


class ExerciseScreen(ctk.CTkFrame):
    def __init__(self, controller, parent, session):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.session = session

        # region Frames
        # Main
        fl = make_frame(self, AppColor.MAIN.value)
        fc = make_frame(self, AppColor.MAIN.value)
        fr = make_frame(self, AppColor.MAIN.value)
        fb = make_frame(self, AppColor.MAIN.value)

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
            self.grid_columnconfigure(c, weight=1)
        for r in range(4):
            self.grid_rowconfigure(r, weight=1)

        # subframes
        fb.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        fb.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # endregion

        callbacks = {
            "update_shoulders_angle": self.update_shoulders_angle,
            "update_elbows_angle": self.update_elbows_angle,
        }
        # Создаем экземпляр класса VideoPlayer
        video_player = VideoPlayer(self, canvas, video_tool_stripe, callbacks)

    def update_shoulders_angle(self, values):
        self.l_shoulder_angle.configure(text=f"{values[0]}")
        self.r_shoulder_angle.configure(text=f"{values[1]}")

    def update_elbows_angle(self, values):
        self.l_elbow_angle.configure(text=f"{values[0]}")
        self.r_elbow_angle.configure(text=f"{values[1]}")
