"""
    User Interface Modul
"""

import address_book
import os

"""
інтерфейс для спілкування з користувачем
якщо додається новий модуль, просто викликається метод call з класу в якому реалізована вся робота з даним модулем


"""




os.system("COLOR f0")



RED = "\033[91m"
GREEN = "\033[92m"
YELLOW="\033[93m"
RESET = "\033[0m"
BLUE = "\033[94m"
FLY_BLUE = "\033[38;5;117m"
PURPURE = "\033[35m"




def help_info():
    print(f'   list of comand:\n'
            f'- "contact" - Interacting with contacts.\n'
            f'- "exit" - exit of program\n'
          )

def start_bot():
    print(f'Hello! I`m your personal assistant! To finish working please enter "exit". To view all commands please enter "Help"')

    PROGRAM_STATUS = True

    while   PROGRAM_STATUS:
        data = input(f"> ").lower()
        if  data == "contact":
            if address_book.Address_book.call():
               PROGRAM_STATUS=False
        elif data == "help":
            help_info()
        elif data == "exit":
            break
        else:
          print(f"Command not found. The following command will 'help' you know what the commands are.")

if __name__ == "__main__":
    start_bot()