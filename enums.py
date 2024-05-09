from enum import Enum


class Color(Enum):
    BLACK = (0, 0, 0)
    BLUE = (255, 0, 0)
    CYAN = (255, 255, 0)
    CHARTREUSE = (0, 255, 128)
    DODGER_BLUE = (255, 128, 0)
    GREY = (134, 136, 138)
    GREEN = (0, 255, 0)
    MAGENTA = (128, 0, 255)
    LIGHT_GREY = (224, 224, 224)
    RED = (0, 0, 255)
    ROSE = (203, 192, 255)
    ORANGE = (50, 172, 255)
    VIOLET = (255, 0, 150)
    SPRING_GREEN = (128, 255, 0)
    PURPLE = (255, 0, 128)
    WHITE = (255, 255, 255)
    YELLOW = (0, 255, 255)


class ExerciseType(Enum):
    RIGHT_SHOULDER_ABDUCTION = 1  # отведение правого плеча
    LEFT_SHOULDER_ABDUCTION = 2  # отведение левого плеча
    RIGHT_ELBOW_BEND = 3
    LEFT_ELBOW_BEND = 4
    RIGHT_SHOULDER_BEND = 5  # сгибание правого плеча
    LEFT_SHOULDER_BEND = 6  # сгибание левого плеча
    KNEE_BEND = 7  # приседание


class UserType(Enum):
    Patient = 1
    Doctor = 2


class AppColor(Enum):
    MAIN = "#2A2A2C"
    SUBMAIN = "#424C58"
    BUTTON = "#4B9BFB"
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GREEN = "#00E9A1"
