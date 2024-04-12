import time
import cv2
import mediapipe as mp

from recognition.joint_data import highlited_joints
from recognition.render import draw_info, draw_pose
from recognition.calculations import get_front_shoulder_angles

OUTPUT_TIME = 0.1


if __name__ == "__main__":

    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()

    capture = cv2.VideoCapture(0)
    previous_time = time.time()

    # TODO: зарефакторить инициализацию

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

        angles = get_front_shoulder_angles(results.pose_landmarks)

        if results.pose_landmarks:
            draw_pose(img, results.pose_landmarks, mpPose, highlited_joints)

        current_time = time.time()
        delta_t = current_time - start_time

        # собираем скорости
        collected_speed += abs(prev_angles[0] - angles[0])

        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        prev_angles = angles

        # обновление скорости движения руки каждые OUTPUT_TIME
        if delta_t > OUTPUT_TIME:
            r_arm_speed = round(collected_speed / delta_t, 1)
            collected_speed = 0
            start_time = time.time()

        draw_info(img, fps, angles, r_arm_speed)

        cv2.imshow("webCam", img)
        if cv2.waitKey(10) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
