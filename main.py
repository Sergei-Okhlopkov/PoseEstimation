import customtkinter as ctk

from app.ctk_helper import make_frame
from app.videoplayer import VideoPlayer
from db.crud import create_user
from db.database import Base, engine, SessionLocal
from db.models import User

# Пересоздали схему БД
Base.metadata.drop_all(bind=engine)  # TODO: добавить файл .env для пересоздания БД

Base.metadata.create_all(bind=engine)

l_shoulder_angle = None
l_elbow_angle = None
r_shoulder_angle = None
r_elbow_angle = None


def update_shoulders_angle(values):
    l_shoulder_angle.configure(text=f"{values[0]}")
    r_shoulder_angle.configure(text=f"{values[1]}")


def update_elbows_angle(values):
    l_elbow_angle.configure(text=f"{values[0]}")
    r_elbow_angle.configure(text=f"{values[1]}")


# TODO: заменить все текстовые пременные (цвета) на enum коллекцию

if __name__ == "__main__":
    ctk.set_default_color_theme("dark-blue")
    ctk.set_appearance_mode("dark")

    app = ctk.CTk()
    app.title("Нейро-реабилитация")
    # app.geometry("900x600")
    # На весь экран
    app.after(0, lambda: app.state("zoomed"))

    # region Frames
    # Main
    fl = make_frame(app, "#2A2A2C")
    fc = make_frame(app, "#2A2A2C")
    fr = make_frame(app, "#2A2A2C")
    fb = make_frame(app, "#2A2A2C")

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
    app.grid_columnconfigure(list(range(10)), weight=1)
    app.grid_rowconfigure(list(range(4)), weight=1)

    # subframes
    fb.grid_columnconfigure(list(range(6)), weight=1)
    fb.grid_rowconfigure(list(range(4)), weight=1)

    # endregion

    # frame_bottom.grid_forget() TODO: использовать для сокрытия элементов

    callbacks = {
        "update_shoulders_angle": update_shoulders_angle,
        "update_elbows_angle": update_elbows_angle,
    }
    # Создаем экземпляр класса VideoPlayer
    video_player = VideoPlayer(app, canvas, video_tool_stripe, callbacks)
    user = User(
        first_name="Сергей",
        last_name="Охлопков",
        patronymic="",
        login="myrza",
        password="123",
        email="s_okhlopkov@mail.ru",
    )
    create_user(SessionLocal(), user)
    app.mainloop()
