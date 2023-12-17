from enum import StrEnum


class AppPaths(StrEnum):
    NEAT_CONFIG_STANDARD_PATH = "NeatConf.txt"


class AppStrings(StrEnum):
    neat_breakout_title = "Breakout NEAT Algorithm"

    start_learning_button = "Начать обучение"
    load_generation_button = "Загрузить поколение"
    configure_settings_button = "Настроить параметры"

    config_file_not_found = "Файл конфигурации не найден!"
    set_path_to_config_file = "Укажите путь к файлу конфигурации."


class NeatConfigStrings(StrEnum):
    ...


# TODO: Подумать над шрифтами