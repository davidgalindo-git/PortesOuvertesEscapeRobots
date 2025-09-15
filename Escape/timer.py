import time

def ticker():
    i = 1
    while True:
        time.sleep(1)
        return i

def start_timer():
    counter = 0
    counter += ticker()

def pause_timer():
    pass

def end_timer():
    pass