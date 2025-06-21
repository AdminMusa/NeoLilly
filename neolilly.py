import pyuac
import sys
import requests
from colorama import init, Fore, Style
from bs4 import BeautifulSoup
import webbrowser
import msvcrt
import os
import subprocess

# Initialize colorama
init(autoreset=True)

prompt_main_color = Fore.MAGENTA
prompt_symbol_color = Fore.CYAN
text_color = Fore.LIGHTMAGENTA_EX
avacmd = Fore.LIGHTBLUE_EX

def proces():
    while True:
        neocommand = input(
            prompt_main_color + "neoLilly" +
            prompt_symbol_color + "$ " +
            Style.RESET_ALL
        )

        if neocommand.lower() == "exit":
            print(Fore.YELLOW + "Disconnecting from NeoLilly... ")
            break

        elif neocommand.lower() == "copywrite":
            print(text_color + "Copyright 2025")
            print(text_color + "All rights to Muhammad Musa")

        elif neocommand.lower().startswith("del "):
            file_to_delete = neocommand[4:].strip()
            if file_to_delete == "":
                print(Fore.RED + "Invalid command syntax. Please include a file to delete.")
            else:
                try:
                    os.remove(file_to_delete)
                    print(f"File {file_to_delete} deleted.")
                except FileNotFoundError:
                    print("File not found.")
                except PermissionError:
                    print("Permission denied.")

        elif neocommand.lower() == "balls":
            while True:
                print("Come WASH MY BALLS")

        elif neocommand.lower() == "help":
            print(avacmd + "Commands: exit, lookup, copywrite, help, neopt, read, clear, del, balls, neoinfo wifipwsd")

        elif neocommand.lower() == "wifipwsd":
            get_wifi_passwords()

        elif neocommand.lower() == "lookup":
            query = input("Search for: ")
            ext_choice = input("Open in external browser? (yes/no): ").lower()

            if ext_choice == "yes":
                url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                print(Fore.GREEN + "Opened in browser.")
            else:
                url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    results = soup.find_all("a", class_="result__a")

                    if results:
                        print(Fore.GREEN + f"Top {min(5, len(results))} results:")
                        for result in results[:5]:
                            print(Fore.CYAN + result.get_text())
                            print(Fore.LIGHTBLACK_EX + result['href'])
                            print(Fore.WHITE + "—" * 40)
                    else:
                        print(Fore.RED + "No results found.")
                else:
                    print(Fore.RED + f"Failed to fetch page. Status code: {response.status_code}")

        elif neocommand.lower() == "neopt":
            neopt()

        elif neocommand.lower().startswith("read"):
            parts = neocommand.split()
            if len(parts) == 2:
                filename = parts[1]
            else:
                filename = input("Enter file to read: ")

            try:
                with open(filename, "r", encoding="utf-8") as file:
                    content = file.read()
                    print(Fore.LIGHTWHITE_EX + "\nFile Contents:\n" + Fore.GREEN + content)
            except FileNotFoundError:
                print(Fore.RED + "File not found.")

        elif neocommand.lower() == "clear":
            os.system("cls" if os.name == "nt" else "clear")

        elif neocommand.lower() == "":
            print("")
        elif neocommand.lower() == "neoinfo":
            get_system_info()

        else:
            print(Fore.RED + f"Unknown command: {neocommand}")


def get_system_info():
    try:
        os_version = os.popen('ver').read().strip()

        cpu_raw = os.popen('wmic cpu get name').read().splitlines()
        cpu = [line.strip() for line in cpu_raw if line.strip() and "Name" not in line][0]

        ram_raw = os.popen('wmic computersystem get TotalPhysicalMemory').read().splitlines()
        ram_line = [line.strip() for line in ram_raw if line.strip() and "TotalPhysicalMemory" not in line][0]
        ram_gb = round(int(ram_line) / (1024 ** 3), 1)

        print(Fore.BLUE + f"OS: {os_version}")
        print(Fore.BLUE + f"CPU: {cpu}")
        print(Fore.BLUE + f"RAM: {ram_gb} GB")

    except Exception as e:
        print(Fore.RED + f"Error fetching system info: {e}")


def get_wifi_passwords():
    try:
        profiles = subprocess.check_output(
            ["netsh", "wlan", "show", "profiles"]
        ).decode("utf-8", errors="ignore")

        for line in profiles.split("\n"):
            if "All User Profile" in line:
                ssid = line.split(":")[1].strip()
                password_info = subprocess.check_output(
                    ["netsh", "wlan", "show", "profile", ssid, "key=clear"]
                ).decode("utf-8", errors="ignore")

                if "Key Content" in password_info:
                    password = password_info.split("Key Content")[1].split("\n")[0].split(":")[1].strip()
                else:
                    password = "None Saved"

                print(Fore.GREEN + f"SSID: {ssid}")
                print(Fore.GREEN + f"Password: {password}")
                print(Fore.WHITE + "—" * 40)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def neopt():
    print(Fore.YELLOW + "NeoText Editor (type your text below)")
    print(Fore.YELLOW + "Press Ctrl+X to exit and save.")

    neopt_lines = []
    line = ""

    while True:
        char = msvcrt.getwch()

        if char == '\r':
            print()
            neopt_lines.append(line)
            line = ""

        elif ord(char) == 24:
            print(Fore.YELLOW + "\nCtrl+X detected. Exiting editor.")
            break

        elif ord(char) == 8:
            if len(line) > 0:
                line = line[:-1]
                print('\b \b', end='', flush=True)

        else:
            line += char
            print(char, end='', flush=True)

    choice = input(Fore.YELLOW + "\nSave this file? (yes/no): ").lower()
    if choice == "yes":
        filename = input(Fore.YELLOW + "Enter filename (with .neopt or .txt): ")
        with open(filename, "w", encoding="utf-8") as f:
            for l in neopt_lines:
                f.write(l + "\n")
        print(Fore.YELLOW + f"File saved as {filename}")
    else:
        print(Fore.RED + "File discarded.")

def main():
    print(Fore.LIGHTMAGENTA_EX + "Welcome to NeoLilly ")
    print(Fore.YELLOW + "Copyright 2025")
    input(Fore.LIGHTCYAN_EX + "All rights to Muhammad Musa. Press enter to continue...")
    proces()

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        sys.exit()
    else:
        main()
