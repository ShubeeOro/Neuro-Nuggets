import re

def valid_password(password) -> bool:
    flag = False
    if not isinstance(password, str):
        raise ValueError
    while True:
        if (len(password)<=8):
            flag = True
            break
        elif not re.search("[a-z]", password):
            flag = True
            break
        elif not re.search("[A-Z]", password):
            flag = True
            break
        elif not re.search("[0-9]", password):
            flag = True
            break
        elif not re.search("[!_#@$%^&*?<>~]" , password):
            flag = True
            break
        else:
            break
    if flag:
        return False
    else:
        return True