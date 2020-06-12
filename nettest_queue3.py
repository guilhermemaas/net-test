# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import subprocess
import os
import time
import sys
import threading
import queue
from enum import Enum
import requests


def make_file(file_path) -> str:
    with open(file_path, 'w') as out:
        out.write('nettest - Network Tester')


def print_separator(file_path, char) -> str:
    print(f'{char}' * 120)
    with open(file_path, 'a') as out:
        out.write(f'{char}' * 120 + '\n')


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
    \n"""
    print('-' * 120 + '\n' + 'Iniciando Testes:\n' + '-' * 120)
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
    'google': 'google.com',
    'googler': 'googlery.com',
}

#sg.theme('Reddit')
sg.theme('DarkAmber')


class JobBase:
    def __init__(self, gui_queue):
        self.gui_queue = gui_queue
    
    def run(self, control_queue):
        self.execute_job()
        control_queue.task_done()

    def execute_job(self):
        pass


class RunCommandJob(JobBase):
    def __init__(self, cmd, gui_queue, timeout, file_path):
        JobBase.__init__(self, gui_queue)
        self.cmd = cmd
        self.timeout = timeout
        self.file_path = file_path

    def execute_job(self):
        p = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ''
        #print_separator(self.file_path, '-')
        for line in p.stdout:
            line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
            output += line
            self.gui_queue.put(line)
            with open(self.file_path, 'a') as out:
                out.write(line + '\n')
        
        p.wait(self.timeout)


class PrintJob(JobBase):
    def __init__(self, gui_queue, string, file_path):
        JobBase.__init__(self, gui_queue)
        self.string = string
        self.file_path = file_path

    def execute_job(self):
        self.gui_queue.put(self.string)
        with open(self.file_path, 'a') as out:
            out.write(self.string+ '\n')


class GetHttpResponseJob(JobBase):
    def __init__(self, gui_queue, url, file_path):
        JobBase.__init__(self, gui_queue)
        self.url = url
        self.file_path = file_path

    def execute_job(self):
        #print_separator(self.file_path, '-')
        #print(f'Realizando teste HTTP para {self.url}.')
        #print_separator(self.file_path, '-')
        try:
            if 'https://' in self.url:
                r = requests.get(self.url)
            elif 'http://' in self.url:
                r = requests.get(self.url)
            else:
                r = requests.get(f'http://' + self.url)
            self.gui_queue.put(f'Resultado da consulta no endereço {self.url}: {r.status_code} Response Code 200(OK).\n')
            with open(self.file_path, 'a') as out:
                out.write(f'-' * 120 + '\nTeste - Coletando Response Code HTTP.\n' + '-' * 120 + '\n' + 
                    f'Resultado consulta no endereço {self.url}: {r.status_code} Response Code 200(OK).\n')
        except requests.ConnectionError:
            self.gui_queue.put(f'Falha ao conectar no endereço {self.url}: Response Code 404(Not found).\n')
            with open(self.file_path, 'a') as out:
                out.write(f'Falha ao conectar no endereço {self.url}: Response Code 404(Not found).\n')


class Job4ParametrosJob(JobBase):
    def __init__(self, gui_queue, p1, p2, p3, p4):
        JobBase.__init__(self, gui_queue)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def execute_job(self):
        self.gui_queue.put(f'{self.p1} -> {self.p2} -> {self.p3} -> {self.p4}')


class ThreadQueue():
    def __init__(self):
        self.thread_queue = queue.Queue()

    def put(self, job):
        self.thread_queue.put(job)

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
            job = self.thread_queue.get()
            job.run(self.thread_queue)


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

    window = sg.Window('nettest - Network Tester', layout, no_titlebar=True, grab_anywhere=True)
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

            command_queue.put(PrintJob(gui_queue,'\n' + '-' * 120 + '\nColetanto informações com o comando ipconfig /all.\n' + '-' * 120 + '\n', file_path))
            command_queue.put(RunCommandJob('ipconfig /all', gui_queue, None, file_path))

            command_queue.put(PrintJob(gui_queue, '\n' + '-' * 120 + '\nColetanto testes com o comando ping:\n' + '-' * 120 + '\n', file_path))
            for key, value in address_dict.items():
                command_queue.put(PrintJob(gui_queue, f'Host - {value}:', file_path))
                command_queue.put(RunCommandJob(f'ping {value}', gui_queue, None, file_path))

            command_queue.put(PrintJob(gui_queue, '\n' + '-' * 120 + '\nColetanto testes com o comando tracert:\n' + '-' * 120 + '\n', file_path))
            for key, value in address_dict.items():
                command_queue.put(PrintJob(gui_queue, f'Host - {value}:', file_path))
                command_queue.put(RunCommandJob(f'tracert -d -w 400 {value}', gui_queue, None, file_path))

            command_queue.put(PrintJob(gui_queue, '\n' + '-' * 120 + '\nColetanto testes com o comando nslookup:\n' + '-' * 120 + '\n', file_path))
            for key, value in address_dict.items():
                command_queue.put(PrintJob(gui_queue, f'Host - {value}:', file_path))
                command_queue.put(RunCommandJob(f'nslookup {value}', gui_queue, None, file_path))

            command_queue.run_in_sequence()

            command_queue.put(PrintJob(gui_queue, '\n' + '-' * 120 + '\nColetando Response Code HTTP.\n' + '-' * 120 + '\n', file_path))
            for key, value in address_dict.items():
                command_queue.put(PrintJob(gui_queue, f'Host - {value}:', file_path))
                command_queue.put(GetHttpResponseJob(gui_queue, value, file_path))
            
        try:
            message = gui_queue.get_nowait()    # see if something has been posted to Queue
        except queue.Empty:                     # get_nowait() will get exception when Queue is empty
            message = None                      # nothing in queue so do nothing

        # if message received from queue, then some work was completed
        if message is not None:
            print(message)

            window.refresh()
            
        if event in (None, 'Sair'):
            break

    window.close()

main()