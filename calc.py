# Were going to code a SIMPLE CALCULATOR USING ONLY 2 PARAMETERS

def Addtion():
    num1 = int(input("Enter number 1: "))
    num2 = int(input("Enter Number 2: "))
    total = num1 + num2
    print("Total sum: ",total)

def Multiplication():
    num1 = int(input("Enter number 1: "))
    num2 = int(input("Enter number 2: "))
    total = num1 * num2
    print("Total Sum {}".format(total))

def Subtraction():
    num1 = int(input("Enter number 1: "))
    num2 = int(input("Enter number 2: "))
    question = input("Do you want to subtract the first value from second? ")
    if question.lower() == 'yes':
        answer = num1 - num2
        print(f"Answer: {answer}")
    else:
        answer = num2 - num1
        print(f"Answer: {answer}")
    
def Division():
    num1 = int(input("Enter number 1: "))
    num2 = int(input("Enter number 2: "))
    question = input("Do you want to subtract the first value from second? ")
    if question.lowercase() == 'yes':
        answer = num1 // num2
        print(f"Answer: {answer}")
    else:
        answer = num2 // num1
        print(f"Answer: {answer}")


print(Subtraction())
        




