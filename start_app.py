from tkinter import Tk
from customtkinter import (set_appearance_mode, set_default_color_theme, CTkLabel,
                           CTkEntry, CTkFrame, CTkButton, CTkInputDialog)
from app_consts import AppStrings

set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
class AppScreen(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title_label = CTkLabel(self, text=AppStrings.neat_breakout_title)
        self.start_learning_button = CTkButton(self, text=AppStrings.start_learning_button)
        self.configures_button = CTkButton(self, text=AppStrings.configure_settings_button)
        self.load_generation_button = CTkButton(self, text=AppStrings.load_generation_button)

        self.grid_gui()

        self.mainloop()

    def grid_gui(self):
        self.title_label.grid(row=0, column=0)
        self.start_learning_button.grid(row=1, column=0)
        self.configures_button.grid(row=2, column=0)
        self.load_generation_button.grid(row=3, column=0)

if __name__ == "__main__":
    app = AppScreen()