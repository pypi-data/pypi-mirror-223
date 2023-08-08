import dis
class Token():
    def __init__(self, varType, line, variableName, varValue):
        self.varType = varType
        self.line = line  
        self.variableName = variableName
        self.varValue = varValue

def getAsciiValue(char):
    return ord(char)

def reportError(message):
    print(message)
    exit()

def keyWords():
    array = [
        "INT",
        "STR",
        "CHAR",
        "is",
        "and",
        "or",
        "not",
        "null"
    ]
    return array

def dis_function(variable_name, variable_value):
    variable_name = variable_value
    return variable_name

token_dictionary = {}
key_words_array = keyWords()
def evaluate(string, index):
    variableName = ""
    varType = ""
    varValue = ""
    for i in range(0, len(string)):
        if string[i:i+4] == "var ":
            array = string.split(" ")

            if str(array[1]) in key_words_array:
                reportError(f"Error:\nLine {index+1} | '{array[1]}' is a reserved word: please change variable name.")
                break

            elif not str(array[3]).__contains__(";") and str(array[3][0]).__eq__('"'):
                variableName += array[1]
                count = 3
                if getAsciiValue(str(array[count][0])) == 34:
                    varType += "STR"
                    varValue += array[count][1:]
                    count += 1
                    varValue += " "
                    while not str(array[count]).__contains__(";"):
                        varValue += array[count]
                        varValue += " "
                        count += 1
                    varValue += array[count].split('"')[0]
                    token = Token(varType, index+1, variableName, varValue)
                    token_dictionary[token.variableName] = [token.varType, token.line, token.variableName, token.varValue]
                    break
            elif str(array[3]).__contains__(";") and str(array[3][0]).__eq__('"'):
                varType += "STR"
                variableName += array[1]
                value = array[3].replace(";", "")
                varValue = value.replace('"', "")
                token = Token(varType, index+1, variableName, varValue)
                token_dictionary[token.variableName] = [token.varType, token.line, token.variableName, token.varValue]
                break
            else:
                varType += "INT"
                variableName += array[1]
                varValue += str(array[3]).replace(";", "")
                token = Token(varType, index+1, variableName, varValue)
                token_dictionary[token.variableName] = [token.varType, token.line, token.variableName, token.varValue]
                break

        elif string[i:i+4] == "viz ":
            viz_array = string.split(" ")
            variable = viz_array[1].replace(";", "")
            if variable in token_dictionary:
                print(f"Instructions for delcaring '{variable}':")
                print(f"\nStep 1\nWe first try to latch onto the name of the variable, and the value associated with it.")
                print("In the program I wrote, we do this by parsing tokens (characters in a program) and categorizing them into lexemes (groups of character types).")
                print("For example: the statement 'var variable = 5;' is actually read as:")
                print(" ___   ________   _   _   _")
                print("|var| |variable| |=| |5| |;|")
                print(" ---   --------   -   -   -")
                print("Where each part of the declaration statement is categorized in its own seperate 'lexeme'.")
                print(f"\nStep 2\nWe next check to make sure that '{variable}' is not in our reserved words array: {key_words_array}.")
                print("A reserved word in a programming language is a word that holds a specific meaning and purpose in the language's syntax and cannot be used as a regular identifier or variable name. These words are 'reserved' for special use cases and play critical roles in defining the language's structure and functionality.")
                print(f"Since '{variable}' is not in our reserved words, we store it in memory location {id(variable)} (Yes, this is the real memory address).")
                print(f"\nStep 3\nNext, we put '{variable}' in a dictionary as the key, and store attributes about this variable in an array. The attributes of this variable declaration are: data type, line number, variable name, and the actual value.")
                print(f"For example, the array stored in reference to '{variable}' is: {token_dictionary[variable]}.")
                print(f"In our case, we can see '{variable}' is stored as a '{token_dictionary[variable][0]}'.")
                print("*Note: even when we declare and integer, it's actually stored in the dictionary as a string. It's not until run-time that we will turn that string into an integer, at least in this language.")
                print("*Further about the string to int conversion - because Python is a dynamically typed language, the interpreter technically has to *interpret* what the data type of a variable is. That is why *compiled* languages, like C, are faster.")
                print("\nStep 4\nNow that the variable name is stored in the dictionary, with its value and other attribute data, the declaration process is complete.")
                print("**Please note** This is meant for learning, and this exact process will certain not hold true for every language, just for this specific language.")
            else:
                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")


        elif str(string[i:i+4]) == "h_by":
            array = string.split(" ")
            variable = array[1].replace(";", "")
            if variable in token_dictionary:
                print("\n")
                print(f"A look at the high-level bytecode for the variable declaration of '{variable}':")
                print("Line Number\tOpcode\t\t\tVariable Information")
                dis.dis(dis_function)
            else:
                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
            break

        elif str(string[i:i+4]) == "byte":
            array = string.split(" ")
            variable = array[1].replace(";", "")
            if variable in token_dictionary:
                print("\n")
                print(f"A look at the low-level bytecode for the variable declaration of {variable}:")
                print(dis_function.__code__.co_code)
                print("\n")
            else:
                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
            break

        elif string[i:i+4] == "out ":
            try:
                string = string.replace(";", "")
                array = string.split(" ")
                if len(array) == 2:
                    variable = array[1]
                    if variable in token_dictionary:
                        print(token_dictionary[variable][3])
                    else:
                        reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
                else:
                    if "+" in array:
                        variable = array[1]
                        if not variable.isdigit():
                            if variable in token_dictionary:
                                if array[3].isdigit():
                                    print(int(token_dictionary[variable][3]) + int(array[3]))
                                elif array[3] in token_dictionary:
                                    print(int(token_dictionary[variable][3]) + int(token_dictionary[array[3]][3]))
                                else:
                                    reportError(f"Error:\nLine {index+1} | Variable Error: '{array[3]}' is undefined.")

                            else:
                                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
                        else:
                            variable = array[3]
                            if variable in token_dictionary:
                                if array[1].isdigit():
                                    print(int(token_dictionary[variable][3]) + int(array[1]))
                                elif array[1] in token_dictionary:
                                    print(int(token_dictionary[variable][3]) + int(token_dictionary[array[1]][3]))
                                else:
                                    reportError(f"Error:\nLine {index+1} | Variable Error: '{array[1]}' is undefined.")

                            else:
                                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
                    elif "-" in array:
                        variable = array[1]
                        if not variable.isdigit():
                            if variable in token_dictionary:
                                if array[3].isdigit():
                                    print(int(token_dictionary[variable][3]) - int(array[3]))
                                elif array[3] in token_dictionary:
                                    print(int(token_dictionary[variable][3]) - int(token_dictionary[array[3]][3]))
                                else:
                                    reportError(f"Error:\nLine {index+1} | Variable Error: '{array[3]}' is undefined.")

                            else:
                                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
                        else:
                            variable = array[3]
                            if variable in token_dictionary:
                                if array[1].isdigit():
                                    print(int(array[1]) - int(token_dictionary[variable][3]))
                                elif array[1] in token_dictionary:
                                    print(int(int(token_dictionary[array[1]][3]) - token_dictionary[variable][3]))
                                else:
                                    reportError(f"Error:\nLine {index+1} | Variable Error: '{array[1]}' is undefined.")

                            else:
                                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
                    
                    elif "/" in array:
                        variable = array[1]
                        if not variable.isdigit():
                            if variable in token_dictionary:
                                if array[3].isdigit():
                                    print(int(token_dictionary[variable][3]) / int(array[3]))
                                elif array[3] in token_dictionary:
                                    print(int(token_dictionary[variable][3]) / int(token_dictionary[array[3]][3]))
                                else:
                                    reportError(f"Error:\nLine {index+1} | Variable Error: '{array[3]}' is undefined.")

                            else:
                                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
                        else:
                            variable = array[3]
                            if variable in token_dictionary:
                                if array[1].isdigit():
                                    print(int(array[1]) / int(token_dictionary[variable][3]))
                                elif array[1] in token_dictionary:
                                    print(int(int(token_dictionary[array[1]][3]) / token_dictionary[variable][3]))
                                else:
                                    reportError(f"Error:\nLine {index+1} | Variable Error: '{array[1]}' is undefined.")

                            else:
                                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")

                    elif "*" in array:
                        variable = array[1]
                        if not variable.isdigit():
                            if variable in token_dictionary:
                                if array[3].isdigit():
                                    print(int(token_dictionary[variable][3]) * int(array[3]))
                                elif array[3] in token_dictionary:
                                    print(int(token_dictionary[variable][3]) * int(token_dictionary[array[3]][3]))
                                else:
                                    reportError(f"Error:\nLine {index+1} | Variable Error: '{array[3]}' is undefined.")

                            else:
                                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
                        else:
                            variable = array[3]
                            if variable in token_dictionary:
                                if array[1].isdigit():
                                    print(int(array[1]) * int(token_dictionary[variable][3]))
                                elif array[1] in token_dictionary:
                                    print(int(int(token_dictionary[array[1]][3]) * token_dictionary[variable][3]))
                                else:
                                    reportError(f"Error:\nLine {index+1} | Variable Error: '{array[1]}' is undefined.")

                            else:
                                reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
                    

                    else:
                        variable = array[1]
                        if variable in token_dictionary:
                            print(int(token_dictionary[variable][3]))
                        else:
                            reportError(f"Error:\nLine {index+1} | Variable Error: '{variable}' is undefined.")
            except:
                reportError(f"Error:\nLine {index+1} | You are trying to perform a mathematical operation on data types that are invalid for this.")

            break
