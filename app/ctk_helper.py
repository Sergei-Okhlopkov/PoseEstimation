from typing import List

import customtkinter as ctk

from db.schemas import SelectPatient
from enums import AppColor

FONT = "Inter"


def make_frame(
    root,
    color=None,
    corner_radius=0,
    width=100,
    height=50,
):
    return ctk.CTkFrame(
        root,
        fg_color=color,
        corner_radius=corner_radius,
        width=width,
        height=height,
        border_width=0,
    )


# TODO: вынести дефолтные настройки в файл настроек (цвет подсказки, радиус закругления, размер шрифта)
def make_entry(root, placeholder, corner_radius=20, font_size=36, height=60, show=None):
    return ctk.CTkEntry(
        root,
        height=height,
        placeholder_text=placeholder,
        corner_radius=corner_radius,
        fg_color=AppColor.WHITE.value,
        font=(FONT, font_size),
        text_color=AppColor.BLACK.value,
        placeholder_text_color=AppColor.GREY.value,
        show=show,
    )


def make_rbtn(root, text, variable, value, font_size=28, command=None):
    return ctk.CTkRadioButton(
        root,
        text=text,
        variable=variable,
        value=value,
        font=(FONT, font_size),
        fg_color=AppColor.WHITE.value,
        command=command,
    )


def make_btn(
    root,
    text,
    width=150,
    height=60,
    corner_radius=20,
    fg_color=AppColor.BUTTON.value,
    text_color=AppColor.WHITE.value,
    font_size=36,
    command=None,
    image=None,
):
    return ctk.CTkButton(
        root,
        width,
        height,
        corner_radius,
        text=text,
        fg_color=fg_color,
        text_color=text_color,
        font=(FONT, font_size),
        command=command,
        image=image,
    )


def make_clickable_lbl(
    root,
    text,
    click=None,
    font_size=18,
    text_color=AppColor.WHITE.value,
):
    return ClickableLabel(
        root, text=text, click=click, font_size=font_size, text_color=text_color
    )


class SelectScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, controller, patients):
        self.patients: List[SelectPatient] = patients
        self.labels = []
        self.controller = controller

        super().__init__(
            master,
            height=300,
            scrollbar_button_color=AppColor.BUTTON.value,
            scrollbar_button_hover_color=AppColor.BUTTON_HOVER.value,
            corner_radius=20,
            border_color=AppColor.BLACK.value,
            border_width=2,
            fg_color=AppColor.SUBMAIN.value,
        )

        if self.patients:
            for patient in self.patients:
                full_name = f"{patient.last_name} {patient.first_name}"
                if patient.patronymic is not None:
                    full_name += f" {patient.patronymic}"

                label = SelectableLabel(
                    self,
                    height=40,
                    text=full_name,
                    label_id=patient.id,
                    click=self.choose_label,
                )
                label.pack(anchor="w", fill="x", pady=5)
                self.labels.append(label)

    def choose_label(self, label_id):
        # Выбираем пациента
        self.controller.selected_patient = label_id

        # Красим выбранного, остальные приводим к дефолтному цвету
        for label in self.labels:
            if label.label_id == label_id:
                label.selected = True
                label.configure(fg_color=AppColor.MAIN.value)
            else:
                label.selected = False
                label.configure(fg_color=AppColor.SUBMAIN.value)


class SelectableLabel(ctk.CTkLabel):
    def __init__(
        self,
        master,
        height,
        text,
        label_id,
        font_size=30,
        text_color=AppColor.WHITE.value,
        click=None,
    ):
        super().__init__(
            master,
            height=height,
            text=text,
            font=(FONT, font_size),
            text_color=text_color,
            justify="left",
            anchor="w",
            padx=20,
            corner_radius=20,
        )
        self.selected = False
        self.label_id = label_id
        self.click = click

        self.bind("<Enter>", lambda e: self.on_enter())
        self.bind("<Leave>", lambda e: self.on_leave())

        self.bind("<Button-1>", lambda e: self.on_select())

    def on_select(self):
        self.selected = True
        self.click(self.label_id)

    def on_enter(self):
        if not self.selected:
            self.configure(fg_color=AppColor.LIST_HOVER.value)

    def on_leave(self):
        if not self.selected:
            self.configure(fg_color=AppColor.SUBMAIN.value)


class ClickableLabel(ctk.CTkLabel):
    def __init__(
        self,
        master,
        text,
        font_size=18,
        text_color=AppColor.WHITE.value,
        click=None,
    ):
        super().__init__(
            master, text=text, font=(FONT, font_size), text_color=text_color
        )

        self.click = click

        self.bind("<Enter>", lambda e: self.configure(cursor="hand2"))
        self.bind("<Leave>", lambda e: self.configure(cursor="arrow"))
        self.bind(
            "<Button-1>", lambda e: self.configure(text_color=AppColor.GREY.value)
        )
        self.bind(
            "<ButtonRelease-1>",
            self.enter_click_release,
        )

    def enter_click_release(self, *args):
        self.configure(text_color=AppColor.WHITE.value)
        frame = self.click[1]
        self.click[0](frame)
