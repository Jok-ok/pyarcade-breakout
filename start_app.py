from tkinter import Tk
from customtkinter import (set_appearance_mode, set_default_color_theme, CTkLabel,
                           CTkButton)
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from app_consts import AppStrings
from sources.main import run_generation_checkpoint, run
from os.path import abspath
from os import getcwd

set_appearance_mode("Dark")
set_default_color_theme("green")


class AppScreen(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("NEAT")
        self.title_label = CTkLabel(self, text=AppStrings.neat_breakout_title, text_color="black",
                                    font=("Roboto", 24, "bold"))
        self.start_learning_button = CTkButton(self, text=AppStrings.start_learning_button, width=300,
                                               command=self.start_learning)
        self.load_generation_button = CTkButton(self, text=AppStrings.load_generation_button, width=300,
                                                command=self.load_generation)
        self.current_sources_path = abspath(getcwd())

        self.grid_gui()

        self.mainloop()

    def grid_gui(self):
        self.title_label.grid(row=0, column=0, padx=10, pady=10)
        self.start_learning_button.grid(row=1, column=0, padx=10, pady=10)
        self.load_generation_button.grid(row=2, column=0, padx=10, pady=10)

    def load_generation(self):
        file_name = askopenfilename(defaultextension="", title=AppStrings.select_generation_checkpoint,
                                    initialdir=self.current_sources_path, filetypes=(("NONE", "*"),))
        try:
            run_generation_checkpoint(file_name)

        except Exception:
            showerror(title=AppStrings.loading_generation_file_error, message=AppStrings.select_correct_generation_file)

    def start_learning(self):
        config_path = askopenfilename(defaultextension=".txt", title=AppStrings.set_path_to_config_file,
                                      initialdir=self.current_sources_path, filetypes=(("TXT", "*.txt"),))

        try:
            run(config_path)

        except Exception:
            showerror(title=AppStrings.config_file_not_found, message=AppStrings.set_path_to_config_file)



if __name__ == "__main__":
    app = AppScreen()
