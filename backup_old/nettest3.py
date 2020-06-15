# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import subprocess
import os
import time
import sys
import threading


def make_file(file_path) -> str:
    with open(file_path, 'w') as out:
        out.write('nettest - Network Tester')


def print_separator(file_path, char) -> str:
    print(f'{char}' * 60)
    with open(file_path, 'a') as out:
        out.write(f'{char}' * 60 + '\n')


def print_title(file_path, phrase) -> str:
    print(f'{phrase}')
    with open(file_path, 'a') as out:
        out.write(f'{phrase}' + '\n')


def print_logo(file_path) -> str:
    logo="""
         _   __     __     ______          __ 
       /  | /  /__  / /_   /_  __/__  _____/ /_
      /   |/  / _ \/ __/    / / / _ \/ ___/ __/
     / / |   /  __/ /_     / / /  __(__  ) /_  
    /_/  |_ /\___/\__/    /_/  \___/____/\__/                                           
    """
    #print(logo)
    print('=' * 60 + '\n' + '=' * 60 + '\n' + 'INICIANDO TESTES:')
    with open(file_path, 'a') as out:
        out.write(logo)


def ping(address, file_path) -> str:
    """Roda o comando ping com host/ip informado."""
    with open(file_path, 'ab') as out:
        out.write(subprocess.check_output(f'ping {address}'))


def ping_print_multiline(address, file_path, key) ->str:
    ping_string = subprocess.check_output(f'ping {address}')
    #window[key].print(ping_string)
    with open(file_path, 'ab') as out:
        out.write(ping_string)


def ipconfig(file_path) -> str:
    """Roda o comando ipconfig /all."""
    with open(file_path, 'ab') as out:
        out.write(subprocess.check_output('ipconfig /all'))


def tracert(address, file_path) -> str:
    """Roda o comando tracert -d -w 400 $endereco"""
    with open(file_path, 'ab') as out:
        out.write(subprocess.check_output(f'tracert -d -w 400 {address}'))


def nslookup(address, file_path) ->str:
    """Roda o comando nslookup"""
    with open(file_path, 'ab') as out:
        out.write(subprocess.check_output(f'nslookup {address}'))


def nslookup2(address, file_path) -> str:
    """Roda o comando nslookup $endereco 8.8.8.8"""
    with open(file_path, 'ab') as out:
        out.write(subprocess.check_output(f'nslookup {address} 8.8.8.8'))


address_dict = {
    'google': 'localhost',
}

#sg.theme('Reddit')
sg.theme('DarkAmber')


def runCommand(cmd, timeout=None, window=None, file_path=None):
    nop = None
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        with open(file_path, 'a') as out:
            out.write(line + '\n')
        window.refresh() if window else nop

    retval = p.wait(timeout)
    return (retval, output)


def main():
    layout = [
        [sg.Image(r'C:\Users\guilh\Documents\dev\net-test\images\nettest.png')],
        [sg.Text('NetTest - A Network tester and log generator.')],
        [sg.Text('Diretório de saída:', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
        [sg.Text('Endereço alternativo:', size=(15, 1)) ,sg.InputText()],
        [sg.Text('Exemplos de endereço: terra.com.br, uol.com.br, globo.com')],
        [sg.Output(size=(110,30), background_color='black', text_color='white')],
        [sg.Button('Testar'), sg.Button('Sair')],
        [sg.Text('github.com/guilhermemaas')],
    ]

    window = sg.Window('nettest - Network Tester', layout)

    while True:
        event, values = window.read(timeout=15)

        out_dir = values[1].replace('/', '\\')

        if values[2]:
            address_dict['custom_address'] = values[2]
        
        file_name = 'nettest.txt'
        file_path = os.path.join(out_dir, file_name)

        #work_id = 0

        if event == 'Testar':
            make_file(file_path)

            print_logo(file_path)

            print_separator(file_path, '=')
            print_separator(file_path, '=')

            runCommand(cmd='ipconfig /all', window=window, file_path=file_path)

            #ping
            print_separator(file_path, '=')
            print_title(file_path=file_path, phrase='Executando Ping...')
            print_separator(file_path, '=')
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                #thread_id = threading.Thread(runCommand(cmd=f'ping {value}', window=window, file_path=file_path))
                #thread_id.start()
                #work_id = work_id+1
                runCommand(cmd=f'ping {value}', window=window, file_path=file_path)

            #tracert
            print_separator(file_path, '=')
            print_title(file_path=file_path, phrase='Executando Tracert...')
            print_separator(file_path, '=')
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                runCommand(cmd=f'tracert -d -w 400 {value}', window=window, file_path=file_path)

            #nslookup
            print_separator(file_path, '=')
            print_title(file_path=file_path, phrase='Executando Nslookup...')
            print_separator(file_path, '=')
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                runCommand(cmd=f'nslookup {value}', window=window, file_path=file_path)

            #with open(file_path, 'r') as log:
            #    sg.popup_scrolled(log.read())
            
            print_separator(file_path, '=')
            print_title(file_path=file_path, phrase='Teste Finalizado.')
            print_separator(file_path, '=')
            
        if event in (None, 'Sair'):
            break

    window.close()

main()