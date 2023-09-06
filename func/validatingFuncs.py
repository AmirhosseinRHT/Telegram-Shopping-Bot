def validate_age(age : str):
    if age.isdigit():
        if 18 <= int(age) <= 99:
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