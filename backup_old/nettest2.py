# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import subprocess
import os
import time
import sys


def make_file(file_path) -> str:
    with open(file_path, 'w') as out:
        out.write('nettest - Network Tester')

def print_separator(file_path, char) -> str:
    with open(file_path, 'a') as out:
        out.write(f'{char}' * 120 + '\n')


def ping(address, file_path) -> str:
    """Roda o comando ping com host/ip informado."""
    with open(file_path, 'ab') as out:
        out.write(subprocess.check_output(f'ping {address}'))


def ping_print_multiline(address, file_path, key) ->str:
    ping_string = subprocess.check_output(f'ping {address}')
    #window[key].print(subprocess.check_output(f'ping {address}'))
    window[key].print(ping_string)
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
    'google': 'localhost'
}

sg.theme('Reddit')

def runCommand(cmd, timeout=None, window=None):
	nop = None
	""" run shell command
	@param cmd: command to execute
	@param timeout: timeout for command execution
	@param window: the PySimpleGUI window that the output is going to (needed to do refresh on)
	@return: (return code from command, command output)
	"""
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output = ''
	for line in p.stdout:
		line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
		output += line
		print(line)
		window.refresh() if window else nop        # yes, a 1-line if, so shoot me

	retval = p.wait(timeout)
	return (retval, output)


def main():
    layout = [
        [sg.Text('nettest - Network Tester')],
        [sg.Image(r'C:\Users\guilh\Documents\dev\net-test\images\simplegui.png')],
        [sg.Text('Pode ser utilizado endereço IP ou Web Site/Host.')],
        [sg.Text('Diretório de saída:', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
        [sg.Text('Endereço:', size=(15, 1)) ,sg.InputText()],
        [sg.Output(size=(110,30), background_color='black', text_color='white')],
        #[sg.Multiline(size=(70, 15), key='ml1')],
        [sg.Button('Testar'), sg.Button('Cancelar')]
    ]

    window = sg.Window('nettest - Network Tester', layout)

    while True:
        event, values = window.read(timeout=15)
        out_dir = values[1].replace('/', '\\')
        if values[2]:
            address_dict['custom_address'] = values[2]
        file_name = 'nettest.txt'
        file_path = os.path.join(out_dir, file_name)

        if event == 'Testar':
            print_separator(file_path, '=')
            print(file_path) #remover
            print_separator(file_path, '=')
            make_file(file_path)
            
            time.sleep(3)
            ipconfig(file_path)
            runCommand(cmd='ipconfig /all', window=window)

            #ping
            #time.sleep(3)
            window['ml1'].print('TESTANDO PING...')
            window.refresh()
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                ping(value, file_path)
                ping_print_multiline(address=value, key='ml1', file_path=file_path)

            #tracert
            #time.sleep(3)
            window['ml1'].print('TESTANDO TRACERT...')
            window.refresh()
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                tracert(value, file_path)

            #nslookup
            #time.sleep(3)
            window['ml1'].print('TESTANDO NSLOOKUP...')
            window.refresh()
            for key, value in address_dict.items():
                print_separator(file_path, '-')
                nslookup(value, file_path)

            with open(file_path, 'r') as log:
                sg.popup_scrolled(log.read())
            
            print_separator(file_path, '=')
            print_separator(file_path, '=')
            
        if event in (None, 'Cancelar'):
            break

    window.close()

main()