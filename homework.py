class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_M: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        information: InfoMessage = InfoMessage(
            self.__class__.__name__, self.duration, self.get_distance(),
            self.get_mean_speed(), self.get_spent_calories())
        return information


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Расчет калорий при занятии бегом."""
        mean_speed_run: float = super().get_mean_speed()
        calories_consumed_run: float = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed_run
             + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
            / self.M_IN_KM * (self.duration
                              * self.H_IN_M))
        return calories_consumed_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SPEED_RATIO_M_IN_KM: float = 0.278
    HEIGHT_RATIO_CM_IN_M: int = 100
    CALORIES_WEIGHT_MULTIPLIER_1: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2: float = 0.029

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет калорий при занятии спортивной ходьбой."""
        mean_speed_in_m_walk: float = (super().get_mean_speed()
                                       * self.SPEED_RATIO_M_IN_KM)
        height_in_m: float = self.height / self.HEIGHT_RATIO_CM_IN_M
        calories_consumed_walk: float = (
            (self.CALORIES_WEIGHT_MULTIPLIER_1 * self.weight
             + (mean_speed_in_m_walk**2 / height_in_m)
             * self.CALORIES_WEIGHT_MULTIPLIER_2 * self.weight)
            * (self.duration * self.H_IN_M))
        return calories_consumed_walk


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed_swim: float = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)
        return mean_speed_swim

    def get_spent_calories(self) -> float:
        """Расчет калорий при занятии плаванием."""
        colories_consumed_swim: float = (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight * self.duration)
        return colories_consumed_swim


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainig_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in trainig_types:
        training: Training = trainig_types[workout_type](*data)
    else:
        print("Error!")
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
