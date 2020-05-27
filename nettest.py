import subprocess
import os

def ping(host: str) -> str:
    """Roda o comando ping com host/ip informado."""
    p = subprocess.Popen(f'ping {host}')
    p.wait()
    return p.poll()

def retorna_diretorio_atual() -> str:
    """Retorna o diretorio no qual o aplicativo foi executado."""
    try:
        diretorio = os.getcwd()
        return diretorio
    except Exception as err:
        print('Erro ao ler diretorio. Diretorio nao existe ou voce nao tem permissao para gravar.', str(err))

def 

host = 'terra.com.br'
saida = ping(host)
print(saida)
print(saida)