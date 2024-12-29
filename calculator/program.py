from os import system
from enum import Enum

class OperationType(Enum):
    Non = -1
    Addition = 0
    Subtraction = 1
    Multiplication = 2
    Division = 3
    Exponent = 4
    OpenSeperator = 5
    CloseSeperator = 6
class NumberToken:
    def __init__(self, value, operation, pa_order):
        operation_order_map = { 
                 OperationType.Addition       : 0,
                 OperationType.Subtraction    : 0,
                 OperationType.Multiplication : 1, 
                 OperationType.Division       : 1,
                 OperationType.Exponent       : 2, 
                 OperationType.OpenSeperator  : 0,
                 OperationType.CloseSeperator : 0,
        }
        
        self.value = value
        self.operation = operation
        self.operation_order = operation_order_map[operation]
        self.parenthesis_order = pa_order
    def __eq__(self, value):
        if isinstance(self, value):
            same_value = self.value == value.value
            same_op = self.operation == value.operation
            same_op_order = self.operation_order == value.operation_order
            same_pa_order = self.parenthesis_order == value.parenthesis_order
            return same_value and same_op and same_op_order and same_pa_order
        return False
    def __str__(self):
        value_strings = []
        value_strings.append(f"Value: {self.value}")
        value_strings.append(f"Operation: {self.operation}")
        value_strings.append(f"Operation Order: {self.operation_order}")
        value_strings.append(f"Parenthesis Order: {self.parenthesis_order}")
        
        total_string = "Number values:\n"
        for value_string in value_strings:
            total_string += "    " + value_string + '\n'
        return total_string
class NumberTreeNode:
    def __init__(self, parent_node, value, operation):
        self.parent_node = parent_node
        self.child_nodes = []
        self.value = value
        self.operation = operation
    def get_value(self):
        if len(self.child_nodes) > 0:
            self.value = 0
            for child_node in self.child_nodes:
                match child_node.operation:
                    case OperationType.Addition:
                        self.value += child_node.get_value()
                    case OperationType.Subtraction:
                        self.value -= child_node.get_value()
                    case OperationType.Multiplication:
                        self.value *= child_node.get_value()
                    case OperationType.Division:
                        self.value /= child_node.get_value()
                    case OperationType.Exponent:
                        self.value **= child_node.get_value()
                
        return self.value
    def append_child(self, value, operation):
        child_node = NumberTreeNode(self, value, operation)
        self.child_nodes.append(child_node)
        return child_node
    
def detect_operation_by_tokens(string, index):
    token_map = { 
                 "("  : OperationType.OpenSeperator,
                 ")"  : OperationType.CloseSeperator,
                 "**" : OperationType.Exponent, 
                 "*"  : OperationType.Multiplication, 
                 "/"  : OperationType.Division,
                 "+"  : OperationType.Addition, 
                 "-"  : OperationType.Subtraction
                 }
    
    for token in token_map:
        if string.find(token, index, index + len(token)) == index:
            return token_map[token]
    
    return OperationType.Non
def tokenize_string(string):
    value = 0
    operation = OperationType.Addition
    parenthesis_order = 0
    number_detected = False
    
    tokenized_result = []
    index = 0
    while index < len(string):
        detected_operation = detect_operation_by_tokens(string, index)
        
        if detected_operation == OperationType.Non:
            if string[index].isdecimal():
                    start_index = index
                    end_index = index + 1
                    value_string = ""
                    trust_me_bro = False
                    
                    while end_index < len(string):
                        value_char = string[end_index]
                        
                        if value_char.isdecimal():
                            trust_me_bro = False
                            end_index += 1
                        elif value_char == '.' and not trust_me_bro:
                            trust_me_bro = True
                            end_index += 1
                        else:
                            if trust_me_bro:
                                end_index -= 1
                            break
                    
                    value_string = string[start_index:end_index]
                    value = float(value_string)
                    number_detected = True
                    index = end_index
            else:
                index += 1
        elif detected_operation == OperationType.OpenSeperator:
            parenthesis_order += 1
            index += 1
        elif detected_operation == OperationType.CloseSeperator:
            parenthesis_order -= 1
            index += 1
        else:
            operation = detected_operation
            if operation == OperationType.Exponent:
                index += 1
            index += 1
                   
        if number_detected:
            tokenized_result.append(NumberToken(value, operation, parenthesis_order))
            number_detected = False
    
    return tokenized_result
def graph_tokens(tokens):
    root_node = NumberTreeNode(None, 0, OperationType.Addition)
    
    pa_order_diff = 0
    op_order_diff = 0
    current_root_node = root_node
    index = 0
    
    paren_node_map = {0 : (None, 0)}
    
    while index < len(tokens): # For allen in the future, i dont know what this does either
        prev_token = tokens[max(index - 1, 0)]
        curr_token = tokens[index]
        next_token = tokens[min(index + 1, len(tokens) - 1)]
        
        pa_order_diff = (curr_token.parenthesis_order - prev_token.parenthesis_order) * 3
        if next_token.parenthesis_order < curr_token.parenthesis_order:
            op_order_diff = 0
        else:
            op_order_diff = next_token.operation_order - curr_token.operation_order
        entering_parenthesis = False
        exiting_parenthesis = False
        
        if pa_order_diff > 0: # Entering the parenthesis
            paren_node_map[curr_token.parenthesis_order] = (current_root_node, curr_token.operation_order)
            op_order_diff = 0
            
            already_set = False
            while pa_order_diff > 0:
                if not already_set:
                    current_root_node = current_root_node.append_child(0, curr_token.operation)
                    already_set = True
                else:
                    current_root_node = current_root_node.append_child(0, OperationType.Addition)

                pa_order_diff -= 1
                
            entering_parenthesis = True
        elif pa_order_diff < 0: # Getting out the parenthesis
            while pa_order_diff < 0:
                current_root_node = current_root_node.parent_node
                pa_order_diff += 1
                
            op_order_diff = curr_token.operation_order - paren_node_map[prev_token.parenthesis_order][1]
            exiting_parenthesis = True
            #continue
        elif pa_order_diff == 0: # Stay where you are
            pass
        
        if op_order_diff > 0: # Need to go deeper in the tree
            if exiting_parenthesis:
                bingus = current_root_node
                while op_order_diff > 0:
                    last_child_index = len(bingus.child_nodes) - 1
                    bingus = bingus.child_nodes[last_child_index]
                    op_order_diff -= 1
                bingus.append_child(curr_token.value, curr_token.operation)
                current_root_node = paren_node_map[prev_token.parenthesis_order][0]
            else:
                already_set = False
                while op_order_diff > 0:
                    if not already_set:
                        current_root_node = current_root_node.append_child(0, curr_token.operation)
                        already_set = True
                    else:
                        current_root_node = current_root_node.append_child(0, OperationType.Addition)
                    op_order_diff -= 1
                current_root_node.append_child(curr_token.value, OperationType.Addition)
        elif op_order_diff < 0: # Need to go closer to the root
            while op_order_diff < 0:
                current_root_node = current_root_node.parent_node
                op_order_diff += 1
            current_root_node.append_child(curr_token.value, curr_token.operation)
        elif op_order_diff == 0: # Stay where you are
            if entering_parenthesis:
                current_root_node.append_child(curr_token.value, OperationType.Addition)
            else:
                current_root_node.append_child(curr_token.value, curr_token.operation)
        
        index += 1
    
    return root_node
def print_tree(root_node, depth):
    print("    " * depth + f"      - Value: {root_node.value}, Operation: {root_node.operation}")
    for child_node in root_node.child_nodes:
        print_tree(child_node, depth + 1)

state = 0
state_names = [
    "1. Calculate",
    "2. Test calculations",
    "3. About",
    "4. Exit"
]
while True:
    system("cls")
    match state:
        case 0:
            print("CALCULATOR: First python project!")
            for state_name in state_names:
                print(f"    --- {state_name}")
            
            answer = input("\n> ")
            if answer.isnumeric():
                state = int(answer[0])
        case 1:
            print("CALCULATOR: Calculating...")
            print("    --- Type \"exit\" to go back")
            
            equation_string = ""
            while True:
                equation_string = input("\n> ")
                if equation_string == "exit":
                    break
                
                tokens = tokenize_string(equation_string)
                tree_graph = graph_tokens(tokens)
                print(tree_graph.get_value())
                
            state = 0
        case 2:
            print("CALCULATOR: Testing calculations...")
            print_token = False
            print_graph = True
            equation_strings = [
                "1 + 8 / (3 - 1) ** 41 + 8 / (3 - 1) ** 4",
                "1 + 8 ** (3 - 1) / 4",
                "1 + 6 / (3 - 1) ** 2",
                "1 + 3 + 2 + 4" 
            ]
            
            max_width = 0
            for equation_string in equation_strings:
                max_width = max(max_width, len(equation_string) + 4)

            for equation_string in equation_strings:
                tokens = tokenize_string(equation_string)
                tree_graph = graph_tokens(tokens)
                displayed_string = f"[ {equation_string} ]"
                print(f"    ---{"-" * (max_width - len(displayed_string)) } {displayed_string} => {tree_graph.get_value()}")
                
                if print_token:
                    print("        Tokens:")
                    for token in tokens:
                        print("          - Token:")
                        print(f"            --- Value: {token.value}")
                        print(f"            --- Operation: {token.operation}")
                        print(f"            --- Operation Order: {token.operation_order}")
                        print(f"            --- Parenthesis Order: {token.parenthesis_order}")
                if print_graph: 
                    print("        Tree Graph:")
                    print_tree(tree_graph, 0)
            
            input("\n> ")
            state = 0
        case 3:
            print("CALCULATOR: About this project")
            print("    --- CREATOR: Seirge Allen")
            print("    --- PROJECT CREATED: December 26, 2024 - 5:09:18 PM")
            print("    --- PROJECT DURATION: ~3 days\n")
            
            print("    This was a really fun project to work on.")
            print("    I feel i learned the basics of the Python syntax,")
            print("    and solved some hard problems on the way!")
            input("\n> ")
            state = 0
        case 4:
            break
        case _:
            state = 0
    
    

#result_string = input("Type an equation to calculate: ")

#tokens = tokenize_string(result_string)

#print_tree(tree_graph, 0)
#print(f"Result: {tree_graph.get_value()}")
