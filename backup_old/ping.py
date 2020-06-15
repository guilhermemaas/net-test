import subprocess
def systemCommand(Command):
    Output = ""
    Error = ""     
    try:
        Output = subprocess.check_output(Command,stderr = subprocess.STDOUT,shell='True')
    except subprocess.CalledProcessError as e:
        #Invalid command raises this exception
        Error =  e.output 

    if Output:
        Stdout = Output.split("\n")
    else:
        Stdout = []
    if Error:
        Stderr = Error.s plit("\n")
    else:
        Stderr = []

    return (Stdout,Stderr)

#main
Host = "ip to ping"
NoOfPackets = 2
Timeout = 5000 #in milliseconds
#windows
Command = 'ping -n {0} -w {1} {2}'.format(NoOfPackets,Timeout,Host)
#linux 
#Command = 'ping -c {0} -w {1} {2}'.format(NoOfPackets,Timeout,Host)
Stdout,Stderr = systemCommand(Command)
if Stdout:
   print("Host [{}] is reachable.".format(Host))
else:
   print("Host [{}] is unreachable.".format(Host))