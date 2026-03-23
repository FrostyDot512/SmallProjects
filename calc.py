import math

# CALCULATOR - supports multiple numbers + math module operations

def Addition(*args):
    total = sum(args)
    print(f"Total sum: {total}")
    return total

def Multiplication(*args):
    total = 1
    for num in args:
        total *= num
    print(f"Total product: {total}")
    return total

def Subtraction(*args):
    # Subtracts all subsequent numbers from the first
    total = args[0] - sum(args[1:])
    print(f"Answer: {total}")
    return total

def Division(*args):
    # Divides the first number by all subsequent numbers
    total = args[0]
    for num in args[1:]:
        if num == 0:
            print("Error: Cannot divide by zero!")
            return None
        total /= num
    print(f"Answer: {total}")
    return total

# --- math module operations (single number) ---

def SquareRoot(num):
    if num < 0:
        print("Error: Cannot take square root of a negative number!")
        return None
    result = math.sqrt(num)
    print(f"Square root of {num}: {result}")
    return result

def Power(base, exp):
    result = math.pow(base, exp)
    print(f"{base} ^ {exp} = {result}")
    return result

def Logarithm(num, base=math.e):
    if num <= 0:
        print("Error: Logarithm only works on positive numbers!")
        return None
    result = math.log(num, base)
    base_label = "e" if base == math.e else base
    print(f"log_{base_label}({num}) = {result}")
    return result

def Factorial(num):
    if num < 0 or not isinstance(num, int):
        print("Error: Factorial only works on non-negative integers!")
        return None
    result = math.factorial(num)
    print(f"{num}! = {result}")
    return result

# --- get multiple numbers from user ---

def get_numbers():
    raw = input("Enter numbers separated by spaces: ")
    return [float(x) for x in raw.split()]

# --- main menu ---

def main():
    options = {
        "1": ("Addition",       Addition),
        "2": ("Multiplication", Multiplication),
        "3": ("Subtraction",    Subtraction),
        "4": ("Division",       Division),
        "5": ("Square Root",    None),
        "6": ("Power",          None),
        "7": ("Logarithm",      None),
        "8": ("Factorial",      None),
    }

    print("\n===== CALCULATOR =====")
    for key, (name, _) in options.items():
        print(f"  {key}. {name}")
    print("======================")

    choice = input("Choose an operation (1-8): ").strip()

    if choice in ("1", "2", "3", "4"):
        nums = get_numbers()
        options[choice][1](*nums)

    elif choice == "5":
        num = float(input("Enter a number: "))
        SquareRoot(num)

    elif choice == "6":
        base = float(input("Enter base: "))
        exp  = float(input("Enter exponent: "))
        Power(base, exp)

    elif choice == "7":
        num  = float(input("Enter number: "))
        base = input("Enter log base (press Enter for natural log): ").strip()
        Logarithm(num, float(base) if base else math.e)

    elif choice == "8":
        num = int(input("Enter a non-negative integer: "))
        Factorial(num)

    else:
        print("Invalid choice!")

main()
