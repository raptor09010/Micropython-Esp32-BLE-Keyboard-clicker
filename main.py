import time
from machine import Pin
from hid_services import Keyboard

class Device:
    def __init__(self):
        self.pin_s = Pin(0, Pin.IN, Pin.PULL_UP)
        self.pin_forward = Pin(19, Pin.IN, Pin.PULL_UP)
        self.pin_backward = Pin(18, Pin.IN, Pin.PULL_UP)
        self.pin_2nd_tab = Pin(17, Pin.IN, Pin.PULL_UP)
        self.pin_1st_tab = Pin(16, Pin.IN, Pin.PULL_UP)

        # Create our device
        self.keyboard = Keyboard("Keyboard")
        # Set a callback function to catch changes of device state
        self.keyboard.set_state_change_callback(self.keyboard_state_callback)
        # Start our device
        self.keyboard.start()

    # Function that catches device status events
    def keyboard_state_callback(self):
        if self.keyboard.get_state() is Keyboard.DEVICE_IDLE:
            return
        elif self.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:
            return
        elif self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
            return
        else:
            return

    def keyboard_event_callback(self, bytes):
       pass

    def advertise(self):
        self.keyboard.start_advertising()

    def stop_advertise(self):
        self.keyboard.stop_advertising()
        
    def release_keys(self):
        self.keyboard.set_keys()
        self.keyboard.set_modifiers()
        self.keyboard.notify_hid_report()
        
    def set_key(self, key):
        self.keyboard.set_keys(key)
        self.keyboard.notify_hid_report()
        
    def send_char(self, char):
        if char == " ":
            mod = 0
            code = 0x2C
        elif ord("a") <= ord(char) <= ord("z"):
            mod = 0
            code = 0x04 + ord(char) - ord("a")
        elif ord("A") <= ord(char) <= ord("Z"):
            mod = 1
            code = 0x04 + ord(char) - ord("A")
        else:
            assert 0

        self.keyboard.set_keys(code)
        self.keyboard.set_modifiers(left_shift=mod)
        self.keyboard.notify_hid_report()
        time.sleep_ms(2)

        self.keyboard.set_keys()
        self.keyboard.set_modifiers()
        self.keyboard.notify_hid_report()
        time.sleep_ms(2)


    def send_string(self, st):
        for c in st:
            self.send_char(c)
    # Main loop
    def start(self):
        self.advertise()
        while True:
            if self.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
                
                if not(self.pin_forward.value()):
                    self.set_key(0x4F)
                    time.sleep_ms(5)

                    
                    self.release_keys()
                    time.sleep_ms(200)
                    
                if not(self.pin_backward.value()):
                    self.set_key(0x50)
                    time.sleep_ms(5)

                    
                    self.release_keys()
                    time.sleep_ms(200)
            
                if not(self.pin_2nd_tab.value()):
                    self.keyboard.set_modifiers(left_control=1)
                    self.set_key(0x1F)
                    time.sleep_ms(5)

                    
                    self.release_keys()
                    time.sleep_ms(200)
                    
                if not(self.pin_1st_tab.value()):
                    self.keyboard.set_modifiers(left_control=1)
                    self.set_key(0x1E)
                    time.sleep_ms(5)

                    
                    self.release_keys()
                    time.sleep_ms(200)
                    
                if not(self.pin_s.value()):
                    self.set_key(0x16)
                    time.sleep_ms(5)

                    
                    self.release_keys()
                    time.sleep_ms(200)
                    
            else:
                time.sleep(2)
                


d = Device()
d.start()
