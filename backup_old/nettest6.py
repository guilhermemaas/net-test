# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import subprocess
import os
import time
import sys
import threading
import queue
from enum import Enum
import concurrent
import concurrent.futures


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
    'google': 'localhost',
}

#sg.theme('Reddit')
sg.theme('DarkAmber')

def runCommandInBackground(cmd, gui_queue, timeout, file_path):
    #nop = None
  
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
    #return True


def rodarEmBackground(target, args):
    thread_id = threading.Thread(target=target, args=args, daemon=True)
    thread_id.start()
    #thread_id.join()


class WorkInProgress():
    def __init__(self, status) -> None:
        self.status = False

    def start_work(self) -> None: 
        self.status = True

    def stop_work(self) -> None:
        self.status = False

    def return_status(self) -> bool:
        return self.status


def main():
    gui_queue = queue.Queue()

    layout = [
        #[sg.Image(r'C:\Users\guilh\Documents\dev\net-test\images\nettest.png')],
        [sg.Image(r'C:\Users\guilherme.maas\Documents\dev\net-test\images\nettest.png')],
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

    #window = sg.Window('nettest - Network Tester', layout)
    window = sg.Window('Unifique - Testador de conexões de Rede', layout)

    #3 - Adicionar cada chamada em bg em uma lista de chamadas(Cada item [e um args])
    #dentro do While a cada for adicionar dentro da lista os args

    command_queue = []
    work_status = WorkInProgress(False)
    work_status.stop_work()

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
            # thread_id = threading.Thread(target=runCommandInBackground, args=('ipconfig /all', gui_queue, None, file_path), daemon=True)
            # thread_id.start()
            #rodarEmBackground(target=runCommandInBackground, args=('ipconfig /all', gui_queue, None, file_path))
            ##event_list.append(('ipconfig /all', gui_queue, None, file_path))
            command_queue.append({'command': 'ipconfig /all', 'gui_queue': gui_queue, 'time_out': None, 'file_path': file_path})

            # ping
            # print_separator(file_path, '=')
            # print_title(file_path=file_path, phrase='Executando Ping...')
            # print_separator(file_path, '=')
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                #rodarEmBackground(target=runCommandInBackground, args=(f'ping {value}', gui_queue, None, file_path))
                #command_queue.append({'args': (f'ping {value}', gui_queue, None, file_path)})
                command_queue.append({'command': f'ping {value}', 'gui_queue': gui_queue, 'time_out': None, 'file_path': file_path})

            # tracert
            # print_separator(file_path, '=')
            # print_title(file_path=file_path, phrase='Executando Tracert...')
            # print_separator(file_path, '=')
            # for key, value in address_dict.items():
            #     print_separator(file_path, '-')
            #     #runCommandInBackground(cmd=f'tracert -d -w 400 {value}', file_path=file_path)
            #     #rodarEmBackground(target=runCommandInBackground, args=(f'tracert -d -w 400 {value}', gui_queue, None, file_path))
            #     #command_queue.append((f'tracert -d -w 400 {value}', gui_queue, None, file_path))
            #     command_queue.append({'args': (f'tracert -d -w 400 {value}', gui_queue, None, file_path)})

            # nslookup
            # print_separator(file_path, '=')
            # print_title(file_path=file_path, phrase='Executando Nslookup...')
            # print_separator(file_path, '=')
            # for key, value in address_dict.items():
            #     print_separator(file_path, '-')
            #     #rodarEmBackground(target=runCommandInBackground, args=(f'nslookup {value}', gui_queue, None, file_path))
            #     #event_list.append((f'nslookup {value}', gui_queue, None, file_path))
            #     command_queue.append({'args': (f'nslookup {value}', gui_queue, None, file_path)})

            # #with open(file_path, 'r') as log:
            # #    sg.popup_scrolled(log.read())

            # print_separator(file_path, '=')
            # print_title(file_path=file_path, phrase='Teste Finalizado.')
            # print_separator(file_path, '=')

            # 5 - Rodar o primeiro da lista antes da etapa #4

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    #executor.submit(runCommandInBackground, ('nslookup localhost', gui_queue, None, file_path))
                    #print(command_queue[0])
                    #print(command_queue[0]['command'])
                    for command in command_queue:
                        executor.submit(runCommandInBackground, command['command'], command['gui_queue'], command['time_out'], command['file_path'])

            """
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                for command in command_queue:
                    print(command['args'])
                    executor.submit(runCommandInBackground, args=command['args'])
            """

            """
            for command in command_queue:
                if command['work_done'] == False:
                    #work_status.start_work
                    rodarEmBackground(target=runCommandInBackground, args=command['args'])
                    command['work_done'] == True
            """
            """
            threads = list()
            for command in command_queue:
                #logging.info("Main    : create and start thread %d.", index)
                x = threading.Thread(target=runCommandInBackground, args=(command['args'], gui_queue, None, file_path))
                threads.append(x)
                x.start()

            for index, thread in enumerate(threads):
                #logging.info("Main    : before joining thread %d.", index)
                thread.join()
                #logging.info("Main    : thread %d done", index)
            """

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

#1 - Passar um work_id no args sempre, diferente para cada chamada em bg.
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms%20old/Demo_Threaded_Work.py
#https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Script_Launcher_Realtime_Output.py

#http://speed.unifique.com.br/
#https://github.com/librespeed/speedtest
#Response HTTP dos endereços do dicionário.