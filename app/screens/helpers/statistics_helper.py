from db.schemas import GraphData
from enums import ExerciseType

exercise_types = [
    ["Отведение правой руки", ExerciseType.RIGHT_SHOULDER_ABDUCTION.value],
    ["Отведение левой руки", ExerciseType.LEFT_SHOULDER_ABDUCTION.value],
    ["Приседания", ExerciseType.KNEE_BEND.value],
    ["Наклон вперёд", ExerciseType.LEANING_FORWARD.value],
]


def get_dynamic(data) -> str:
    overall_dynamics = 0

    data = data[(len(data) - 5) : len(data)]  # берём последние 5 элементов массива
    for i in range(1, len(data)):
        if data[i].max_angle > data[i - 1].max_angle:
            overall_dynamics += 1
        if data[i].max_angle < data[i - 1].max_angle:
            overall_dynamics -= 1

        if data[i].avg_speed > data[i - 1].avg_speed:
            overall_dynamics += 1
        if data[i].avg_speed < data[i - 1].avg_speed:
            overall_dynamics -= 1

    if overall_dynamics > 0:
        return "положительная"
    elif overall_dynamics < 0:
        return "отрицательная"
    else:
        return "—"


def get_graph_data(exercise_data, exercise_num) -> GraphData:
    graph_data = GraphData(angle=[], speed=[], date=[])
    for session_info in exercise_data[exercise_num]:
        graph_data.angle.append(session_info.max_angle)
        graph_data.speed.append(session_info.avg_speed)
        graph_data.date.append(session_info.finished_at.strftime("%Y-%m-%d"))

    return graph_data
