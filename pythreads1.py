import concurrent.futures
from time import sleep

def print_teste(name):
    print(f'start thread. {name}.')
    sleep(2)
    print(f'finish thread. {name}.')

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    for index in range(2):
        executor.submit(print_teste, index)