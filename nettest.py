import PySimpleGUI as sg
import subprocess
import os


def make_file(file_path) -> str:
    with open(file_path, 'w') as out:
        out.write('nettest - Network Tester')


def ping(address, file_path) -> str:
    """Roda o comando ping com host/ip informado."""
    with open(file_path, 'ab') as out:
        out.write(subprocess.check_output(f'ping {address}'))


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


sg.theme('Reddit')

layout = [
    [sg.Text('nettest - Network Tester')],
    [sg.Image(r'C:\Users\guilherme.maas\Documents\dev\net-test\images\simplegui.png')],
    [sg.Text('Pode ser utilizado endereço IP ou Web Site/Host.')],
    [sg.Text('Diretório de saída:', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
    [sg.Text('Endereço:', size=(15, 1)) ,sg.InputText()],
    [sg.Multiline(size=(70, 15))],
    [sg.Button('Testar'), sg.Button('Cancelar')]
]

window = sg.Window('nettest - Network Tester', layout)

while True:
    event, values = window.read()
    out_dir = values[1].replace('/', '\\')
    address = values[2]
    file_name = 'teste.txt'
    file_path = os.path.join(out_dir, file_name)

    if event == 'Testar':
        print(file_path)
        make_file(file_path)
        ipconfig(file_path)
        ping(address, file_path)
        ping('localhost', file_path)
        tracert(address, file_path)
        nslookup(address, file_path)
        nslookup2(address, file_path)

        with open(file_path, 'r') as log:
            sg.popup_scrolled(log.read())
        
    if event in (None, 'Cancelar'):
        break

window.close()