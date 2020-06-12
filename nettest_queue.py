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
        self.threads_pool = []
        self.count_threads = 0
        self.thread_worker_busy = False

    def thread_pool_append(self, target, args, daemon=True):
        self.threads_pool.append({'target': target, 'args': args, 'daemon': True, 'picked': False, 'done': False})
        self.count_threads += 1

    def thread_pool_print(self):
        for thread in self.threads_pool:
            print(thread)

    def return_pool_len(self):
        return len(self.threads_pool)

    def get_thread_of_pool(self, index):
        if self.threads_pool[index]['done'] == False:
            return self.threads_pool[index]
        else:
            return False

    def runCommandInBackground(self, cmd, gui_queue, timeout, file_path):
        #nop = None
        self.thread_worker_busy = True
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ''
        print_separator(file_path, '-')
        for line in p.stdout:
            line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
            output += line
            gui_queue.put(line)
            #2 - retorna uma tupla com work_id e o texto e booleano dizendo se terminou.
            #print(line)
            with open(file_path, 'a') as out:
                out.write(line + '\n')
            #window.refresh() if window else nop
        
        # gui_queue.put(output)
        p.wait(timeout)
        #retval = p.wait(timeout)
        #return (retval, output)
        #self.thread_pool_print()
        print(f'ESTADOR DO WORKER DENTRO DA FUNCAO RUNCOMMAND ANTES DE SETAR: {self.thread_worker_busy}')
        self.thread_worker_busy = False
        print(f'ESTADOR DO WORKER DENTRO DA FUNCAO RUNCOMMAND DEPOIS DE SETAR: {self.thread_worker_busy}')


    #def execute_thread(self, args):
    #    executing_thread = threading.Thread(target=runCommandInBackground, args=args, daemon=True)
    #    executing_thread.start()


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

    tp = ThreadQueue() 

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

            #runCommandInBackground(cmd='ipconfig /all', window=window, file_path=file_path)
            #rodarEmBackground(target=runCommandInBackground, args=('ipconfig /all', gui_queue, None, file_path))
            tp.thread_pool_append(target=tp.runCommandInBackground, args=('ipconfig /all', gui_queue, None, file_path))
        
            #ping
            # print_separator(file_path, '=')
            # print_title(file_path=file_path, phrase='Executando Ping...')
            # print_separator(file_path, '=')
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                #rodarEmBackground(target=runCommandInBackground, args=(f'ping {value}', gui_queue, None, file_path))
                tp.thread_pool_append(target=tp.runCommandInBackground, args=(f'ping {value}', gui_queue, None, file_path))

            #tracert
            #print_separator(file_path, '=')
            #print_title(file_path=file_path, phrase='Executando Tracert...')
            #print_separator(file_path, '=')
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                # runCommandInBackground(cmd=f'tracert -d -w 400 {value}', file_path=file_path)
                #rodarEmBackground(target=runCommandInBackground, args=(f'tracert -d -w 400 {value}', gui_queue, None, file_path))
                tp.thread_pool_append(target=tp.runCommandInBackground, args=(f'tracert -d -w 400 {value}', gui_queue, None, file_path))

            #nslookup
            # print_separator(file_path, '=')
            # print_title(file_path=file_path, phrase='Executando Nslookup...')
            # print_separator(file_path, '=')
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                #rodarEmBackground(target=runCommandInBackground, args=(f'nslookup {value}', gui_queue, None, file_path))
                tp.thread_pool_append(target=tp.runCommandInBackground, args=(f'nslookup {value}', gui_queue, None, file_path))

            #Printa a thread a ser executada no momento:
            tp.thread_pool_print()

            #Executa a thread e a marca como done = True, apos executar.

            threads_pool_len = tp.return_pool_len()
            print(f'THREAD POOL LEN: {threads_pool_len}')

            for index in range(0, threads_pool_len):

                #printar o estado do Worker
                print(f'ESTADO DO WORKER: {tp.thread_worker_busy}')

                current_thread = tp.threads_pool[index]
                
                while True:
                    window.refresh()
                    if current_thread['picked'] == False and tp.thread_worker_busy == False:
                        args = (current_thread['args'][0], 
                                current_thread['args'][1],
                                current_thread['args'][2],
                                current_thread['args'][3])       
                        executing_thread = threading.Thread(target=current_thread['target'], args=args, daemon=True)
                        executing_thread.start()
                    else:
                        print('Thread Pool Cleaned.')

                    if tp.thread_worker_busy == False:
                        pass

            #tp.thread_pool_print()
            print(f'ESTADO DO WORKER DEPOIS PERCORRER A POOL: {tp.thread_worker_busy}')
            
        try:
            message = gui_queue.get_nowait()    # see if something has been posted to Queue
        except queue.Empty:                     # get_nowait() will get exception when Queue is empty
            message = None                      # nothing in queue so do nothing

        # if message received from queue, then some work was completed
        if message is not None:
            #4 - cada vez que vier uma mensagem com booleano true que acabou comecar a proxima, rodar em bg e remover da lista
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