from pathlib import Path
from PIL import Image
import customtkinter as ctk

from app.videoplayer import VideoPlayer
from enums import AppColor, Color
from recognition.render import bgr_to_hex

TOOL_BTN_SIZE = 250


class ExerciseScreen(ctk.CTkFrame):
    def __init__(self, controller, parent):
        super().__init__(parent, fg_color=AppColor.MAIN.value)

        knee_img, right_shoulder_img, left_shoulder_img, leaning_forward_img = (
            get_btns_images()
        )

        # Окно для фреймов упражнений
        self.exercise_frame = ctk.CTkFrame(
            self,
            fg_color=AppColor.MAIN.value,
            corner_radius=0,
        )
        self.exercise_frame.grid_columnconfigure(list(range(10)), weight=1)
        self.exercise_frame.grid_rowconfigure(list(range(1)), weight=1)

        self.exercise_frame.pack(anchor="n", fill="both", expand=True)
        self.exercise_frame.pack_propagate(False)

        self.menu = ctk.CTkFrame(
            self,
            height=220,
            corner_radius=0,
        )
        self.menu.pack(anchor="n", fill="x")
        self.menu.pack_propagate(False)

        left_bar = ctk.CTkFrame(
            self.exercise_frame, fg_color=AppColor.MAIN.value, corner_radius=0
        )
        center = ctk.CTkFrame(self.exercise_frame, corner_radius=0)
        right_bar = ctk.CTkFrame(
            self.exercise_frame, fg_color=AppColor.MAIN.value, corner_radius=0
        )

        left_bar.grid(row=0, column=0, sticky="nsew")
        center.grid(row=0, column=1, columnspan=8, sticky="nsew")
        right_bar.grid(row=0, column=9, sticky="nsew")

        # Виджет Canvas для отображения видео
        canvas = ctk.CTkCanvas(center, highlightthickness=0, bg=AppColor.GREEN.value)
        canvas.pack(fill="both", expand=True, padx=70)

        l_shoulder = ctk.CTkLabel(
            left_bar,
            text="Левый локоть",
            font=("Arial", 22),
            text_color=AppColor.WHITE.value,
        )
        l_shoulder.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=(20, 0))

        l_elbow = ctk.CTkLabel(
            left_bar,
            text="Левое плечо",
            font=("Arial", 22),
            text_color=AppColor.WHITE.value,
        )
        l_elbow.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=(20, 0))

        l_hip = ctk.CTkLabel(
            left_bar,
            text="Левое бедро",
            font=("Arial", 22),
            text_color=AppColor.WHITE.value,
        )
        l_hip.grid(row=2, column=0, sticky="w", pady=(10, 10), padx=(20, 0))

        l_knee = ctk.CTkLabel(
            left_bar,
            text="Левое колено",
            font=("Arial", 22),
            text_color=AppColor.WHITE.value,
        )
        l_knee.grid(row=3, column=0, sticky="w", pady=(10, 10), padx=(20, 0))

        r_shoulder = ctk.CTkLabel(
            right_bar,
            text="Правый локоть",
            font=("Arial", 22),
            text_color=AppColor.WHITE.value,
        )
        r_shoulder.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=(20, 0))

        r_elbow = ctk.CTkLabel(
            right_bar,
            text="Правое плечо",
            font=("Arial", 22),
            text_color=AppColor.WHITE.value,
        )
        r_elbow.grid(row=1, column=0, sticky="w", pady=(10, 10), padx=(20, 0))

        r_hip = ctk.CTkLabel(
            right_bar,
            text="Правое бедро",
            font=("Arial", 22),
            text_color=AppColor.WHITE.value,
        )
        r_hip.grid(row=2, column=0, sticky="w", pady=(10, 10), padx=(20, 0))

        r_knee = ctk.CTkLabel(
            right_bar,
            text="Правое колено",
            font=("Arial", 22),
            text_color=AppColor.WHITE.value,
        )
        r_knee.grid(row=3, column=0, sticky="w", pady=(10, 10), padx=(20, 0))

        self.l_shoulder_angle = ctk.CTkLabel(
            left_bar,
            text="0",
            font=("Arial", 22),
            text_color=bgr_to_hex(Color.GREEN.value),
            width=100,
        )
        self.l_shoulder_angle.grid(row=0, column=1, sticky="w")

        self.l_elbow_angle = ctk.CTkLabel(
            left_bar,
            text="0",
            font=("Arial", 22),
            text_color=bgr_to_hex(Color.BLUE.value),
            width=100,
        )
        self.l_elbow_angle.grid(row=1, column=1, sticky="w")

        self.r_shoulder_angle = ctk.CTkLabel(
            right_bar,
            text="0",
            font=("Arial", 22),
            text_color=bgr_to_hex(Color.GREEN.value),
            width=100,
        )
        self.r_shoulder_angle.grid(row=0, column=1, sticky="w")

        self.r_elbow_angle = ctk.CTkLabel(
            right_bar,
            text="0",
            font=("Arial", 22),
            text_color=bgr_to_hex(Color.BLUE.value),
            width=100,
        )
        self.r_elbow_angle.grid(row=1, column=1, sticky="w")

        self.l_hip_angle = ctk.CTkLabel(
            left_bar,
            text="0",
            font=("Arial", 22),
            text_color=bgr_to_hex(Color.VIOLET.value),
            width=100,
        )
        self.l_hip_angle.grid(row=2, column=1, sticky="w")

        self.l_knee_angle = ctk.CTkLabel(
            left_bar,
            text="0",
            font=("Arial", 22),
            text_color=bgr_to_hex(Color.CYAN.value),
            width=100,
        )
        self.l_knee_angle.grid(row=3, column=1, sticky="w")

        self.r_hip_angle = ctk.CTkLabel(
            right_bar,
            text="0",
            font=("Arial", 22),
            text_color=bgr_to_hex(Color.VIOLET.value),
            width=100,
        )
        self.r_hip_angle.grid(row=2, column=1, sticky="w")

        self.r_knee_angle = ctk.CTkLabel(
            right_bar,
            text="0",
            font=("Arial", 22),
            text_color=bgr_to_hex(Color.CYAN.value),
            width=100,
        )
        self.r_knee_angle.grid(row=3, column=1, sticky="w")

        callbacks = {
            "update_shoulders_angle": self.update_shoulders_angle,
            "update_elbows_angle": self.update_elbows_angle,
            "update_hips_angle": self.update_hips_angle,
            "update_knees_angle": self.update_knees_angle,
        }

        videoplayer = VideoPlayer(
            controller,
            canvas,
            callbacks,
        )

        video_tool_stripe = ctk.CTkFrame(
            self.menu, fg_color=AppColor.SUBMAIN.value, corner_radius=0, height=60
        )
        video_tool_stripe.pack(fill="x")
        video_tool_stripe.pack_propagate(False)

        control_btns = ctk.CTkFrame(video_tool_stripe, fg_color="transparent")
        control_btns.pack(anchor="center")

        control_btns.grid_columnconfigure(list(range(3)), weight=1)
        control_btns.grid_rowconfigure(list(range(1)), weight=1)

        start_btn = ctk.CTkButton(
            control_btns,
            text="Начать занятие",
            fg_color=AppColor.GREEN.value,
            font=("Inter", 24, "bold"),
            height=40,
            width=TOOL_BTN_SIZE,
            corner_radius=15,
        )
        start_btn.grid(
            row=0,
            column=0,
            pady=10,
        )

        stop_btn = ctk.CTkButton(
            control_btns,
            text="Закончить занятие",
            fg_color=AppColor.RED.value,
            font=("Inter", 24, "bold"),
            height=40,
            width=TOOL_BTN_SIZE,
            corner_radius=15,
        )
        stop_btn.grid(
            row=0,
            column=1,
            pady=10,
            padx=(20, 0),
        )

        switch_pose_btn = ctk.CTkButton(
            control_btns,
            text="Выключить отрисовку",
            fg_color=AppColor.BUTTON.value,
            font=("Inter", 24, "bold"),
            height=40,
            width=TOOL_BTN_SIZE,
            corner_radius=15,
            command=videoplayer.draw_pose_switch,
        )
        switch_pose_btn.grid(
            row=0,
            column=2,
            pady=10,
            padx=(20, 0),
        )

        exercise_buttons = ctk.CTkFrame(
            self.menu,
            fg_color=AppColor.MAIN.value,
            corner_radius=0,
        )
        exercise_buttons.pack(fill="both")

        left_hand_exercise_btn = ctk.CTkButton(
            exercise_buttons,
            text=None,
            image=left_shoulder_img,
            width=150,
            fg_color="transparent",
        ).pack(side="left", padx=(60, 0))

        right_hand_exercise_btn = ctk.CTkButton(
            exercise_buttons,
            text=None,
            image=right_shoulder_img,
            width=150,
            fg_color="transparent",
        ).pack(side="left", padx=(60, 0))

        knee_bend_exercise_btn = ctk.CTkButton(
            exercise_buttons,
            text=None,
            image=knee_img,
            width=150,
            fg_color="transparent",
        ).pack(side="left", padx=(60, 0))

        leaning_forward_exercise_btn = ctk.CTkButton(
            exercise_buttons,
            text=None,
            image=leaning_forward_img,
            width=150,
            fg_color="transparent",
        ).pack(side="left", padx=(60, 0))

    def update_shoulders_angle(self, values):
        self.l_shoulder_angle.configure(text=f"{values[0]}")
        self.r_shoulder_angle.configure(text=f"{values[1]}")

    def update_elbows_angle(self, values):
        self.l_elbow_angle.configure(text=f"{values[0]}")
        self.r_elbow_angle.configure(text=f"{values[1]}")

    def update_hips_angle(self, values):
        self.l_hip_angle.configure(text=f"{values[0]}")
        self.r_hip_angle.configure(text=f"{values[1]}")

    def update_knees_angle(self, values):
        self.l_knee_angle.configure(text=f"{values[0]}")
        self.r_knee_angle.configure(text=f"{values[1]}")


def get_btns_images():
    # Получаем путь к директории скрипта
    script_dir = Path(__file__).parent.parent

    img_size = 150
    # Формируем путь к файлу изображения
    path = script_dir / "images"

    knee_bend = ctk.CTkImage(
        Image.open(path / "btn_knee_bend.png"), size=(img_size, img_size)
    )
    shoulder_right = ctk.CTkImage(
        Image.open(path / "btn_right_shoulder.png"), size=(img_size, img_size)
    )
    shoulder_left = ctk.CTkImage(
        Image.open(path / "btn_left_shoulder.png"), size=(img_size, img_size)
    )

    leaning_forward = ctk.CTkImage(
        Image.open(path / "leaning_forward_btn.png"), size=(img_size, img_size)
    )

    return knee_bend, shoulder_right, shoulder_left, leaning_forward
