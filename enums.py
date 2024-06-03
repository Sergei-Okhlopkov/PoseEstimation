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
    # RIGHT_ELBOW_BEND = 3
    # LEFT_ELBOW_BEND = 4
    # RIGHT_SHOULDER_BEND = 5  # сгибание правого плеча
    # LEFT_SHOULDER_BEND = 6  # сгибание левого плеча
    KNEE_BEND = 3  # приседание
    LEANING_FORWARD = 4  # наклон вперёд


class UserType(Enum):
    Patient = 1
    Doctor = 2


class AppColor(Enum):
    MAIN = "#2A2A2C"
    SUBMAIN = "#424C58"
    BUTTON = "#4B9BFB"
    BUTTON_HOVER = "#14375D"
    LIST_HOVER = "#535362"
    BLACK = "#000000"
    GREEN = "#00E9A1"
    GREY = "#808080"
    WHITE = "#FFFFFF"
    RED = "#C60000"


class AppScreen(Enum):
    REGISTRATION = "registration"
    AUTH = "auth"
    EXERCISES = "exercises"
    MAIN_PATIENT = "main_patient"
    MAIN_DOCTOR = "main_doctor"
    STATISTICS_PATIENT = "statistics_patient"
    STATISTICS_DOCTOR = "statistics_doctor"
