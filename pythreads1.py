import concurrent.futures
from time import sleep

def print_teste(nome, alias, index):
    print(f'start thread. nome:{nome} - {alias} - {index}.')
    sleep(2)
    print(f'finish thread. nome:{nome} - {alias} - {index}.')

args=('teste', 'teste_alias')
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    for index in range(2):
        executor.submit(print_teste, 'teste_nome', 'teste_alias', index)