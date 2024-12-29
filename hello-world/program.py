import os

question_string = "Will you sign your life to Bill Gates? (\"yes\" or \"no\")\n"
result_string = ""
max_attempts = 5
attempts = 0
attempts_string = ""

while True:
    if attempts > 0:
        attempts_string = f"({attempts}/{max_attempts} chances)\n"
    
    if attempts > max_attempts:
        print("Burn in hell you babbling, retarded swine")
        input()
        break
        
    result_string = input(attempts_string + question_string)
    os.system("cls")
    match result_string: 
        case "yes":
            print("Yes you will.")
            input()
            break
        case "no":
            print("Burn in hell you ungrateful, unloyal servant.")
            input()
            break
        case _:
            attempts += 1
            continue
        
    