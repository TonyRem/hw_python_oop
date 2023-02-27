class InfoMessage:
    """Информационное сообщение о тренировке."""
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
        formatted_duration: str = format(self.duration, ".3f")
        formatted_distance: str = format(self.distance, ".3f")
        formatted_speed: str = format(self.speed, ".3f")
        formatted_calories: str = format(self.calories, ".3f")
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {formatted_duration} ч.; '
                f'Дистанция: {formatted_distance} км; '
                f'Ср. скорость: {formatted_speed} км/ч; '
                f'Потрачено ккал: {formatted_calories}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES_IN_HOUR = 60

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
        pass

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
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        speed: float = self.get_mean_speed()
        duration_minutes: float = self.duration * self.MINUTES_IN_HOUR
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                           + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                           / self.M_IN_KM * duration_minutes)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SPEED_TO_M_IN_SEC = 0.278
    SM_IN_M = 100
    FIRST_CALORIES_WEIGHT_MULTIPLIER = 0.035
    SECOND_CALORIES_WEIGHT_MULTIPLIER = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed: float = self.get_mean_speed()
        speed_m_in_sec: float = speed * self.SPEED_TO_M_IN_SEC
        duration_minutes: float = self.duration * self.MINUTES_IN_HOUR
        height_m: float = self.height / self.SM_IN_M
        calories: float = ((self.FIRST_CALORIES_WEIGHT_MULTIPLIER * self.weight
                           + (speed_m_in_sec ** 2 / height_m)
                           * self.SECOND_CALORIES_WEIGHT_MULTIPLIER
                           * self.weight) * duration_minutes)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    FIRST_CALORIES_CONST = 1.1
    SECOND_CALORIES_CONST = 2

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
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        speed: float = self.get_mean_speed()
        calories: float = ((speed + self.FIRST_CALORIES_CONST)
                           * self.SECOND_CALORIES_CONST * self.weight
                           * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    TrainingType = training_types[workout_type]
    return TrainingType(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    result: str = info.get_message()
    print(result)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
        except KeyError:
            print(f'<нет тренировки с кодом: "{workout_type}">')
            continue
        main(training)
