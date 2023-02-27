from typing import Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration} ч.; '
                    'Дистанция: {distance} км; '
                    'Ср. скорость: {speed} км/ч; '
                    'Потрачено ккал: {calories}.')

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывести информацию сообщение с информацией о тренировке."""
        return self.MESSAGE.format(
            training_type=self.training_type,
            duration=format(self.duration, ".3f"),
            distance=format(self.distance, ".3f"),
            speed=format(self.speed, ".3f"),
            calories=format(self.calories, ".3f")
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        distance: float = self.get_distance()
        speed: float = distance / self.duration
        return speed

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в '
                                  f'"{self.__class__.__name__}"')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        training_type: str = self.__class__.__name__
        return InfoMessage(training_type, self.duration,
                           distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed: float = self.get_mean_speed()
        duration_minutes: float = self.duration * self.MINUTES_IN_HOUR
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                           + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                           / self.M_IN_KM * duration_minutes)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SPEED_TO_M_IN_SEC: float = 0.278
    SM_IN_M: int = 100
    WEIGHT_FACTOR: float = 0.035
    SPEED_AND_WEIGHT_FACTOR: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed: float = self.get_mean_speed()
        speed_m_in_sec: float = speed * self.SPEED_TO_M_IN_SEC
        duration_minutes: float = self.duration * self.MINUTES_IN_HOUR
        height_m: float = self.height / self.SM_IN_M
        calories: float = ((self.WEIGHT_FACTOR * self.weight
                           + (speed_m_in_sec ** 2 / height_m)
                           * self.SPEED_AND_WEIGHT_FACTOR
                           * self.weight) * duration_minutes)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SPEED_FACTOR: float = 1.1
    SPEED_MULTIPIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed: float = self.get_mean_speed()
        calories: float = ((speed + self.SPEED_FACTOR)
                           * self.SPEED_MULTIPIER * self.weight
                           * self.duration)
        return calories


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    try:
        training_type = training_types[workout_type]
    except KeyError:
        raise KeyError(f'<нет тренировки с кодом: "{workout_type}">')
    return training_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
