import sys
import re

operations = {}
history = []
operation_pattern = '(?P<Operation>^[\\w?]+)\\s*(?P<Args>[\\d\\.\\s]+)?'
operation_match = re.compile(operation_pattern)

class HistoryObject():
    def __init__(self, operation, args, result):
        self.operation = operation
        self.args = args
        self.result = result
    def __str__(self):
        return 'Operation "' + str(self.operation) + '" was called with [' + str(' '.join(self.args)) + '] as args with result of ' + str(self.result)

def main():
    global history
    print "Enter operations as such operation num1 num2 num3 ....."
    print "Use '?' to list availible operations"
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
        operation = result.group('Operation')
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

def call_operation(operation, args):
    global operations
    if operation in operations.keys():
        result = operations[operation](args)
        history.append(HistoryObject(operation, args, result))
        if result is not None:
            print(result)
    else:
        raise ParseError('There is no operation with that name, use \'?\' to list operations')

def add_operation(op_name, function_pointer):
    global operations
    operations[op_name] = function_pointer

# exit or quit
def exit(args):
    sys.exit()
add_operation('exit', exit)
add_operation('quit', exit)

def list_operations(args):
    print
    print 'Operations\n-------------------'
    for k, v in operations.iteritems():
        print k
    print '-------------------'
add_operation('?', list_operations)

# add a1 a2 a3 a4
def add(args):
    value = 0
    for arg in args:
        try:
            addTo = float(arg)
            value += addTo
        except ValueError:
            raise ParseError('Value provided was no an int or float')
    return value
add_operation('add', add)

def print_history(args):
    item = 1
    for v in history:
        print str(item) + '. ' + str(v)
        item+=1
add_operation('history', print_history)

def clear_history(args):
    global history
    history = []
add_operation('clear_history', clear_history)

def clear_screen(args):


main()
