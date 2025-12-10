from calculator_art import art
print(art)

def add(num1, num2):
    return num1 + num2

def sub(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2

operations= {
    "+": add,
    "-": sub,
    "*": multiply,
    "/": divide
}

def calculator():
    print(art)
    first_number = int(input("What is the first number: "))
    continue_calculating = True
    while continue_calculating:
        for operation in operations:
            print(operation)
        choose_operation = input("Pick an operation: ")
        second_number = int(input("What is the next number: "))

        if choose_operation in operations:
            result = operations[choose_operation](first_number, second_number)
            print(f"{first_number} {choose_operation} {second_number} = {result}")
            other_choice = input(f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation: ")
            if other_choice == 'y':
                first_number = result
            else:
                print("\n" * 100)
                calculator() #Recursion


calculator()




