import pandas as pd
import re

contacts = {"John": "123-456-7890",
            "Alice": "987-654-3210",
            "Bob": "555-555-5555"
            }
QUIT_COMMANDS = ("good bye", "close", "exit")


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError as e:
            return e
        except IndexError:
            return None, "Wrong number of parameters, please check your input"
        except TypeError as e:
            return None, e

    return wrapper


def hello(*args):
    return "How can I help you?"


@input_error
def add_contact(name, phone):
    validate_name_and_phone(name, phone)
    if name in contacts:
        raise KeyError(f"{name} already is in contacts. If you want to make changes to the record,"
                       f" use 'change [name] [phone]' command instead")

    contacts[name] = phone
    return f"{name}'s phone has been added to contacts"


@input_error
def change_contact(name, phone):
    validate_name_and_phone(name, phone)
    if name in contacts:
        contacts[name] = phone
        return f"{name}'s phone has been changed in contacts"
    else:
        raise KeyError("Sorry, there's no such record, enter another name or check your spelling")


def name_is_valid(name):
    # more complicated check will be realized if needed
    return re.match('[a-zA-Z]', name)


def phone_is_valid(phone: str):
    # more complicated check will be realized if needed
    return not phone.isalpha()


def validate_name_and_phone(name, phone):
    if not name_is_valid(name):
        raise TypeError("Please enter a proper name")
    if not phone_is_valid(phone):
        raise TypeError("Please enter a valid phone number")


@input_error
def get_phone(name):
    if name not in contacts:
        return TypeError("Sorry, there's no such record, enter another name or check your spelling")
    return f"{name}'s phone is {contacts[name]}"


def show_all_contacts(*args):
    all_contacts = (pd.DataFrame(list(contacts.items()),
                                 columns=['Name', 'Phone']).sort_values(by=["Name"], ignore_index=True))

    return all_contacts.to_string(index=False)


@input_error
def parse_command(user_input):
    if user_input.startswith('hello'):
        return hello, []
    if user_input == "show all":
        return show_all_contacts, []
    if user_input.startswith('phone'):
        name = user_input.split()[1].capitalize()
        return get_phone, name
    if user_input.startswith("add"):
        name, phone = parse_complex_data(user_input)
        return add_contact, name, phone
    if user_input.startswith("change"):
        name, phone = parse_complex_data(user_input)
        return change_contact, name, phone
    else:
        raise TypeError('Invalid command, please check your input')


def parse_complex_data(user_input):
    data = user_input.split()
    name, phone = data[1].capitalize(), data[2]
    return name, phone


def main():
    while True:
        user_input = input("Please enter your command here >>> ")
        if user_input in QUIT_COMMANDS:
            print("Good bye!")
            break
        run, *args = parse_command(user_input.lower())
        if run:
            print(run(*args))
        else:
            print(args[0])


if __name__ == '__main__':
    main()
