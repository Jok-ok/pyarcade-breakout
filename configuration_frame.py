import neat
from customtkinter import CTkFrame
from tkinter import messagebox
from neat.config import Config
from neat import DefaultGenome, DefaultStagnation, DefaultReproduction, DefaultSpeciesSet
from os.path import exists, isfile
from app_consts import AppPaths, AppStrings
from tkinter.filedialog import askopenfilename
from neat_parameter_types import get_standard_neat_configuration


class ConfigurationFrame(CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            configurator = NeatConfigurator(AppPaths.NEAT_CONFIG_STANDARD_PATH)
        except Exception:
            messagebox.showerror(AppStrings.config_file_not_found, AppStrings.set_path_to_config_file)
            configurator = self.ask_neat_file()

        self.neat_configuration = get_standard_neat_configuration(configurator.neat_config)


    def ask_neat_file(self) -> str:
        return askopenfilename("txt")


class NeatConfigurator:
    def __init__(self, neat_config_path: str):
        self.neat_config = Config(DefaultGenome,
                                  DefaultReproduction,
                                  DefaultSpeciesSet,
                                  DefaultStagnation,
                                  neat_config_path)





