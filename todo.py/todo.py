#!/usr/bin/env python3

# TODO +tag @context/location/project 
# TODO !/!!/!!! priority levels
# TODO a "shell" function that keeps you in the program anduses os.clear and whatever to cls

import sys

def load_from_file():
    """ Loads the todo.txt file into memory and returns a list """
    
    try:
        with open('todo.txt') as todo_file:
            return todo_file.readlines()
    except FileNotFoundError:
        return []

def write_to_file(todo_list):
    """ Writes the todo list to a text file"""
    
    todo_list = sort_todo_list(todo_list)
    
    # TODO test this by raising an error 
    
    try:
        with open('todo.txt', 'w') as todo_file:
            todo_file.writelines(todo_list)
    except Exception as e:
        print(type(e), "Unexpected Error: Terminating Program")
        sys.exit()

def print_todo(todo_list):
    """ Prints the todo list to the console """
    
    todo_list = sort_todo_list(todo_list)
    
    i = 1
    
    for item in todo_list:
        print(i, "\t", item, end="")
        i += 1

def read_args():
    """ Get the arguments from the command line and perform appropriate tasks"""
    
    todo_list = load_from_file()
    
    # Get only relevant arguments (no file name)
    str_args = ' '.join(sys.argv[1:])
    
    
    if len(sys.argv) == 1:
        if len(todo_list) == 0:
            print("No TODO Items!")
        else:
            print_todo(todo_list)
    else:
        if str_args.startswith('del'): # TODO consider regex for getting numbers?
            todo_list = del_todo(todo_list, str_args[4:]) 
            print_todo(todo_list)
        elif str_args.startswith('urg'):
            todo_list = mark_task(todo_list, str_args[4:], "!")
            print_todo(todo_list)
        elif str_args.startswith('edit'):
            pass
        elif str_args.startswith('list'):
            if len(todo_list) == 0:
                print('You have no todo items!')
            else:
                print_todo(todo_list)
        elif str_args.startswith('move'): # TODO bettername?
            todo_list = mark_task(todo_list, str_args[5:], ">") 
            print_todo(todo_list)
        elif str_args.startswith('done'): # TODO better name?
            todo_list = mark_task(todo_list, str_args[5:], "X")
            print_todo(todo_list)
        else: # assume that no argument means to add a task
            str_args += "\n"
            todo_list = add_todo(todo_list, str_args)
            print_todo(todo_list)

def add_todo(todo_list, todo_item):
    """ Adds the todo item to the list of tasks and writes to file"""
    
    todo_list.append(todo_item)
    write_to_file(todo_list)
    
    return todo_list
    

def edit_todo(todo_list, task_number):
    """ """
    pass

def del_todo(todo_list, task_number):
    """ Removes the given task from the list and writes to disk """
    # TODO make a done-todo fn that either doesn't print done tasks or moves to todo_done file
    
    try:
        task_number = int(task_number)
        
        if task_number > len(todo_list):
            print("That task does not exist.")
            return todo_list
        
        del(todo_list[task_number-1])
        write_to_file(todo_list)

        return todo_list
    except ValueError: #TODO test this function
        print("Please enter valid number.")
        return todo_list
    
def sort_todo_list(todo_list):
    """ Returns a sorted todo list: urgent tasks, normal, delayed, completed.  """
    
    # TODO we can otherwise remove from todo list, but must make iterate through a copy of the list
    # TODO find a more efficient way of doing this?
    # perhaps make a copy of todo list and then remove the items from it, pass it to the next for?

    sorted_list = []
    
    for item in todo_list:
        if item.startswith('!'):
            sorted_list.append(item)
            
    for item in todo_list:
        if item not in sorted_list and (not item.startswith('X')) and (not item.startswith('>')):
            sorted_list.append(item)

    for item in todo_list:
        if item not in sorted_list and (not item.startswith('X')):
            sorted_list.append(item)
    
    for item in todo_list:
        if item.startswith('X'):
            sorted_list.append(item)
            
    return sorted_list


def mark_task(todo_list, task_number, mark):
    """ Marks the given todo_list item !urgent >delayed Xcompleted """

    try: 
        task_number = int(task_number)
        
        if task_number > len(todo_list):
            print("That task does not exist.")
            return todo_list
        
        # Clear previous mark if present
        if todo_list[task_number-1][0] in "X!>":
            todo_list[task_number-1] = todo_list[task_number-1][2:]
        # Append new mark
        todo_list[task_number-1] = mark + " " + todo_list[task_number-1] 
        write_to_file(todo_list)

        return todo_list

    except ValueError: #TODO test this function
        print("Please enter valid number.")
        return todo_list

if __name__ == "__main__":

    print("Commands are 'move' 'del' 'urg' 'done'") 
    read_args()
