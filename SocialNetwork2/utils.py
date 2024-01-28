import os
import platform


def clear_console():
    # Clear console command depending on the operating system
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Linux and Mac
        os.system('clear')


def press_any_key():
    input("\nPress enter to continue...")


def validate_empty_input(user_input):
    if user_input == "":
        clear_console()
        print("Input cannot be empty.")
        press_any_key()
        return False
    return True


def draw_options(options):
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    user_input = input("\nEnter your choice: ")
    return user_input


def validate_user_input(user_input, options):
    clear_console()

    choice = validate_is_digit(user_input)

    if not choice:
        return None

    if choice < 1 or choice > len(options):
        print("Invalid input. Please enter a valid choice.")
        press_any_key()
        return None

    return choice


def validate_is_digit(user_input):
    if not user_input.isdigit():
        print("Invalid input. Please enter a numerical value.")
        press_any_key()
        return None
    validated_input = int(user_input)

    return validated_input
