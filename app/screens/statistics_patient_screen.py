import customtkinter as ctk
from pathlib import Path
from app.ctk_helper import make_frame, make_btn
from enums import AppColor, AppScreen
from PIL import Image, ImageTk


class StatisticsPatientScreen(ctk.CTkFrame):
    def __init__(self, controller, parent, session):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.session = session
        self.spec_name_lbl = None
        self.current_date_lbl = None
        self.dynamic_direction_lbl = None

        statistics_area = make_frame(
            self,
            AppColor.SUBMAIN.value,
            corner_radius=20,
        )

        statistics_area.pack(
            anchor="center",
            expand=True,
            fill="both",
            padx=20,
            pady=30,
        )

        info_frame = make_frame(
            statistics_area,
            color=AppColor.GREEN.value,
            corner_radius=20,
            width=500,
            height=650,
        )
        info_frame.pack(side="left", anchor="nw", padx=(60, 0), pady=(60, 30))

        # region CANVAS
        canvas_frame = make_frame(
            statistics_area,
            color="blue",
            corner_radius=20,
        )
        canvas = ctk.CTkCanvas(
            master=canvas_frame,
            bg=AppColor.MAIN.value,
            height=800,
            width=1050,
            borderwidth=0,
            highlightthickness=0,
        )

        # PACK
        canvas_frame.pack(side="left", anchor="nw", padx=(40, 0), pady=(60, 30))
        canvas.pack(pady=10, padx=10)

        # endregion

        # region Labels
        spec_lbl = ctk.CTkLabel(
            info_frame,
            text="Ваш специалист:",
            font=("Inter", 24, "bold"),
            text_color=AppColor.WHITE.value,
            width=100,
            fg_color=AppColor.BLACK.value,
        )
        self.spec_name_lbl = ctk.CTkLabel(
            info_frame,
            text="Здоровьев Николай Фёдорович",
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            fg_color=AppColor.BLACK.value,
            wraplength=250,
            justify="left",
        )
        date_lbl = ctk.CTkLabel(
            info_frame,
            text="Дата последнего занятия:",
            font=("Inter", 24, "bold"),
            text_color=AppColor.WHITE.value,
            width=100,
            fg_color=AppColor.BLACK.value,
        )
        self.current_date_lbl = ctk.CTkLabel(
            info_frame,
            text="05.03.2024",
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            fg_color=AppColor.BLACK.value,
            wraplength=250,
            justify="left",
        )

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
            fg_color=AppColor.BLACK.value,
            wraplength=300,
            justify="left",
        )

        self.dynamic_direction_lbl = ctk.CTkLabel(
            info_frame,
            text="положительная",
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            fg_color=AppColor.BLACK.value,
            wraplength=250,
            justify="left",
        )

        spec_comment_lbl = ctk.CTkLabel(
            info_frame,
            text="Комментарий специалиста:",
            font=(
                "Arial",
                24,
                "bold",
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            fg_color=AppColor.BLACK.value,
            wraplength=350,
            justify="left",
        )

        comment_frame = make_frame(
            info_frame, AppColor.MAIN.value, 20, height=200, width=350
        )

        self.spec_comment_lbl = ctk.CTkLabel(
            comment_frame,
            text="Так держать, Сергей! Ещё пара занятий и вы сможете стабильно выполнять все действия.",
            font=(
                "Arial",
                24,
            ),
            corner_radius=20,
            text_color=AppColor.WHITE.value,
            width=100,
            wraplength=300,
            justify="left",
        )

        choose_exercise_frame = make_frame(
            info_frame, color="red", width=200, height=200
        )
        arrow_left, arrow_right = get_btns_images()
        left_btn = ctk.CTkButton(
            choose_exercise_frame,
            text="",
            image=arrow_left,
            width=120,
            fg_color="transparent",
            border_width=0,
        ).grid(
            sticky="w",
            column=0,
        )

        right_btn = make_btn(
            choose_exercise_frame,
            text="",
            image=arrow_right,
            width=20,
            fg_color=AppColor.BLACK.value,
        ).grid(sticky="ne", column=2)
        # endregion

        # region Pack|GRID

        # region info_frame
        spec_lbl.pack(anchor="nw", padx=(60, 0))
        self.spec_name_lbl.pack(anchor="nw", padx=(60, 0))
        date_lbl.pack(anchor="nw", padx=(60, 0), pady=(40, 0))
        self.current_date_lbl.pack(anchor="nw", padx=(60, 0))

        dynamic_lbl.pack(anchor="nw", padx=(60, 0), pady=(40, 0))
        self.dynamic_direction_lbl.pack(anchor="nw", padx=(60, 0))

        spec_comment_lbl.pack(anchor="nw", padx=(60, 0), pady=(40, 0))

        comment_frame.pack(anchor="nw", padx=(60, 0), pady=(10, 0), ipady=10, ipadx=10)

        self.spec_comment_lbl.pack(anchor="nw", pady=20)

        # endregion

        choose_exercise_frame.pack(anchor="nw", padx=(60, 0), pady=20)

        choose_exercise_frame.grid_columnconfigure(list(range(3)), weight=1)

        # endregion


def get_btns_images():
    # Получаем путь к директории скрипта
    script_dir = Path(__file__).parent.parent

    # Формируем путь к файлу изображения
    path = script_dir / "images"

    arrow_left = ctk.CTkImage(Image.open(path / "arrow_left.png"), size=(90, 90))
    # arrow_left = ImageTk.PhotoImage(Image.open(path / "arrow_left.png"))
    arrow_right = ctk.CTkImage(Image.open(path / "arrow_right.png"), size=(90, 90))

    return arrow_left, arrow_right
