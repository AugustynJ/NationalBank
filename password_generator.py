import random
import string

def getStrongPassword(length: int):
    if type(length) != int:
        raise ValueError("Parametr 'length' must be integeer")
    elif length < 12 or length > 128:
        raise ValueError("Password length must be between 12 and 128 letters length!")
    
    lower = list(string.ascii_lowercase)
    upper = list(string.ascii_uppercase)
    digits = list(string.digits)
    symbol = list(string.punctuation)

    random.shuffle(lower)
    random.shuffle(upper)
    random.shuffle(digits)
    random.shuffle(symbol)

    # lower = 35% of pssword length
    # upper = 30% of passwrd length
    # digits = 20% of password length
    # symbol = 15% of passwod length

    result = []
    for i in range (round(0.35*length)):
        result.append(lower[i%len(lower)])

    for i in range (round(0.3*length)):
        result.append(upper[i%len(upper)])

    for i in range (round(0.2*length)):
        result.append(digits[i%len(digits)])

    for i in range (round(0.15*length)):
        result.append(symbol[i%len(symbol)])
    
    random.shuffle(result)

    return "".join(result)[:length]