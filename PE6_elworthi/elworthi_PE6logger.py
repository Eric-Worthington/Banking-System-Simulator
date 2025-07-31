# Eric Worthington, CIS345, A3

import random

def create_pin():
    attempts = 0
    while attempts < 3:
        try:
            print("You have 3 tires to enter a number between 1 and 9999 as your pin.")
            print("If you didn't reset your pin after 3 tries, the system will create a pin for you.")
            pin = int(input("Select a number between 1 and 9999 as your pin: "))
            if 1 <= pin <= 9999:
                return pin
            else:
                raise ValueError("Pin needs to be an integer between 1 and 9999.")
        except ValueError as ex:
            attempts += 1
            print(f"\nInvalid pin. Attempt {attempts} of 3.")

    print("The system will create a pin randomly for you.")
    pin = random.randint(1,9999)
    print(f"Your pin is: {pin}")
    return pin