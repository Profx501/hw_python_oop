class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывод сообщения на экран."""
        message: str = (f"Тип тренировки: {self.training_type}; "
                        f"Длительность: {self.duration:.3f} ч.; "
                        f"Дистанция: {self.distance:.3f} км; "
                        f"Ср. скорость: {self.speed:.3f} км/ч; "
                        f"Потрачено ккал: {self.calories:.3f}.")
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Расстояние, которое спортсмен преодолевает за один Шаг.
    M_IN_KM = 1000  # Для перевода значений из метров в километры.
    TIME_IN_MINUTES = 60  # Для перевода времени тренировки в минуты.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self. weight = weight
        self.type_training: str = ""

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.type_training,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка:бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # Коэффициент.
    CALORIES_MEAN_SPEED_SHIFT = 1.79  # Коэффициент.

    def __init__(self, action, duration, weight) -> None:
        super().__init__(action, duration, weight)
        self.type_training: str = "Running"

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight / self.M_IN_KM * self.duration
                           * self.TIME_IN_MINUTES)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    ATHLETE_WEIGHT_MULTIPLIER = 0.035  # Коэффициент.
    SPEED_AND_GROWTH_MULTIPLIER = 0.029  # Коэффициент.
    CONVERSION = 0.278  # Км/ч в м/c.
    CONVERSION_2 = 100  # См. в м.

    def __init__(self, action, duration, weight, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.type_training = "SportsWalking"

    def get_spent_calories(self) -> float:
        """Считает количество затраченных калорий."""
        result_conversion: float = self.get_mean_speed() * self.CONVERSION
        result_conversion_2: float = self.height / self.CONVERSION_2
        calories: float = ((self.ATHLETE_WEIGHT_MULTIPLIER * self.weight
                           + (result_conversion**2
                            / result_conversion_2)
                           * self.SPEED_AND_GROWTH_MULTIPLIER
                           * self.weight) * self.duration
                           * self.TIME_IN_MINUTES)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # Расстояние за один гребок.
    BIAS_VALUE = 1.1
    SPEED_MULTIPLIER = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.type_training = "Swimming"

    def get_mean_speed(self) -> float:
        """Считает скорость движения."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Считает количество затраченных калорий."""
        average_speed = self.get_mean_speed()
        calories: float = ((average_speed + self.BIAS_VALUE)
                           * self.SPEED_MULTIPLIER * self.weight
                           * self.duration)
        return calories


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_code: dict[str, type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking
                                               }
    if workout_type in workout_code.keys():
        return workout_code[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
