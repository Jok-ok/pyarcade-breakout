from enum import StrEnum


class AppPaths(StrEnum):
    NEAT_CONFIG_STANDARD_PATH = "NeatConf.txt"


class AppStrings(StrEnum):
    neat_breakout_title = "Breakout NEAT Algorithm"

    start_learning_button = "Начать обучение"
    load_generation_button = "Загрузить поколение"

    config_file_not_found = "Файл конфигурации не найден!"
    set_path_to_config_file = "Укажите путь к файлу конфигурации."

    loading_generation_file_error = "Ошибка загрузки файла чекпоинта."
    select_correct_generation_file = "Повторите попытку и выберите корректный файл чекпоинта."

    browse = "Обзор..."

    select_generation_checkpoint = "Выберите файл поколения"


class NeatConfigStrings(StrEnum):
    ...

# TODO: Подумать над шрифтами
