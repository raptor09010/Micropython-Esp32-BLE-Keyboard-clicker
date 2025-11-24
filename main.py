import time
from machine import Pin
from hid_services import Keyboard

class Device:
    def __init__(self, name="Keyboard"):
        # --- CONFIG TABLE (edit this to change buttons) ---
        self.actions = [
            # pin,        keycode, modifier
            (19, 0x4F, None),              # Forward → Right Arrow
            (18, 0x50, None),              # Backward → Left Arrow
            (17, 0x1F, "ctrl"),            # Ctrl + 2
            (16, 0x1E, "ctrl"),            # Ctrl + 1
            (0,  0x16, None),              # Key "S"
        ]
        # --------------------------------------------------

        # Load pins dynamically
        self.pins = []
        for pin_num, keycode, modifier in self.actions:
            self.pins.append(Pin(pin_num, Pin.IN, Pin.PULL_UP))

        # Create Bluetooth keyboard
        self.keyboard = Keyboard(name)
        self.keyboard.set_state_change_callback(self.keyboard_state_callback)
        self.keyboard.start()

    # BLE state changes (unused but required)
    def keyboard_state_callback(self):
        pass

    def advertise(self):
        self.keyboard.start_advertising()

    def stop_advertise(self):
        self.keyboard.stop_advertising()

    def release_keys(self):
        self.keyboard.set_keys()
        self.keyboard.set_modifiers()
        self.keyboard.notify_hid_report()

    def send(self, keycode, modifier):
        # Apply modifiers
        if modifier == "ctrl":
            self.keyboard.set_modifiers(left_control=1)
        elif modifier == "shift":
            self.keyboard.set_modifiers(left_shift=1)
        elif modifier == "ctrl-shift":
            self.keyboard.set_modifiers(left_control=1, left_shift=1)
        else:
            self.keyboard.set_modifiers()

        # Send key
        self.keyboard.set_keys(keycode)
        self.keyboard.notify_hid_report()
        time.sleep_ms(5)

        # Release
        self.release_keys()
        time.sleep_ms(200)

    # MAIN LOOP
    def start(self):
        self.advertise()
        while True:
            if self.keyboard.get_state() == Keyboard.DEVICE_CONNECTED:
                for i, (pin_num, keycode, modifier) in enumerate(self.actions):
                    if not self.pins[i].value():  
                        self.send(keycode, modifier)
            else:
                time.sleep(2)
d = Device()
d.start()


