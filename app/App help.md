
# Справка по переменным
## <span style="color:#2285B2">Videoplayer.py</span>
- **video_tool_stripe**: панель с кнопками упарвления видео 
- **callbacks**: словарь с функциями для отрисовки актуальной информации в интерфейсе
- **capture**: в эту переменную идёт захват видеопотока
- **elbows_angles**: текущий угол сиба локтей (сначала идёт угол для правой руки, затем для левой)
- **shoulders_angles**: текущий угол сиба в плечевом суставе (сначала идёт угол для правой руки, затем для левой)
- **значения с префиксом _prev__**: значения переменной в предыдущий момент времени
- **shouders_speed / elbows_speed**: скорость движения конечности, угол/секунду
- **collected_speed**: в этот кортеж суммируется скорость конечности в каждый момент времени

Главное действо происходит в функции update_video. Она рекурсивно запущена при создании класса


# Отображение окна "Просмотр пациента" врача
- ФИО пациента
- id пациента
- дата последнего занятия
- динамика занятий (за последние 5 дней)
- График занятий (в масштабе отображаются последние 7 занятий, остальные нужно листать). На
графике отображается две зависимости: макс. угол от занятий и средняя скорость от занятий
- выпадающий список упражнений для отображения статистики
- Текстовое поле с комментарием (если есть)
- Кнопка сохранения комментария
