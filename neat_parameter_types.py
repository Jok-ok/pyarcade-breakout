from typing import Protocol, Optional

import neat
from neat.config import Config


class NeatParameter(Protocol):
    """Протокол для всех видов параметров файла конфигурации NEAT"""
    name: str
    description: str
    value: Optional[object]


class NeatBasicParameter:
    """
    Базовый класс параметра файла конфигурации NEAT
    """

    def __init__(self, name: str, description: str, value: Optional[object]):
        """
        Базовый конструктор
        :param name: имя параметра
        :param description: описание параметра
        :param value: установленное значение параметра
        """
        self.name = name
        self.description = description
        self.value = value


class NeatBoolParameter(NeatBasicParameter):
    """
    Класс булевого параметра файла конфигурации NEAT
    """

    def __init__(self, name: str, description: str, value: bool):
        """
        Конструктор
        :param name: имя параметра
        :param description: описание параметра
        :param value: установленное значение параметра
        :type value: bool
        """
        super().__init__(name, description, value)
        if type(value) is not bool:
            raise TypeError


class NeatMultipleValuesParameter(NeatBasicParameter):
    """
    Класс параметра с несколькими возмодными значениями файла конфигурации NEAT
    """

    def __init__(self, name: str, description: str, values_list: Optional[list[str]], cases_list: Optional[list[str]]):
        """

        :param name: имя параметра
        :param description: описание параметра
        :param values_list: список выбранных значений параметра
        :param cases_list: список возможных значений параметра
        """
        super().__init__(name, description, values_list)
        self.cases_list = cases_list


class NeatComboboxParameter(NeatBasicParameter):
    """
    Класс параметра с выбором из нескольких параметров файла конфигурации NEAT
    """

    def __init__(self, name: str, description: str, value: str, cases_list: Optional[list[str]]):
        """
        Конструктор
        :param name: имя параметра
        :param description: описание параметра
        :param value: значение параметра
        :param cases_list: список возможных значений параметра
        """
        super().__init__(name, description, value)
        self.cases_list = cases_list


class NeatIntParameter(NeatBasicParameter):
    """
    Класс целочисленного параметра конфигурации NEAT
    """

    def __init__(self, name: str, description: str, value: int):
        """
        Конструктор
        :param name: имя параметра
        :param description: описание параметра
        :param value: установленное значение параметра
        :type value: int
        """
        super().__init__(name, description, value)


class NeatFloatParameter(NeatBasicParameter):
    """
    Класс вещественного параметра файла конфигурации NEAT
    """

    def __init__(self, name: str, description: str, value: float):
        """
        Конструктор
        :param name: имя параметра
        :param description: описание параметра
        :param value: установленное значение параметра
        :type value: float
        """
        super().__init__(name, description, value)


class ParameterSection:
    """
    Класс секции параметров конфигурации NEAT
    """

    def __init__(self, section_name, parameters: list[NeatParameter], description: str):
        """
        Конструктор
        :param section_name: название секции
        :param parameters: список параметров секции
        :param description: описание секции
        """
        self.section_name = section_name
        self.parameters = parameters
        self.description = description


class NeatConfiguration:
    def __init__(self, sections: list[ParameterSection]):
        self.sections = sections


def get_standard_neat_configuration(conf: Config) -> NeatConfiguration:
    # genome_config: neat.genome.DefaultGenomeConfig = conf.genome_config
    # genome_config._params
    # genome_config
    neat_config_params = conf.__params # Короче где-то тут лежит список параметров этой пиздоблядской либы, которые один господб знает как парсить

    neat_section_parameters = [
        NeatComboboxParameter("fitness_criterion",
                              "Критерий выбора наиболее успешного генома по значению фитнесс функции.",
                              "max",
                              ["min", "mean", "max"]),
        NeatFloatParameter("fitness_threshold",
                           "Значение фитнесс функции при котором поиск решения завершается и "
                           "найденное решение считается оптимальным",
                           2500),
        NeatBoolParameter("no_fitness_termination",
                          "Если установлено в True, то параметры fitness_criterion и fitness_threshold "
                          "будут игнорироваться. Поиск решения завершится если будет достигнуто максимальное "
                          "число поколений",
                          False),
        NeatIntParameter("pop_size",
                         "Размер популяции",
                         20),
        NeatBoolParameter("reset_on_extinction",
                          "Если установлено в true, то когда все виды вымрут из-за застоя, то будет создана"
                          " новая случайная популяция. Если False, то в данном случае будет выбрашено исключение "
                          "CompleteExtinctionException",
                          True)
    ]

    neat_section = ParameterSection("NEAT",
                                    neat_section_parameters,
                                    "Обязательный раздел. "
                                    "Содержит основные параметры алгоритма NEAT")

    default_stagnation_section_parameters = []
    default_stagnation_section = ParameterSection()

    default_reproduction_section_parameters = []
    default_reproduction_section = ParameterSection()

    default_species_set_section_parameters = []
    default_species_set_section = ParameterSection()

    default_genome_section_parameters = []
    default_genome_section = ParameterSection()

    configuration = NeatConfiguration([neat_section,
                                       default_stagnation_section,
                                       default_reproduction_section,
                                       default_species_set_section,
                                       default_genome_section])

    return configuration
