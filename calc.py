import sys
import os
import re

operations = {}
history = []
operation_pattern = '(?P<Operation>^[\\w?]+)\\s*(?P<Args>[\\.\\s\\w\\$]*\\S)?(?:\\s*)'
operation_match = re.compile(operation_pattern)

class HistoryObject():
    def __init__(self, operation, args, result):
        self.operation = operation
        self.args = args
        self.result = result
    def __str__(self):
        return 'Operation "' + str(self.operation) + '" was called with [' + str(' '.join(self.args)) + '] as args with result of ' + str(self.result)

class Operation():
    def __init__(self, operation_name, function, helptext, save_history):
        self.operation_name = operation_name
        self.function = function
        self.helptext = helptext
        self.save_history = save_history
    def __str__(self):
        return str(self.operation_name)

def main():
    global history
    print "Enter operations as such 'operation param1 param2 param3 .....'"
    print "Use '?' to list availible operations"
    print "Use $n to replace an argument with the result from the n-th history item"
    while(True):
        try:
            user_input = raw_input()
            operation, args = parse(user_input)
            result = call_operation(operation, args)
        except ParseError as pe:
            print pe.value

def parse(raw):
    global operation_match
    result = operation_match.match(raw)
    args = []
    try:
        operation = result.group('Operation').lower()
    except IndexError:
        raise ParseError('There is no operation listed')
    try:
        args_inside = result.group('Args')
        if args_inside is not None:
            args = re.split('\s+', args_inside)
    except IndexError:
        pass
    return (operation, args)

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def replace_args(args):
    if args is None:
        return None
    return_args = []
    for arg in args:
        result = re.match('\$(\d+)' ,arg)
        if result:
            value = result.group(1)
            try:
                return_args.append(history[int(value)-1].result)
            except IndexError:
                raise ParseError('No history object at position $' + value)
        else:
            return_args.append(arg)
    return return_args

def call_operation(operation, args):
    global operations
    args = replace_args(args)
    if operation in operations.keys():
        op = operations[operation]
        result = op.function(args)
        if op.save_history:
            history.append(HistoryObject(operation, args, result))
        if result is not None:
            print(result)
    else:
        raise ParseError('There is no operation with that name, use \'?\' to list operations')

def add_operation(op_name, function_pointer, helptext="No set help text", save_history=True):
    global operations
    operations[op_name] = Operation(op_name, function_pointer, helptext, save_history)

def exit(args):
    sys.exit()
add_operation('exit', exit, helptext="Closes the program")
add_operation('quit', exit, helptext="Closes the program")

def list_operations(args):
    if args is not None and len(args) > 0 and args[0] is not None and args[0] in operations.keys():
        print operations[args[0]].helptext
    else:
        print
        print 'Operations\n-------------------'
        for k, v in operations.iteritems():
            print k
        print '-------------------'
        print "Use '? operation' to get more details for an operation"
add_operation('?', list_operations, helptext="Use without params to list all operations, with a single param to get details about an operation, ignores additional params", save_history=False)


def print_history(args):
    item = 1
    if len(history) == 0:
        print 'You have no history yet'
        return
    for v in history:
        print str(item) + '. ' + str(v)
        item+=1
    print "Use $n to replace an argument with the result from the n-th history item"
add_operation('hist', print_history, helptext="History: Lists the history, ignores arguments", save_history=False)

def clear_history(args):
    global history
    history = []
add_operation('clh', clear_history, helptext="Clear history: Clears out your history and saved results", save_history=False)

def clear_screen(args):
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system('clear')
    elif sys.platform == "win32":
        os.system('cls')
    else:
        print("Can't clear screen on your os type")
add_operation('clear', clear_screen, helptext="Clears the screen", save_history=False)
add_operation('cls', clear_screen, helptext="Clears the screen", save_history=False)
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
def check_args(args):
    if len(args) < 2:
        raise ParseError("At least 2 params need to be passed to this operation")

def add(args):
    check_args(args)
    value = 0
    for arg in args:
        try:
            arg_value = float(arg)
            value += arg_value
        except ValueError:
            raise ParseError('Value provided was not an int or float')
    return value
add_operation('add', add, helptext="Adds the list of params together, only accepts floats and ints")

def sub(args):
    check_args(args)
    value = 0
    first = True
    for arg in args:
        try:
            arg_value = float(arg)
            if first:
                first = False
                value += arg_value
            else:
                value -= arg_value
        except ValueError:
            raise ParseError('Value provided was not an int or float')
    return value
add_operation('sub', sub, helptext="Subtracts params 2..n from the 1st param")

def mul(args):
    check_args(args)
    value = 1
    for arg in args:
        try:
            arg_value = float(arg)
            value = value * arg_value
        except ValueError:
            raise ParseError('Value provided was not an int or float')
    return value
add_operation('mul', mul, helptext="Multiples the list of params together")

def div(args):
    check_args(args)
    value = 0
    first = True
    for arg in args:
        try:
            arg_value = float(arg)
            if first:
                first = False
                value = arg_value
            else:
                if arg_value == 0:
                    raise ParseError("Can't divide by zero")
                value = value / arg_value
        except ValueError:
            raise ParseError('Value provided was not an int or float')
    return value
add_operation('div', div, helptext="Divides params 2..n from the 1st param")

main()
