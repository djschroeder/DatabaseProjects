import display_user_details
import display_users
from utils import clear_console, press_any_key


def select_and_display_users(users):
    clear_console()
    if not users:
        print("No users found.")
        press_any_key()
        return

    while True:
        clear_console()
        display_users.display_users(users)

        try:
            selection = input(
                "Enter the number of the user to view details, or type 'back' to return: ").strip().lower()

            if selection == 'back':
                break

            selection = int(selection) - 1
            if 0 <= selection < len(users):
                clear_console()
                display_user_details.display_user_details(users[selection])
                input("\nPress Enter to return to the list...")
            else:
                clear_console()
                print("Invalid selection. Please enter a number from the list or type 'back' to return.")
                press_any_key()
        except ValueError:
            clear_console()
            print("Invalid input. Please enter a numerical value or type 'back'.")
            press_any_key()
