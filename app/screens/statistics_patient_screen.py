from typing import List
import matplotlib.pyplot as plt

import customtkinter as ctk
from pathlib import Path

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.ctk_helper import make_frame
from app.screens.helpers.statistics_helper import (
    exercise_types,
    get_graph_data,
    get_dynamic,
)
from db.crud import (
    get_user_by_id,
    get_user_med_sessions_by_exercise_type,
    get_last_comment_by_exercise_for_user,
)
from db.database import get_session
from db.models import MedSession
from db.schemas import GraphData
from enums import AppColor, AppScreen
from PIL import Image


class StatisticsPatientScreen(ctk.CTkFrame):
    def __init__(self, controller, parent):
        super().__init__(parent, fg_color=AppColor.MAIN.value)
        self.controller = controller

        self.spec_name_lbl = None
        self.last_date_lbl = None
        self.dynamic_direction_lbl = None
        self.exercise_lbl = None
        self.canvas: FigureCanvasTkAgg = None
        self.fig, self.axes = plt.subplots()

        self.last_date: str = "—"
        self.doctor_name: str = "не указан"
        self.exercise_name: str = None
        self.exercise_comment: str = None
        self.selected_exercise: int = 0  # начинаем показ с первого упражнения
        self.exercise_data: List[List[MedSession]] = None

        # загрузка данных перед показом
        self.load_data()
        # Изображения для кнопок
        arrow_left, arrow_right, cross = get_btns_images()

        # region Вёрстка
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

        cross_btn = ctk.CTkButton(
            statistics_area,
            text=None,
            image=cross,
            width=20,
            fg_color="transparent",
            command=lambda: controller.show_frame(AppScreen.MAIN_PATIENT.value),
        )

        info_frame = make_frame(
            statistics_area,
            color="transparent",
            width=500,
            height=650,
        )
        info_frame.pack(side="left", anchor="nw", padx=(60, 0), pady=(60, 30))

        # region CANVAS
        self.canvas_frame = make_frame(
            statistics_area,
            height=800,
            width=920,
            color=AppColor.MAIN.value,
            corner_radius=20,
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self.canvas_frame,
        )

        # PACK
        self.canvas_frame.pack(
            side="left",
            anchor="nw",
            padx=(40, 0),
            pady=(60, 30),
        )
        self.canvas_frame.pack_propagate(False)
        cross_btn.pack(anchor="n", pady=10, padx=(0, 10))

        # endregion

        # region Labels
        spec_lbl = ctk.CTkLabel(
            info_frame,
            text="Ваш специалист:",
            font=("Inter", 24, "bold"),
            text_color=AppColor.WHITE.value,
            width=100,
        )
        self.spec_name_lbl = ctk.CTkLabel(
            info_frame,
            text=self.doctor_name,
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            wraplength=250,
            justify="left",
        )
        date_lbl = ctk.CTkLabel(
            info_frame,
            text="Дата последнего занятия:",
            font=("Inter", 24, "bold"),
            text_color=AppColor.WHITE.value,
            width=100,
        )
        self.last_date_lbl = ctk.CTkLabel(
            info_frame,
            text=self.last_date,
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=100,
            wraplength=250,
            justify="left",
        )

        dynamic_lbl = ctk.CTkLabel(
            info_frame,
            text="Динамика за последние 5 занятий:",
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

        self.dynamic_direction_lbl = ctk.CTkLabel(
            info_frame,
            text="-",
            font=(
                "Arial",
                24,
            ),
            text_color=AppColor.WHITE.value,
            width=100,
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
            wraplength=350,
            justify="left",
        )

        comment_frame = make_frame(
            info_frame, AppColor.MAIN.value, 20, height=200, width=350
        )

        self.spec_comment_lbl = ctk.CTkLabel(
            comment_frame,
            text=self.exercise_comment,
            font=(
                "Arial",
                20,
            ),
            corner_radius=20,
            text_color=AppColor.WHITE.value,
            width=100,
            wraplength=300,
            justify="left",
        )

        choose_exercise_frame = make_frame(
            info_frame, color="transparent", width=200, height=200
        )

        left_btn = ctk.CTkButton(
            choose_exercise_frame,
            text=None,
            image=arrow_left,
            width=60,
            fg_color="transparent",
            border_width=0,
            command=self.prev_exercise,
        ).grid(sticky="w", column=0, row=0, padx=(0, 20))

        self.exercise_lbl = ctk.CTkLabel(
            choose_exercise_frame,
            text=self.exercise_name,
            font=("Arial", 24, "bold"),
            text_color=AppColor.WHITE.value,
            wraplength=200,
            justify="left",
        )

        self.exercise_lbl.grid(sticky="w", column=1, row=0)

        right_btn = ctk.CTkButton(
            choose_exercise_frame,
            text=None,
            image=arrow_right,
            width=60,
            fg_color="transparent",
            command=self.next_exercise,
        ).grid(sticky="e", column=2, row=0, padx=(20, 0))
        # endregion

        # region Pack|GRID

        # region info_frame
        spec_lbl.pack(anchor="nw", padx=(60, 0))
        self.spec_name_lbl.pack(anchor="nw", padx=(60, 0))
        date_lbl.pack(anchor="nw", padx=(60, 0), pady=(40, 0))
        self.last_date_lbl.pack(anchor="nw", padx=(60, 0))

        dynamic_lbl.pack(anchor="nw", padx=(60, 0), pady=(40, 0))
        self.dynamic_direction_lbl.pack(anchor="nw", padx=(60, 0))

        spec_comment_lbl.pack(anchor="nw", padx=(60, 0), pady=(40, 0))

        comment_frame.pack(anchor="nw", padx=(60, 0), pady=(10, 0))

        self.spec_comment_lbl.pack(anchor="nw", pady=20)

        # endregion

        choose_exercise_frame.pack(anchor="nw", padx=(60, 0), pady=20)

        choose_exercise_frame.grid_columnconfigure(list(range(3)), weight=1)
        choose_exercise_frame.grid_rowconfigure(list(range(1)), weight=1)
        self.update_interface()
        # endregion
        # endregion

    def load_data(self):
        with get_session() as session:
            doctor = get_user_by_id(session, self.controller.user.doctor_id)

        full_name = f"{doctor.last_name} {doctor.first_name}"
        if doctor.patronymic is not None:
            full_name += f" {doctor.patronymic}"

        self.doctor_name = full_name
        self.exercise_name = exercise_types[self.selected_exercise][0]

        with get_session() as session:
            comment = get_last_comment_by_exercise_for_user(
                session, self.controller.selected_exercise, self.controller.user.id
            )
            if comment is None:
                self.exercise_comment = ""
            else:
                self.exercise_comment = comment.text

        # загрузка данных по упражнениям
        self.load_exercise_data()

    def load_exercise_data(self):
        exercises = []
        for ex_type in exercise_types:
            with get_session() as session:
                ex_data = get_user_med_sessions_by_exercise_type(
                    session,
                    self.controller.user.id,
                    ex_type[1],  # ex_type(ex_name, ex_enum_type)
                )

            exercises.append([med_session for med_session in ex_data])
        self.exercise_data = exercises

    def update_interface(self):
        fig = self.fig
        ax = self.axes

        # Установим название упражнения
        self.exercise_lbl.configure(text=exercise_types[self.selected_exercise][0])

        # Установим последний комментарий
        with get_session() as session:
            comment = get_last_comment_by_exercise_for_user(
                session, self.selected_exercise, self.controller.user.id
            )
            if comment is None:
                self.spec_comment_lbl.configure(text="")
            else:
                self.spec_comment_lbl.configure(text=comment.text)

        if self.exercise_data[self.selected_exercise]:

            date = self.exercise_data[self.selected_exercise][-1].finished_at.strftime(
                "%Y-%m-%d"
            )
            # Установим дату последнего занятия
            self.last_date_lbl.configure(text=date)
            # Установим дату последнего занятия
            # self.last_date_lbl.configure(
            #     text=self.exercise_data[self.selected_exercise][-1].finished_at.date()
            # )

            # Определим динамику последних 5 занятий
            dynamic = get_dynamic(self.exercise_data[self.selected_exercise])
            self.dynamic_direction_lbl.configure(text=dynamic)

            graph_data = get_graph_data(self.exercise_data, self.selected_exercise)

            # Установка отступов
            plt.subplots_adjust(
                left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0, hspace=0
            )

            # отображение графиков
            ax.clear()
            ax.plot(
                graph_data.date,
                graph_data.angle,
                linewidth=3,
                marker="o",
                label="Максимальный угол отклонения",
            )
            ax.plot(
                graph_data.date,
                graph_data.speed,
                linewidth=3,
                marker="o",
                label="Средняя скорость движения",
            )

            # Добавляем легенду
            ax.legend(loc="upper left", fontsize=10, frameon=True)
            plt.xlabel("Дата")
            plt.ylabel("Угол")
            ax.xaxis.label.set_color(AppColor.WHITE.value)
            ax.yaxis.label.set_color(AppColor.WHITE.value)
            ax.tick_params(axis="x", colors=AppColor.WHITE.value)
            ax.tick_params(axis="y", colors=AppColor.WHITE.value)
            ax.set_facecolor(AppColor.MAIN.value)

            ax.spines["bottom"].set_color(AppColor.WHITE.value)
            ax.spines["top"].set_color(AppColor.WHITE.value)
            ax.spines["left"].set_color(AppColor.WHITE.value)
            ax.spines["right"].set_color(AppColor.WHITE.value)

            # Добавляем заголовок и подписи осей
            plt.title(
                "Статистика по упражнению за последние 10 занятий",
                color=AppColor.WHITE.value,
            )
            plt.grid(True)

            fig.set_facecolor(AppColor.MAIN.value)

            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            self.canvas.get_tk_widget().pack_configure(padx=10, pady=10)

    def next_exercise(self):
        if self.selected_exercise < 3:
            self.selected_exercise += 1
            self.update_interface()

    def prev_exercise(self):
        if self.selected_exercise > 0:
            self.selected_exercise -= 1
            self.update_interface()


def get_btns_images():
    # Получаем путь к директории скрипта
    script_dir = Path(__file__).parent.parent

    # Формируем путь к файлу изображения
    path = script_dir / "images"

    arrow_left = ctk.CTkImage(Image.open(path / "arrow_left.png"), size=(60, 60))
    arrow_right = ctk.CTkImage(Image.open(path / "arrow_right.png"), size=(60, 60))
    cross = ctk.CTkImage(Image.open(path / "cross.png"), size=(20, 20))

    return arrow_left, arrow_right, cross
