from pyfiglet  import Figlet
from termcolor import colored

def greeting():
    n=70
    text = "ARMOR Project"
    
    f = Figlet(font='standard')
    print(colored('-'*n, 'blue'))
    print(colored('-'*n, 'blue'))
    print(colored(f.renderText(text), 'green'))
    print(colored('-'*n, 'blue'))
    print(colored('-'*n, 'blue'))
    print('\n')