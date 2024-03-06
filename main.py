import time
import cv2
import mediapipe as mp
import numpy as np

OUTPUT_TIME = 0.1


def get_angle(landmarks):
    # локоть, плечо, таз - 3 точки для определения угла
    elbow = landmarks[0]
    shoulder = landmarks[1]
    pelvis = landmarks[2]

    se_list = [elbow.x - shoulder.x, elbow.y - shoulder.y]
    sp_list = [pelvis.x - shoulder.x, pelvis.y - shoulder.y]

    SE = np.array(se_list)
    SP = np.array(sp_list)

    scalar = np.dot(SE, SP)

    SE_norm = np.linalg.norm(SE)
    SP_norm = np.linalg.norm(SP)

    cos_a = scalar / (SE_norm * SP_norm)
    angle_rad = np.arccos(cos_a)  # получаем угол в радианах
    degrees = np.degrees(angle_rad)  # получаем угол в градусах

    return degrees


def get_front_shoulder_angles(landmarks):
    if landmarks:
        right_shoulder = [landmarks.landmark[14],
                          landmarks.landmark[12],
                          landmarks.landmark[24]]

        left_shoulder = [landmarks.landmark[13],
                         landmarks.landmark[11],
                         landmarks.landmark[23]]

        r_shoulder_angle = round(get_angle(right_shoulder), 1)
        l_shoulder_angle = round(get_angle(left_shoulder), 1)

        return [r_shoulder_angle, l_shoulder_angle]
    else:
        return ["no points", "no points"]


def draw_info(img, fps, angles, r_arm_speed):
    color_gray = (134, 136, 138)

    cv2.rectangle(img, (0, 0), (100, 200), color_gray, -1)
    cv2.putText(img, str(int(fps)), (30, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 0), 3)

    cv2.putText(img,
                str(angles[0]),
                (30, 100),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 0, 255),
                3)

    cv2.putText(img,
                str(r_arm_speed),
                (200, 100),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (255, 0, 150),
                3)

    cv2.putText(img,
                str(angles[1]),
                (30, 150),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 255, 0),
                3)


if __name__ == '__main__':
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()

    capture = cv2.VideoCapture(0)
    previous_time = time.time()

    # right shoulder (mediapipe: 14, 12, 24), then left (mediapipe: 13, 11, 23)
    angles = [0, 0]
    prev_angles = angles
    r_arm_speed = 0
    collected_speed = 0
    r_collected_count = 0
    left_arm_speed = 0
    start_time = time.time()

    while True:
        success, img = capture.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        # print(results.pose_landmarks)

        angles = get_front_shoulder_angles(results.pose_landmarks)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(img,
                                  results.pose_landmarks,
                                  mpPose.POSE_CONNECTIONS)

        current_time = time.time()
        delta_t = current_time - start_time

        # TODO: Избавиться от "no points", нужна другая обработка этой ситуации

        # собираем скорости + проверка на значение "no points"
        if type(angles[0]) is np.float64 and \
                type(prev_angles[0]) is np.float64:
            collected_speed += abs(prev_angles[0] - angles[0])

        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        prev_angles = angles

        # обновление скорости движения руки каждые OUTPUT_TIME
        if delta_t > OUTPUT_TIME:
            r_arm_speed = collected_speed / delta_t
            collected_speed = 0
            start_time = time.time()

        draw_info(img, fps, angles, r_arm_speed)

        cv2.imshow("webCam", img)
        if cv2.waitKey(10) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
