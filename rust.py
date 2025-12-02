import schedule as sch
from time import sleep
import mouse, keyboard

#binds
keyForOpenConsole = 'f1'

#connect data
serverIP = 'ip' #without connect
dayToEnter = 'monday' #name
timeToEnter = '00:00' #only hh:mm


def enter():
    global keyForOpenConsole, serverIP
    
    keyboard.send(keyForOpenConsole)
    sleep(0.3)
    keyboard.write('connect ' + serverIP)
    sleep(0.3)
    keyboard.send('enter')
    sleep(0.3)
    keyboard.send(keyForOpenConsole)
    sleep(0.2)
    
    print('\n' + 'entered to server ' + serverIP)
    quit()


def inputData():
    global keyForOpenConsole, serverIP, dayToEnter, timeToEnter
    
    keyForOpenConsole = input('enter your bind for open console *f1*: ').lower()
    dayToEnter = input('enter day to enter to server *monday*: ').lower()
    timeToEnter = input('enter time to enter to server *00:00*: ').lower()
    serverIP = input('enter server ip *ip*: ').lower()

    
def main():
    global dayToEnter, timeToEnter
    
    inputData()
    print('\n' + 'auto enter scheduled for ' + dayToEnter + ' at ' + timeToEnter + ' to server ' + serverIP)
    
    getattr(sch.every(), dayToEnter).at(timeToEnter + ':58').do(enter)

    while True:
        sch.run_pending()
        

if __name__ == '__main__':
    main()