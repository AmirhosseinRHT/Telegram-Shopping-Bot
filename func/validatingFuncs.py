import os , re

def validate_age(age : str):
    if age.isdigit():
        if 11< int(age) <= 90:
            return True
    return False

def validate_phone_number(number : str):
    if not number[1:].isdigit():
        return False
    if len(number) != 11:
        if len(number) != 13:
            return False
    if number[:2] != "09":
        if number[:4] != "+989":
            return False
    return True


def is_sqlite_file(file_path):
    if not os.path.isfile(file_path):
        return False
    with open(file_path, "rb") as file:
        header = file.read(16)
    return header[:6] == b"SQLite"  

def check_given_link_is_valid(string : str):
    if len(string) <= 3:
        return False
    if not string.startswith('https://t.me/') and not string.startswith('@'):
        return False
    if string.count('@') != 1:
        return False
    if not re.match("^[a-zA-Z0-9]+$", string):
        return False
    return True