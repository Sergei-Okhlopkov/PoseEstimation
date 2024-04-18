import customtkinter as ctk


def make_frame(root, color, corner_radius=0, width=100, height=50):
    return ctk.CTkFrame(
        root, fg_color=color, corner_radius=corner_radius, width=width, height=height
    )
