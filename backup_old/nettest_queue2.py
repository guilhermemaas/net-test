# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import subprocess
import os
import time
import sys
import threading
import queue
from enum import Enum


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
    print('=' * 60 + '\n' + '=' * 60 + '\n' + 'INICIANDO TESTES:\n' + '-' * 60)
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
    'localhost': 'localhost'
}

#sg.theme('Reddit')
sg.theme('DarkAmber')


class ThreadQueue():
    def __init__(self):
        self.thread_queue = queue.Queue()

    def put(self, args):
        self.thread_queue.put(args)

    def run_in_sequence(self):
        worker = threading.Thread(target=self.__control_loop)
        worker.setDaemon(True)
        worker.start()

    def __control_loop(self):
        worker = threading.Thread(target=self.run_command_in_background)
        worker.setDaemon(True)
        worker.start()
        
        self.thread_queue.join() #aguarda o processamento da fila

    def run_command_in_background(self):
        while True:
            cmd, gui_queue, timeout, file_path = self.thread_queue.get()

            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = ''
            print_separator(file_path, '-')
            for line in p.stdout:
                line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
                output += line
                gui_queue.put(line)
                with open(file_path, 'a') as out:
                    out.write(line + '\n')
            
            p.wait(timeout)
            self.thread_queue.task_done()


def main():

    gui_queue = queue.Queue()

    layout = [
        [sg.Image(r'C:\Users\guilh\Documents\dev\net-test\images\nettest.png')],
        #[sg.Image(r'C:\Users\guilherme.maas\Documents\dev\net-test\images\unifique.png')],
        #[sg.Text('Unifique - Testador de conexões de Rede.')],
        [sg.Text('NetTest - Testador de conexões de Rede.')],
        [sg.Text('Diretório de saída:', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
        [sg.Text('Endereço alternativo:', size=(15, 1)) ,sg.InputText()],
        [sg.Text('Exemplos de endereço: terra.com.br, uol.com.br, globo.com')],
        [sg.Output(size=(110,30), background_color='black', text_color='white')],
        [sg.Button('Testar'), sg.Button('Sair')],
        [sg.Text('github.com/guilhermemaas')],
        #[sg.Text('unifique.com.br')]
    ]

    window = sg.Window('nettest - Network Tester', layout)
    #window = sg.Window('Unifique - Testador de conexões de Rede', layout)

    command_queue = ThreadQueue() 

    while True:        
        event, values = window.read(timeout=15)

        out_dir = values[1].replace('/', '\\')

        if values[2]:
            address_dict['custom_address'] = values[2]
        
        file_name = 'nettest.txt'
        file_path = os.path.join(out_dir, file_name)

        if event == 'Testar':
            
            make_file(file_path)

            print_logo(file_path)

            print_separator(file_path, '=')
            print_separator(file_path, '=')

            command_queue.put(('ipconfig /all', gui_queue, None, file_path))
        
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                command_queue.put((f'ping {value}', gui_queue, None, file_path))

            for key, value in address_dict.items():
                print_separator(file_path, '-')
                command_queue.put((f'tracert -d -w 400 {value}', gui_queue, None, file_path))

            for key, value in address_dict.items():
                print_separator(file_path, '-')
                command_queue.put((f'nslookup {value}', gui_queue, None, file_path))

            command_queue.run_in_sequence()
            
        try:
            message = gui_queue.get_nowait()    # see if something has been posted to Queue
        except queue.Empty:                     # get_nowait() will get exception when Queue is empty
            message = None                      # nothing in queue so do nothing

        # if message received from queue, then some work was completed
        if message is not None:
            print(message)
            # LOCATION 3
            # this is the place you would execute code at ENDING of long running task
            # You can check the completed_work_id variable to see exactly which long-running function completed
            # completed_work_id = int(message[:message.index(' :::')])
            # window.Element('_OUTPUT2_').Update('Complete Work ID "{}"'.format(completed_work_id))
            # window.Element(completed_work_id).Update(background_color='green')
            #ctrl+ku, ctrl+kc
            window.refresh()
            
        if event in (None, 'Sair'):
            break

    window.close()

main()