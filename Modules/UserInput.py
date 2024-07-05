def input_alternative(message, alternatives):
    while True:
        choice = input(message)
        if choice in alternatives:
            return choice

def input_integer(message):
    while True:
        try:
            number = int(input(message))
            return number
        except ValueError:
            print("Input an integer.")

def input_float(message):
    while True:
        try:
            number = float(input(message))
            return number
        except ValueError:
            print("Input float.")
   
def input_percentage(message):
    while True:
        try:
            number = float(input(message))
            return number / 100
        except ValueError:
            print("Input percentage.")