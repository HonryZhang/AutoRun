import paramiko  

#execute command from remote host  
def sshclient_execmd(hostname, port, username, password, execmd, **kw):  
    paramiko.util.log_to_file("paramiko.log")   
    s = paramiko.SSHClient()  
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())       
    s.connect(hostname=hostname, port=port, username=username, password=password)  
    sync = True 
    for k,w in kw.iteritems():
        if (k == 'sync'):
            sync = w
    #execmd = execmd + ' 2>\&1'
    #print execmd
    #print sync
    #sync
    if(sync == True):
        stdin, stdout, stderr = s.exec_command (execmd)  
    else: #async
        stdin, stdout, stderr = s.exec_command (execmd, get_pty=True)  

    #stdin, stdout, stderr = s.exec_command (execmd)  
    
    #stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.        
    #stdin.flush()
    result = stdout.read() +stderr.read()

    
    s.close()  
    return result[1:]

