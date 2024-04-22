from pyfiglet  import Figlet
from termcolor import colored

def greeting():
    number_of_=70
    text = "ARMOR Project"
    
    f = Figlet(font='standard')
    print(colored('-'*number_of_, 'blue'))
    print(colored('-'*number_of_, 'blue'))
    print(colored(f.renderText(text), 'green'))
    print(colored('-'*number_of_, 'blue'))
    print(colored('-'*number_of_, 'blue'))
    print('\n')