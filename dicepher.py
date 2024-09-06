#! /bin/python3

# @thisisnotcamilo
# usage: python3 dicepher.py -d <diceware_dict> -n <number_of_passwords>

import random
import click

def load_diceware_list(filename):
    diceware_dict = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 2:
                diceware_dict[parts[0]] = parts[1]
    return diceware_dict

def roll_dice():
    return ''.join(str(random.randint(1, 6)) for _ in range(5))

def get_random_word(diceware_dict):
    while True:
        roll = roll_dice()
        word = diceware_dict.get(roll)
        if word:
            return word

def get_random_special_char():
    special_chars = '!@#$%&*-+='
    return random.choice(special_chars)

def generate_password(diceware_dict):
    words = [get_random_word(diceware_dict).capitalize() for _ in range(3)]
    special_chars = [get_random_special_char() for _ in range(2)]
    number = random.randint(10, 99)
    
    number_position = random.randint(0, 2)
    words[number_position] += str(number)
    
    password = f"{words[0]}{special_chars[0]}{words[1]}{special_chars[1]}{words[2]}"
    return password

@click.command()
@click.option('-d', '--dict-file', required=True, help='Path to the diceware dictionary')
@click.option('-n', '--number', required=True, default=1, type=int, help='Number of passwords to generate')

def main(dict_file, number):
    try:
        click.secho("Generated password: ", bold=True)

        diceware_dict = load_diceware_list(dict_file)
        for i in range(number):
            password = generate_password(diceware_dict)
            click.secho("  * ", bold=True, nl=False)
            click.secho(f"{password}", fg="magenta")
    except FileNotFoundError:
        click.echo(f"Error: The dictionary file '{dict_file}' was not found.", err=True)
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)

if __name__ == "__main__":
    main()
