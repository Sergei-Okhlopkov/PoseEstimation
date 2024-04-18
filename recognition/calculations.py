import numpy as np


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


def get_shoulders_angles(landmarks):
    if landmarks:
        right_shoulder = [
            landmarks.landmark[14],
            landmarks.landmark[12],
            landmarks.landmark[24],
        ]

        left_shoulder = [
            landmarks.landmark[13],
            landmarks.landmark[11],
            landmarks.landmark[23],
        ]

        r_shoulder_angle = int(get_angle(right_shoulder))
        l_shoulder_angle = int(get_angle(left_shoulder))
        # r_shoulder_angle = round(get_angle(right_shoulder), 1)
        # l_shoulder_angle = round(get_angle(left_shoulder), 1)

        return [r_shoulder_angle, l_shoulder_angle]
    else:
        return [-1, -1]


def get_elbows_angles(landmarks):
    if landmarks:
        right_elbow = [
            landmarks.landmark[16],
            landmarks.landmark[14],
            landmarks.landmark[12],
        ]

        left_elbow = [
            landmarks.landmark[15],
            landmarks.landmark[13],
            landmarks.landmark[11],
        ]

        r_elbow_angle = int(get_angle(right_elbow))
        l_elbow_angle = int(get_angle(left_elbow))

        return [r_elbow_angle, l_elbow_angle]
    else:
        return [-1, -1]


def get_middle_coordinates(x0, y0, x1, y1):
    xm = int((x0 + x1) / 2)
    ym = int((y0 + y1) / 2)
    return xm, ym
