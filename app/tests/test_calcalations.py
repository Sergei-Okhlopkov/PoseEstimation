from collections import namedtuple
import cv2

from recognition.calculations import get_angle
from recognition.pose_recognition import recognize_pose

Landmark = namedtuple("Landmark", ["x", "y"])


def test_get_angle():
    landmarks = []
    landmarks.append(Landmark(x=0, y=0))
    landmarks.append(Landmark(x=0, y=3))
    landmarks.append(Landmark(x=3, y=0))

    result = int(get_angle(landmarks))
    expected = 45

    assert result == expected


def test_recognize_pose_success():
    result = False
    expected = True
    img = cv2.imread("images_for_tests/test_1.jpg")
    pose = recognize_pose(img)

    if pose.pose_landmarks:
        result = True

    assert result == expected


def test_recognize_pose_no_pose():
    result = False
    expected = False
    img = cv2.imread("images_for_tests/test_2.jpg")
    pose = recognize_pose(img)

    if pose.pose_landmarks:
        result = True

    assert result == expected
