from colorama import Fore, Style
import colorama

colorama.init()

def bright(string):
    return Style.BRIGHT + string + Style.RESET_ALL

def light_white(string):
    return Fore.WHITE + string + Style.RESET_ALL

def cyan(string):
    return Fore.CYAN + string + Style.RESET_ALL

def green(string):
    return Fore.GREEN + string + Style.RESET_ALL

def light_green(string):
    return Fore.LIGHTGREEN_EX + string + Style.RESET_ALL

def light_red(string):
    return Fore.LIGHTRED_EX + string + Style.RESET_ALL

def light_magenta(string):
    return Fore.LIGHTMAGENTA_EX + string + Style.RESET_ALL

def light_yellow(string):
    return Fore.LIGHTYELLOW_EX + string + Style.RESET_ALL

