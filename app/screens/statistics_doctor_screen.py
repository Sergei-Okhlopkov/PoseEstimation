import customtkinter as ctk
from pathlib import Path
from app.ctk_helper import make_frame, make_entry
from enums import AppColor, AppScreen
from PIL import Image

PAD = 30
FONT = "Inter"


class StatisticsDoctorScreen(ctk.CTkFrame):
    def __init__(self, controller, parent, session):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.session = session
        self.patient_name_lbl: str = None
        self.current_date_lbl: str = None
        self.dynamic_direction_lbl = None
        self.exercise_lbl: str = None
        self.patient_id_lbl: int = None

        # Изображения для кнопок
        arrow_left, arrow_right, cross = get_btns_images()

        statistics_area = make_frame(
            self,
            AppColor.SUBMAIN.value,
            corner_radius=20,
        )

        comment_area = make_frame(self, "transparent", height=50)

        statistics_area.pack(
            anchor="n",
            expand=True,
            fill="both",
            padx=20,
            pady=30,
        )

        comment_area.pack(
            anchor="n",
            expand=True,
            fill="x",
            padx=20,
        )

        comment_area.grid_columnconfigure(list(range(12)), weight=1)
        comment_area.grid_rowconfigure(list(range(1)), weight=1)

        comment_entry = make_entry(
            comment_area,
            "Комментарий к упражнению",
            font_size=24,
        ).grid(row=0, column=0, columnspan=11, sticky="ew")

        # comment_entry.pack(side="left", fill="x")

        comment_btn = ctk.CTkButton(
            comment_area,
            text="Отправить",
            height=60,
            fg_color=AppColor.BUTTON.value,
            text_color=AppColor.WHITE.value,
            corner_radius=20,
            font=(FONT, 28, "bold"),
        )
        comment_btn.grid(row=0, column=11)

        cross_btn = ctk.CTkButton(
            statistics_area,
            text=None,
            image=cross,
            width=160,
            fg_color="transparent",
            command=lambda: controller.show_frame(AppScreen.MAIN_DOCTOR.value),
        )

        info_frame = make_frame(
            statistics_area,
            color="transparent",
            width=500,
            height=650,
        )
        info_frame.pack(side="left", anchor="nw", padx=(PAD, 0), pady=(60, 30))

        # region CANVAS
        canvas_frame = make_frame(
            statistics_area,
            color=AppColor.MAIN.value,
            corner_radius=20,
        )
        canvas = ctk.CTkCanvas(
            master=canvas_frame,
            bg=AppColor.MAIN.value,
            height=700,
            width=1250,
            borderwidth=0,
            highlightthickness=0,
        )

        # PACK
        canvas_frame.pack(side="left", anchor="nw", padx=(40, 0), pady=(60, 30))
        cross_btn.pack(anchor="n", pady=10, padx=10)
        canvas.pack(pady=10, padx=10)

        # endregion

        # region Labels
        spec_lbl = ctk.CTkLabel(
            info_frame,
            text="Пациент:",
            font=("Inter", 32, "bold"),
            text_color=AppColor.WHITE.value,
            width=100,
        )
        spec_lbl.pack(anchor="nw", padx=(PAD, 0))

        self.patient_name_lbl = ctk.CTkLabel(
            info_frame,
            text="Охлопков Сергей Михайлович",
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            wraplength=250,
            justify="left",
        )
        self.patient_name_lbl.pack(anchor="nw", padx=(PAD, 0))

        id_frame = ctk.CTkFrame(
            info_frame,
            fg_color="transparent",
        )
        id_frame.pack(anchor="w", padx=(PAD, 0), pady=(40, 0))

        id_lbl = ctk.CTkLabel(
            id_frame,
            text="Id: ",
            font=("Inter", 24, "bold"),
            text_color=AppColor.WHITE.value,
            width=10,
        )
        id_lbl.pack(side="left", anchor="w")

        self.patient_id_lbl = ctk.CTkLabel(
            id_frame,
            text="7879987437581",
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=90,
            wraplength=300,
            justify="left",
        )
        self.patient_id_lbl.pack(side="left", anchor="w")

        date_lbl = ctk.CTkLabel(
            info_frame,
            text="Дата последнего занятия:",
            font=("Inter", 24, "bold"),
            text_color=AppColor.WHITE.value,
            width=100,
        )
        date_lbl.pack(anchor="nw", padx=(PAD, 0), pady=(40, 0))

        self.current_date_lbl = ctk.CTkLabel(
            info_frame,
            text="05.03.2024",
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            wraplength=250,
            justify="left",
        )
        self.current_date_lbl.pack(anchor="nw", padx=(PAD, 0))

        dynamic_lbl = ctk.CTkLabel(
            info_frame,
            text="Динамика занятий за последние 5 дней:",
            font=(
                "Arial",
                24,
                "bold",
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            wraplength=300,
            justify="left",
        )
        dynamic_lbl.pack(anchor="nw", padx=(PAD, 0), pady=(40, 0))

        self.dynamic_direction_lbl = ctk.CTkLabel(
            info_frame,
            text="положительная",
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            wraplength=250,
            justify="left",
        )
        self.dynamic_direction_lbl.pack(anchor="nw", padx=(PAD, 0))

        choose_exercise_frame = make_frame(
            info_frame, color="transparent", width=200, height=200
        )
        choose_exercise_frame.pack(anchor="nw", padx=(PAD, 0), pady=40)

        choose_exercise_frame.grid_columnconfigure(list(range(3)), weight=1)
        choose_exercise_frame.grid_rowconfigure(list(range(1)), weight=1)

        left_btn = ctk.CTkButton(
            choose_exercise_frame,
            text=None,
            image=arrow_left,
            width=60,
            fg_color="transparent",
            border_width=0,
        ).grid(sticky="w", column=0, row=0, padx=(0, 20))

        self.exercise_lbl = ctk.CTkLabel(
            choose_exercise_frame,
            text="Отведение левой руки",
            font=("Arial", 24, "bold"),
            text_color=AppColor.WHITE.value,
            wraplength=200,
            justify="left",
        ).grid(sticky="w", column=1, row=0)

        right_btn = ctk.CTkButton(
            choose_exercise_frame,
            text=None,
            image=arrow_right,
            width=60,
            fg_color="transparent",
        ).grid(sticky="e", column=2, row=0, padx=(20, 0))
        # endregion


def get_btns_images():
    # Получаем путь к директории скрипта
    script_dir = Path(__file__).parent.parent

    # Формируем путь к файлу изображения
    path = script_dir / "images"

    arrow_left = ctk.CTkImage(Image.open(path / "arrow_left.png"), size=(60, 60))
    arrow_right = ctk.CTkImage(Image.open(path / "arrow_right.png"), size=(60, 60))
    cross = ctk.CTkImage(Image.open(path / "cross.png"), size=(20, 20))

    return arrow_left, arrow_right, cross
