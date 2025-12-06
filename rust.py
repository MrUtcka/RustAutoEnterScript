import schedule as sch
from time import sleep
from datetime import datetime, timedelta
import mouse, keyboard
import os

#binds
keyForOpenConsole = 'f1'

#connect data
serverIP = '19.magicrust.gg' #without connect
dayToEnter = 'monday' #name
timeToEnter = '00:00' #only hh:mm

def enter():
    global keyForOpenConsole, serverIP
    
    print('\n' + 'entering to server ' + serverIP + ' ...')
    
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


def _get_key():
    """Возвращает 'UP','DOWN','LEFT','RIGHT','ENTER','ESC' или обычный символ."""
    try:
        import msvcrt
    except Exception:
        return None

    ch = msvcrt.getwch()
    if ch in ('\x00', '\xe0'):
        ch2 = msvcrt.getwch()
        return {'H': 'UP', 'P': 'DOWN', 'K': 'LEFT', 'M': 'RIGHT'}.get(ch2, None)
    if ch == '\r':
        return 'ENTER'
    if ch == '\x1b':
        return 'ESC'
    return ch
        

def setKeyForOpenConsole():
    global keyForOpenConsole
    print("RustAutoEnterScript" + "\n" + "-" * 50)
    keyForOpenConsole = input(f'enter your bind for open console | current: *{keyForOpenConsole}*: ').lower()
    
    
def setTimeToEnter():
    global timeToEnter
    print("RustAutoEnterScript" + "\n" + "-" * 50)
    timeToEnter = input(f'enter time to wipe server (hh:mm) | current: *{timeToEnter}*: ').lower()
    
    
def setDayToEnter():
    global dayToEnter
    print("RustAutoEnterScript" + "\n" + "-" * 50)
    dayToEnter = input(f'enter day to wipe server (monday) | current:  *{dayToEnter}*: ').lower()
    
    
def setServerIP():
    global serverIP
    print("RustAutoEnterScript" + "\n" + "-" * 50)
    serverIP = input(f'enter server ip (without connect) | current: *{serverIP}*: ').lower()


def console_menu(options, title = "Menu"):
    """Простой прототип консольного меню.

    Управление: стрелки вверх/вниз — перемещение, Enter — выбор, Esc — выход.
    Возвращает индекс выбранного пункта или None при выходе.
    """
    sel = 0
    while True:
        os.system('cls')
        
        if title:
            print(title)
            print('-' * min(len(title), 50))

        for i, opt in enumerate(options):
            prefix = '>' if i == sel else ' '
            print(f" {prefix} {opt}")

        k = _get_key()
        if k == 'UP':
            sel = (sel - 1) % len(options)
        elif k == 'DOWN':
            sel = (sel + 1) % len(options)
        elif k == 'ENTER':
            return sel
        elif k == 'ESC' or k is None:
            return None


def run_menu(menu_def, title = None):
    """Универсальная функция меню.

    Управление: стрелки вверх/вниз для пунктов, влево/вправо для переключения вкладок,
    Enter для выбора, Esc для выхода.
    Возвращает 'exit' если выбран пункт с action == 'exit', иначе None.
    """
        

    if isinstance(menu_def, dict) and 'tabs' in menu_def:
        tabs = menu_def['tabs']
        tab_idx = 0
        sel = 0
        while True:
            os.system('cls')
            if title:
                print(title)
            tab_line = []
            for i, t in enumerate(tabs):
                lbl = t[0]
                if i == tab_idx:
                    tab_line.append(f'[{lbl}]')
                else:
                    tab_line.append(f' {lbl} ')
            print(' '.join(tab_line))
            print('-' * 100)

            items = tabs[tab_idx][1]
            for i, it in enumerate(items):
                label = it.get('label') if isinstance(it, dict) else str(it)
                prefix = '>' if i == sel else ' '
                print(f" {prefix} {label}")

            k = _get_key()
            if k == 'LEFT':
                tab_idx = (tab_idx - 1) % len(tabs)
                sel = 0
            elif k == 'RIGHT':
                tab_idx = (tab_idx + 1) % len(tabs)
                sel = 0
            elif k == 'UP':
                sel = (sel - 1) % len(items)
            elif k == 'DOWN':
                sel = (sel + 1) % len(items)
            elif k == 'ENTER':
                action = items[sel].get('action') if isinstance(items[sel], dict) else None
                if action is None:
                    return None
                if action == 'exit':
                    return 'exit'
                if callable(action):
                    os.system('cls')
                    try:
                        action()
                    except Exception as e:
                        print(f'Error in action: {e}')
                elif isinstance(action, list) or (isinstance(action, dict) and 'tabs' in action):
                    res = run_menu(action, title = items[sel].get('label'))
                    if res == 'exit':
                        return 'exit'
            elif k == 'ESC' or k is None:
                return None
    else:
        if isinstance(menu_def, list):
            labels = []
            for it in menu_def:
                if isinstance(it, dict):
                    labels.append(it.get('label'))
                else:
                    labels.append(str(it))
            idx = console_menu(labels, title = title or 'Menu')
            if idx is None:
                return None
            item = menu_def[idx]
            action = item.get('action') if isinstance(item, dict) else None
            if action == 'exit':
                return 'exit'
            if callable(action):
                action()
            elif isinstance(action, list) or (isinstance(action, dict) and 'tabs' in action):
                return run_menu(action, title = item.get('label') if isinstance(item, dict) else None)
        return None


def start():
    print("waiting...")
    
    current_time = datetime.strptime(timeToEnter, "%H:%M")
    temp = (current_time - timedelta(minutes = 1)).strftime("%H:%M")
    getattr(sch.every(), dayToEnter).at(temp + ':58').do(enter)

    while True:
        sch.run_pending()
        
    
def main():
    global dayToEnter, timeToEnter
    
    def show_info():
        print('\nCurrent settings:')
        print(f' bind: {keyForOpenConsole}, server: {serverIP}, day: {dayToEnter}, time: {timeToEnter}')
        input('\nPress Enter to continue...')

    main_menu = {
        'tabs': [
            ('General', [
                {'label': 'Run', 'action': lambda: start()},
                {'label': 'Show current settings', 'action': show_info},
            ]),
            ('Settings', [
                {'label': 'Edit ip', 'action': lambda: setServerIP()},
                {'label': 'Edit day', 'action': lambda: setDayToEnter()},
                {'label': 'Edit time', 'action': lambda: setTimeToEnter()},
                {'label': 'Edit console bind', 'action': lambda: setKeyForOpenConsole()},
            ]),
            ('Quit', [
                {'label': 'Exit program', 'action': 'exit'},
            ])
        ]
    }

    choice = run_menu(main_menu, title = 'RustAutoEnterScript')
    if choice == 'exit':
        print('Exit menu.')
        quit()


if __name__ == '__main__':
    main()