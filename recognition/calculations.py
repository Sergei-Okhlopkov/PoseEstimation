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


# TODO: сделать из нескольких функций расчёта углов одну, в которую передаётся параметр
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

        return [r_shoulder_angle, l_shoulder_angle]
    else:
        return [-1, -1]


def get_elbows_angles(landmarks, revert=False):
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

        if revert:
            r_elbow_angle = 180 - r_elbow_angle
            l_elbow_angle = 180 - l_elbow_angle

        return [r_elbow_angle, l_elbow_angle]
    else:
        return [-1, -1]


def get_hips_angles(landmarks, revert=False):
    if landmarks:
        right_hip = [
            landmarks.landmark[12],
            landmarks.landmark[24],
            landmarks.landmark[26],
        ]

        left_hip = [
            landmarks.landmark[11],
            landmarks.landmark[23],
            landmarks.landmark[25],
        ]

        r_hip_angle = int(get_angle(right_hip))
        l_hip_angle = int(get_angle(left_hip))

        if revert:
            r_hip_angle = 180 - r_hip_angle
            l_hip_angle = 180 - l_hip_angle

        return [r_hip_angle, l_hip_angle]
    else:
        return [-1, -1]


def get_knees_angles(landmarks, revert=True):
    if landmarks:
        right_knee = [
            landmarks.landmark[24],
            landmarks.landmark[26],
            landmarks.landmark[28],
        ]

        left_knee = [
            landmarks.landmark[23],
            landmarks.landmark[25],
            landmarks.landmark[27],
        ]

        r_knee_angle = int(get_angle(right_knee))
        l_knee_angle = int(get_angle(left_knee))

        if revert:
            r_knee_angle = 180 - r_knee_angle
            l_knee_angle = 180 - l_knee_angle

        return [r_knee_angle, l_knee_angle]
    else:
        return [-1, -1]


def get_middle_coordinates(x0, y0, x1, y1):
    xm = int((x0 + x1) / 2)
    ym = int((y0 + y1) / 2)
    return xm, ym
