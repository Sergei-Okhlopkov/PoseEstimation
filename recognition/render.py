import cv2

from recognition.calculations import get_middle_coordinates
from enums import Color
from recognition.joint_data import joint_to_color


def draw_info(img, fps, angles, r_arm_speed):
    cv2.rectangle(img, (0, 0), (150, 200), Color.LIGHT_GREY.value, -1)

    cv2.putText(img, "fps", (10, 20), cv2.FONT_HERSHEY_PLAIN, 0.7, Color.BLACK.value, 1)

    cv2.putText(
        img, str(int(fps)), (60, 20), cv2.FONT_HERSHEY_PLAIN, 1, Color.BLACK.value, 2
    )

    cv2.putText(
        img, "r_angle", (10, 40), cv2.FONT_HERSHEY_PLAIN, 0.7, Color.BLACK.value, 1
    )
    # Правое плечо (угол)
    cv2.putText(
        img,
        str(angles[0]),
        (60, 40),
        cv2.FONT_HERSHEY_PLAIN,
        1,
        Color.DODGER_BLUE.value,
        2,
    )

    cv2.putText(
        img, "r_speed", (10, 60), cv2.FONT_HERSHEY_PLAIN, 0.7, Color.BLACK.value, 1
    )
    # Правое плечо (скорость)
    cv2.putText(
        img,
        str(r_arm_speed),
        (60, 60),
        cv2.FONT_HERSHEY_PLAIN,
        1,
        Color.VIOLET.value,
        2,
    )

    cv2.putText(
        img, "l_angle", (10, 80), cv2.FONT_HERSHEY_PLAIN, 0.7, Color.BLACK.value, 1
    )
    # Левое плечо (угол)
    cv2.putText(
        img, str(angles[1]), (60, 80), cv2.FONT_HERSHEY_PLAIN, 1, Color.BLUE.value, 2
    )


def draw_pose(img, landmarks, mp_pose, highlight_joints=None):
    # TODO: сделать из сустава класс, также сделать из ребра класс.
    #  Для получения точек оформить конструктор из landmarks. Упростить
    #  "Отмеченные суставы", можно обойтись без повтора if (по факту там
    #  меняется только pt1 и color)

    # Основной скелет
    for edge in mp_pose.POSE_CONNECTIONS:
        joint_x0 = int(landmarks.landmark[edge[0]].x * img.shape[1])
        joint_y0 = int(landmarks.landmark[edge[0]].y * img.shape[0])
        joint_x1 = int(landmarks.landmark[edge[1]].x * img.shape[1])
        joint_y1 = int(landmarks.landmark[edge[1]].y * img.shape[0])

        cv2.line(img, (joint_x0, joint_y0), (joint_x1, joint_y1), Color.WHITE.value, 1)

        # Отмеченные суставы
        # Целевой сустав первый в edge
        if edge[0] in highlight_joints and edge[0] % 2 == edge[1] % 2:
            xm, ym = get_middle_coordinates(joint_x0, joint_y0, joint_x1, joint_y1)
            cv2.line(img, (joint_x0, joint_y0), (xm, ym), joint_to_color[edge[0]], 3)

        # Целевой сустав второй в edge
        if edge[1] in highlight_joints and edge[0] % 2 == edge[1] % 2:
            xm, ym = get_middle_coordinates(joint_x0, joint_y0, joint_x1, joint_y1)
            cv2.line(img, (joint_x1, joint_y1), (xm, ym), joint_to_color[edge[1]], 3)

    for i, joint in enumerate(landmarks.landmark):
        joint_x = int(joint.x * img.shape[1])
        joint_y = int(joint.y * img.shape[0])

        if i in highlight_joints:
            cv2.circle(img, (joint_x, joint_y), 4, joint_to_color[i], -1)
            continue

        cv2.circle(img, (joint_x, joint_y), 4, Color.ORANGE.value, -1)
