import subprocess
import os

file_dir = r'D:\test.txt'

def make_file(file_dir):
    with open(file_dir, 'wb') as out:
        out.write(subprocess.check_output('TESTE Unifique'))

def ping(file_dir) -> str:
    """Roda o comando ping com host/ip informado."""
    with open(file_dir, 'ab') as out:
        out.write(subprocess.check_output('ping terra.com.br'))
    #p.wait()
    #return p.poll()

def retorna_diretorio_atual() -> str:
    """Retorna o diretorio no qual o aplicativo foi executado."""
    try:
        diretorio = os.getcwd()
        return diretorio
    except Exception as err:
        print('Erro ao ler diretorio. Diretorio nao existe ou voce nao tem permissao para gravar.', str(err))


host = 'terra.com.br'
print(host, file_dir)
make_file(file_dir)
ping(file_dir)
print('=' * 10)


"""
import subprocess
with open('output.txt','w') as out:
    out.write(subprocess.check_output("ping www.google.com"))
"""