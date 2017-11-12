from lib.iot.gpio import gsgpio
from time import sleep

if __name__=='__main__':
    gpioBuzz=gsgpio(13,'Buzz')
    gpioBuzz.open()
    gpioBuzz.buzz()
    gpioBuzz.close()