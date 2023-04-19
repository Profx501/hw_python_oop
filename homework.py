from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывод сообщения на экран."""
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    TIME_IN_MINUTES = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self. weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка:бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration
                * self.TIME_IN_MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    ATHLETE_WEIGHT_MULTIPLIER = 0.035
    SPEED_AND_GROWTH_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    SM_IN_M = 100

    def __init__(self, action, duration, weight, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Считает количество затраченных калорий."""
        result_conversion: float = self.get_mean_speed() * self.KMH_IN_MSEC
        result_conversion_2: float = self.height / self.SM_IN_M
        return ((self.ATHLETE_WEIGHT_MULTIPLIER * self.weight
                + (result_conversion**2
                 / result_conversion_2)
                * self.SPEED_AND_GROWTH_MULTIPLIER
                * self.weight) * self.duration
                * self.TIME_IN_MINUTES)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
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

    def get_mean_speed(self) -> float:
        """Считает скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Считает количество затраченных калорий."""
        average_speed = self.get_mean_speed()
        return ((average_speed + self.BIAS_VALUE)
                * self.SPEED_MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_code: dict[str, type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking
                                               }
    if workout_type not in workout_code.keys():
        raise ValueError("Код тренировки не соответствует.")
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
