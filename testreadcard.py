from lib.iot.readcard import standard
from lib.cmd import cmdshell
def buzz():
    cmdshell("sudo python "+path+"/buzz.py").execute()
if  __name__=='__main__':
    dev=standard("jsc260v20cpu")
    dev.open()
    path=cmdshell().getPath
    # card="000079efbd10"
    # ret=""
    # for i in range(len(card)):
    #     if i%2==0:ret=card[i:i+2]+ret
    # print ret