import customtkinter as ctk

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
def make_entry(root, placeholder, corner_radius=20, font_size=36, height=60):
    return Entry(root, placeholder, corner_radius, font_size, height=height)


def make_rbtn(root, text, variable, value, font_size=28):
    return ctk.CTkRadioButton(
        root,
        text=text,
        variable=variable,
        value=value,
        font=(FONT, font_size),
        fg_color=AppColor.WHITE.value,
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


class Entry(ctk.CTkEntry):
    def __init__(
        self,
        master,
        placeholder="PLACEHOLDER",
        corner_radius=20,
        font_size=36,
        placeholder_color="grey",
        height=60,
    ):
        super().__init__(
            master,
            height=height,
            corner_radius=corner_radius,
            fg_color=AppColor.WHITE.value,
            text_color=placeholder_color,
            font=(FONT, font_size),
        )

        self.placeholder = placeholder
        self.placeholder_color = placeholder_color

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self._text_color = self.placeholder_color

    def foc_in(self, *args):
        if self._text_color == self.placeholder_color:
            self.delete("0", "end")
            self.configure(text_color=AppColor.BLACK.value)

    def foc_out(self, *args):
        if not self.get():
            self.configure(text_color=self.placeholder_color)
            self.put_placeholder()
