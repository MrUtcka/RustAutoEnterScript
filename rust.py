import schedule as sch
from time import sleep
import mouse, keyboard

def enter():
    keyboard.send('f1')
    sleep(0.3)
    keyboard.write('connect 19.magicrust.gg')
    sleep(0.3)
    keyboard.send('enter')
    sleep(0.3)
    keyboard.send('f1')
    sleep(0.2)

    
def main():
    sch.every().friday.at('13:59:58').do(enter)

    while True:
        sch.run_pending()
        

if __name__ == '__main__':
    main()