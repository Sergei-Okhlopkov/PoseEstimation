import datetime

import cv2
import time
import customtkinter
from PIL import Image, ImageTk

from db.crud import create_med_session, update_med_session
from db.database import get_session
from db.models import MedSession
from db.schemas import MedSessionUpdate
from enums import ExerciseType
from recognition.calculations import (
    get_shoulders_angles,
    get_elbows_angles,
    get_hips_angles,
    get_knees_angles,
)
from recognition.joint_data import highlited_joints
from recognition.pose_recognition import recognize_pose, mpPose
from recognition.render import draw_pose

CANVAS_WIDTH = 1340
CANVAS_HEIGHT = 730
OUTPUT_TIME = 0.1
UPDATE_VIDEO = 0.03


class VideoPlayer:
    def __init__(self, controller, canvas, callbacks):
        self.controller = controller
        self.canvas = canvas

        # Callback функции для отображения в интерфейсе
        self.callbacks = callbacks
        self.med_session_id: int = None
        self.max_angle: int = 0
        self.avg_speed: int = 0

        # Открываем видеопоток
        self.capture = cv2.VideoCapture(0)

        self.is_playing = True
        self.draw_pose = True
        self.recording_session = False

        self.previous_time = time.time()

        self.elbows_angles = [0, 0]
        self.shoulders_angles = [0, 0]
        self.hips_angles = [0, 0]
        self.knees_angles = [0, 0]

        self.prev_shoulder_angles = self.shoulders_angles
        self.prev_elbows_angles = self.elbows_angles
        self.prev_hips_angles = self.hips_angles
        self.prev_knees_angles = self.knees_angles

        self.shoulders_speed = [0, 0]
        self.elbows_speed = [0, 0]
        self.hips_speed = [0, 0]
        self.knees_speed = [0, 0]

        # Для левой руки, затем для правой, поочерёдно
        self.collected_speed_arms = [0, 0, 0, 0]
        self.collected_speed_legs = [0, 0, 0, 0]
        self.start_time = time.time()

        # Запускаем метод для обновления видео каждые 30 миллисекунд
        self.update_video()

    def draw_pose_switch(self):
        if self.draw_pose:
            self.draw_pose = False
        else:
            self.draw_pose = True

    def start_med_session(self):
        if not self.recording_session:
            self.avg_speed = 0
            self.max_angle = 0
            self.recording_session = True

            med_session = MedSession(
                user_id=self.controller.user.id,
                started_at=datetime.datetime.utcnow(),
                finished_at=None,
                exercise_type=self.controller.selected_exercise,
                max_angle=None,
                avg_speed=None,
            )

            with get_session() as session:
                created_med_session = create_med_session(session, med_session)

            self.med_session_id = created_med_session.id
        else:
            # Сессия уже запущена, перед запуском новой нужно остановить старую
            pass

    def stop_med_session(self):
        if self.recording_session:
            self.recording_session = False

            med_session_update = MedSessionUpdate(
                finished_at=datetime.datetime.utcnow(),
                max_angle=self.max_angle,
                avg_speed=self.avg_speed,
            )

            with get_session() as session:
                update_med_session(session, self.med_session_id, med_session_update)

    def update_video(self):
        if self.is_playing:
            # Считываем кадр из видеопотока
            ret, frame = self.capture.read()
            if ret:
                # Отражение по вертикали
                frame = cv2.flip(frame, 1)
                # Распознавание позы
                pose = recognize_pose(frame)

                self.shoulders_angles = get_shoulders_angles(pose.pose_landmarks)
                self.elbows_angles = get_elbows_angles(pose.pose_landmarks, revert=True)
                self.hips_angles = get_hips_angles(pose.pose_landmarks, revert=True)
                self.knees_angles = get_knees_angles(pose.pose_landmarks, revert=True)

                if pose.pose_landmarks and self.draw_pose:
                    # Отрисовка позы
                    draw_pose(frame, pose.pose_landmarks, mpPose, highlited_joints)

                current_time = time.time()
                delta_t = current_time - self.start_time

                # region Сбор статистики за занятие
                if self.recording_session:
                    if (
                        self.controller.selected_exercise
                        == ExerciseType.LEFT_SHOULDER_ABDUCTION.value
                    ):
                        # diff - разница предыдущего угла и текущего
                        diff = self.shoulders_angles[0] - self.prev_shoulder_angles[0]
                        self.collect_statistics(self.shoulders_angles[0], diff)

                    if (
                        self.controller.selected_exercise
                        == ExerciseType.RIGHT_SHOULDER_ABDUCTION.value
                    ):
                        diff = self.shoulders_angles[1] - self.prev_shoulder_angles[1]
                        self.collect_statistics(self.shoulders_angles[1], diff)

                    if (
                        self.controller.selected_exercise
                        == ExerciseType.KNEE_BEND.value
                    ):
                        knee_angle = sum(self.knees_angles) / len(self.knees_angles)
                        diff = sum(self.prev_knees_angles) / len(self.prev_knees_angles)
                        self.collect_statistics(knee_angle, diff)

                    if (
                        self.controller.selected_exercise
                        == ExerciseType.LEANING_FORWARD.value
                    ):
                        hips_angle = sum(self.hips_angles) / len(self.hips_angles)
                        diff = sum(self.prev_hips_angles) / len(self.prev_hips_angles)
                        self.collect_statistics(hips_angle, diff)

                # endregion

                # собираем скорости
                self.collected_speed_arms[0] += abs(
                    self.prev_elbows_angles[0] - self.elbows_angles[0]
                )

                self.collected_speed_arms[1] += abs(
                    self.prev_elbows_angles[1] - self.elbows_angles[1]
                )

                self.collected_speed_arms[2] += abs(
                    self.prev_shoulder_angles[0] - self.shoulders_angles[0]
                )

                self.collected_speed_arms[3] += abs(
                    self.prev_shoulder_angles[1] - self.shoulders_angles[1]
                )

                self.previous_time = current_time
                self.prev_shoulder_angles = self.shoulders_angles
                self.prev_elbows_angles = self.elbows_angles
                self.prev_hips_angles = self.hips_angles
                self.prev_knees_angles = self.knees_angles

                # обновление скорости движения руки каждые OUTPUT_TIME
                if delta_t > OUTPUT_TIME:
                    self.shoulders_speed[0] = round(
                        self.collected_speed_arms[0] / delta_t, 1
                    )
                    self.shoulders_speed[1] = round(
                        self.collected_speed_arms[1] / delta_t, 1
                    )
                    self.shoulders_speed[0] = round(
                        self.collected_speed_arms[2] / delta_t, 1
                    )
                    self.shoulders_speed[1] = round(
                        self.collected_speed_arms[3] / delta_t, 1
                    )
                    self.collected_speed_arms = [0, 0, 0, 0]
                    self.start_time = time.time()

                # Вывод всей информации в интерфейс
                self.update_interface_info(
                    self.shoulders_angles,
                    self.elbows_angles,
                    self.hips_angles,
                    self.knees_angles,
                )

                # Преобразуем кадр из BGR (OpenCV) в RGB (PIL)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Создаем объект Image из массива байтов кадра
                image = Image.fromarray(image)
                # Пропорционально изменяем размер изображения
                # Масштабируем изображение до размеров Canvas
                image = self.resize_and_keep_ratio(image, CANVAS_WIDTH, CANVAS_HEIGHT)
                # Преобразуем изображение в объект PhotoImage для отображения в Canvas
                photo = ImageTk.PhotoImage(image=image)
                # photo = ImageTk.PhotoImage(image=image)

                # Устанавливаем изображение в Canvas
                self.canvas.create_image(0, 0, anchor=customtkinter.NW, image=photo)
                # # Удаляем ссылку на объект PhotoImage, чтобы избежать утечки памяти
                self.canvas.image = photo

        # Запускаем рекурсивно метод для обновления видео каждые 30 миллисекунд
        self.controller.after(30, self.update_video)

    def collect_statistics(self, angle, speed_up) -> None:
        if angle > self.max_angle:
            self.max_angle = int(angle)

        if speed_up > 0:
            self.avg_speed = int((self.avg_speed + speed_up) / 2)

    @staticmethod
    def resize_and_keep_ratio(image, target_width, target_height):
        image_width, image_height = image.size
        width_ratio = target_width / image_width
        height_ratio = target_height / image_height
        scale_ratio = min(width_ratio, height_ratio)
        new_width = int(scale_ratio * image_width)
        new_height = int(scale_ratio * image_height)
        return image.resize((new_width, new_height))

    def update_interface_info(
        self,
        shoulders_angles,
        elbows_angles,
        hips_angles,
        knees_angles,
    ):
        self.callbacks["update_elbows_angle"](shoulders_angles)
        self.callbacks["update_shoulders_angle"](elbows_angles)
        self.callbacks["update_hips_angle"](hips_angles)
        self.callbacks["update_knees_angle"](knees_angles)
