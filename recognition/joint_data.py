from enums import Color

highlited_joints = [11, 12, 13, 14, 23, 24, 25, 26, 27, 28]

joint_to_color = {
    11: Color.BLUE.value,  # Правое плечо
    12: Color.BLUE.value,  # Левое плечо
    13: Color.GREEN.value,  # Правый локоть
    14: Color.GREEN.value,  # Левый локоть
    15: Color.RED.value,  # Правый кулак
    16: Color.ROSE.value,  # Левый кулак
    23: Color.VIOLET.value,  # Правое бедро
    24: Color.VIOLET.value,  # Левое бедро
    25: Color.CYAN.value,  # Правое колено
    26: Color.CYAN.value,  # Левое колено
    27: Color.RED.value,  # Правая лодыжка
    28: Color.RED.value,  # Левая лодыжка
}

landMarkEdges = [
    (15, 21),  # Правый кулак - правый большой палец
    (16, 20),  # Левый кулак - левый указательный палец
    (18, 20),  # Левый мизинец - левый указательный палец
    (3, 7),  # Правый глаз внеш. - правое ухо
    (14, 16),  # Левый локоть - левый кулак
    (23, 25),  # Правое бедро - правое колено
    (28, 30),  # Левая лодыжка - левая пятка
    (11, 23),  # Правое плечо - правое бедро
    (27, 31),  # Правая лодыжка - правый указательный палец ноги
    (6, 8),  # Левый глаз внеш. - левое ухо
    (15, 17),  # Правый кулак - костяшка правого мизинца
    (24, 26),  # Левое бедро - левое колено
    (16, 22),  # Левый кулак - левая костяшка большого пальца
    (4, 5),  # Левый глаз внутр. - левый глаз
    (5, 6),  # Левый глаз - левый глаз внеш.
    (29, 31),  # Правая лодыжка - правый указательный палец ноги
    (12, 24),  # Левое плечо - левое бедро
    (23, 24),  # Правое бедро - левое бедро
    (0, 1),  # Нос - правый глаз внутр.
    (9, 10),  # Губы право - губы лево
    (1, 2),  # Правый глаз внутр. - правый глаз
    (0, 4),  # Нос - левый глаз внутр.
    (11, 13),  # Правое плечо - левое плечо
    (30, 32),  # Левая пятка - левый указательный палец ноги
    (28, 32),  # Левая лодыжка - левый указательный палец ноги
    (15, 19),  # Правый кулак - правая костяшка указательного пальца
    (16, 18),  # Левый кулак - левая костяшка мизинца
    (25, 27),  # Правое колено - правая лодыжка
    (26, 28),  # Левое колено - левая лодыжка
    (12, 14),  # Левое плечо - левый локоть
    (17, 19),  # Правая костяшка мизинца - правая костяшка указательного пальца
    (2, 3),  # Правый глаз - правый глаз внеш.
    (11, 12),  # Правое плечо - левое плечо
    (27, 29),  # Правая лодыжка - правая пятка
    (13, 15),  # Правый локоть - правый КУЛАК
]
