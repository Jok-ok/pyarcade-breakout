from main import run_generation

if __name__ == "__main__":
    generation_num = input("Введите номер поколения для запуска: ")
    generation_num = int(generation_num)
    run_generation(generation_num)