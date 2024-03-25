import cv2
from enums import Color

joint_to_color = {11: Color.BLUE.value,         # Правое плечо
                  12: Color.DODGER_BLUE.value,  # Левое плечо
                  13: Color.CHARTREUSE.value,   # Правый локоть
                  14: Color.GREEN.value,        # Левый локоть
                  15: Color.RED.value,          # Правый кулак
                  16: Color.ROSE.value,          # Левый кулак
                  23: Color.VIOLET.value,       # Правое бедро
                  24: Color.PURPLE.value,       # Левое бедро
                  25: Color.YELLOW.value,       # Правое колено
                  26: Color.CYAN.value,         # Левое колено
                  27: Color.SPRING_GREEN.value, # Правая лодыжка
                  28: Color.MAGENTA.value       # Левая лодыжка
                  }

landMarksStatic = [(15, 21),    # Правый кулак - правый большой палец
                   (16, 20),    # Левый кулак - левый указательный палец
                   (18, 20),    # Левый мизинец - левый указательный палец
                   (3, 7),      # Правый глаз внеш. - правое ухо
                   (14, 16),    # Левый локоть - левый кулак
                   (23, 25),    # Правое бедро - правое колено
                   (28, 30),    # Левая лодыжка - левая пятка
                   (11, 23),    # Правое плечо - правое бедро
                   (27, 31),    # Правая лодыжка - правый указательный палец ноги
                   (6, 8),      # Левый глаз внеш. - левое ухо
                   (15, 17),    # Правый кулак - костяшка правого мизинца
                   (24, 26),    # Левое бедро - левое колено
                   (16, 22),    # Левый кулак - левая костяшка большого пальца
                   (4, 5),      # Левый глаз внутр. - левый глаз
                   (5, 6),      # Левый глаз - левый глаз внеш.
                   (29, 31),    # Правая лодыжка - правый указательный палец ноги
                   (12, 24),    # Левое плечо - левое бедро
                   (23, 24),    # Правое бедро - левое бедро
                   (0, 1),      # Нос - правый глаз внутр.
                   (9, 10),     # Губы право - губы лево
                   (1, 2),      # Правый глаз внутр. - правый глаз
                   (0, 4),      # Нос - левый глаз внутр.
                   (11, 13),    # Правое плечо - левое плечо
                   (30, 32),    # Левая пятка - левый указательный палец ноги
                   (28, 32),    # Левая лодыжка - левый указательный палец ноги
                   (15, 19),    # Правый кулак - правая костяшка указательного пальца
                   (16, 18),    # Левый кулак - левая костяшка мизинца
                   (25, 27),    # Правое колено - правая лодыжка
                   (26, 28),    # Левое колено - левая лодыжка
                   (12, 14),    # Левое плечо - левый локоть
                   (17, 19),    # Правая костяшка мизинца - правая костяшка указательного пальца
                   (2, 3),      # Правый глаз - правый глаз внеш.
                   (11, 12),    # Правое плечо - левое плечо
                   (27, 29),    # Правая лодыжка - правая пятка
                   (13, 15)     # Правый локоть - правый КУЛАК
                   ]


def draw_info(img, fps, angles, r_arm_speed):
    cv2.rectangle(img, (0, 0), (100, 200), Color.GREY.value, -1)
    cv2.putText(img, str(int(fps)), (30, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 0), 3)

    cv2.putText(img,
                str(angles[0]),
                (30, 100),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                Color.RED.value,
                3)

    cv2.putText(img,
                str(r_arm_speed),
                (200, 100),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                Color.VIOLET.value,
                3)

    cv2.putText(img,
                str(angles[1]),
                (30, 150),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                Color.GREEN.value,
                3)


def draw_pose(img, landmarks, mp_pose, highlight_joints=None):
    for edge in mp_pose.POSE_CONNECTIONS:
        joint_x0 = int(landmarks.landmark[edge[0]].x * img.shape[1])
        joint_y0 = int(landmarks.landmark[edge[0]].y * img.shape[0])
        joint_x1 = int(landmarks.landmark[edge[1]].x * img.shape[1])
        joint_y1 = int(landmarks.landmark[edge[1]].y * img.shape[0])

        cv2.line(img, (joint_x0, joint_y0), (joint_x1, joint_y1),
                 Color.BLUE.value, 2)

    for i, joint in enumerate(landmarks.landmark):
        joint_x = int(joint.x * img.shape[1])
        joint_y = int(joint.y * img.shape[0])

        if i in highlight_joints:
            cv2.circle(img, (joint_x, joint_y), 6, joint_to_color[i], -1)
            continue

        cv2.circle(img, (joint_x, joint_y), 6, Color.ORANGE.value, -1)

