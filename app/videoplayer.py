import cv2
import time
import customtkinter
from PIL import Image, ImageTk

from recognition.calculations import get_shoulders_angles, get_elbows_angles
from recognition.joint_data import highlited_joints
from recognition.pose_recognition import recognize_pose, mpPose
from recognition.render import draw_pose

CANVAS_WIDTH = 1340
CANVAS_HEIGHT = 730
OUTPUT_TIME = 0.1


class VideoPlayer:
    def __init__(self, app, canvas, video_tool_stripe, callbacks):
        self.app = app
        self.canvas = canvas
        self.video_tool_stripe = video_tool_stripe

        # Callback функции для отображения в интерфейсе
        self.callbacks = callbacks

        # TODO: вынести кнопки в класс APP
        # Создаем кнопку Play/Pause
        self.play_button = customtkinter.CTkButton(
            self.video_tool_stripe,
            text="Pause",
            command=self.play_pause,
            bg_color="#424C58",
        )

        # Создаем кнопку вкл/выкл отрисовки позы
        self.pose_button = customtkinter.CTkButton(
            self.video_tool_stripe,
            text="Turn off rendering",
            command=self.draw_pose_switch,
            bg_color="#424C58",
        )

        self.play_button.pack(side="left", padx=[20, 50])
        self.pose_button.pack(side="left", padx=[20, 50])

        # Открываем видеопоток
        self.capture = cv2.VideoCapture(0)

        self.is_playing = True
        self.draw_pose = True

        self.previous_time = time.time()

        self.elbows_angles = [0, 0]
        self.shoulders_angles = [0, 0]
        self.prev_shoulder_angles = self.shoulders_angles
        self.prev_elbows_angles = self.elbows_angles
        self.shoulders_speed = [0, 0]
        self.elbows_speed = [0, 0]
        self.collected_speed = [0, 0, 0, 0]  # Для левой руки, затем для правой
        self.start_time = time.time()

        # Запускаем метод для обновления видео каждые 30 миллисекунд
        self.update_video()

    def play_pause(self):
        if self.is_playing:
            self.is_playing = False
            self.play_button.configure(text="Play")
        else:
            self.is_playing = True
            self.play_button.configure(text="Pause")

    def draw_pose_switch(self):
        if self.draw_pose:
            self.draw_pose = False
            self.pose_button.configure(text="Turn on rendering")
        else:
            self.draw_pose = True
            self.pose_button.configure(text="Turn off rendering")

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
                self.elbows_angles = get_elbows_angles(pose.pose_landmarks)

                if pose.pose_landmarks and self.draw_pose:
                    # Отрисовка позы
                    draw_pose(frame, pose.pose_landmarks, mpPose, highlited_joints)

                current_time = time.time()
                delta_t = current_time - self.start_time

                # собираем скорости
                self.collected_speed[0] += abs(
                    self.prev_elbows_angles[0] - self.elbows_angles[0]
                )

                self.collected_speed[1] += abs(
                    self.prev_elbows_angles[1] - self.elbows_angles[1]
                )

                self.collected_speed[2] += abs(
                    self.prev_shoulder_angles[0] - self.shoulders_angles[0]
                )

                self.collected_speed[3] += abs(
                    self.prev_shoulder_angles[1] - self.shoulders_angles[1]
                )

                # fps = 1 / (current_time - self.previous_time)
                self.previous_time = current_time
                self.prev_shoulder_angles = self.shoulders_angles

                # обновление скорости движения руки каждые OUTPUT_TIME
                if delta_t > OUTPUT_TIME:
                    self.shoulders_speed[0] = round(
                        self.collected_speed[0] / delta_t, 1
                    )
                    self.shoulders_speed[1] = round(
                        self.collected_speed[1] / delta_t, 1
                    )
                    self.shoulders_speed[0] = round(
                        self.collected_speed[2] / delta_t, 1
                    )
                    self.shoulders_speed[1] = round(
                        self.collected_speed[3] / delta_t, 1
                    )
                    self.collected_speed = [0, 0, 0, 0]
                    self.start_time = time.time()

                # Вывод всей информации в интерфейс
                self.update_interface_info(
                    self.callbacks,
                    self.shoulders_angles,
                    self.elbows_angles,
                    self.shoulders_speed,
                )
                # self.update_l_elbow_angle(self.l_arm_speed)

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
        self.app.after(30, self.update_video)

    @staticmethod
    def resize_and_keep_ratio(image, target_width, target_height):
        image_width, image_height = image.size
        width_ratio = target_width / image_width
        height_ratio = target_height / image_height
        scale_ratio = min(width_ratio, height_ratio)
        new_width = int(scale_ratio * image_width)
        new_height = int(scale_ratio * image_height)
        return image.resize((new_width, new_height))

    @staticmethod
    def update_interface_info(
        callbacks, shoulders_angles, elbows_angles, shoulders_speed
    ):
        update_elbows_angle = callbacks["update_elbows_angle"]
        update_shoulders_angle = callbacks["update_shoulders_angle"]

        update_shoulders_angle(shoulders_angles)
        update_elbows_angle(elbows_angles)
