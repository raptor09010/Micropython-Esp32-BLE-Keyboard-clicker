# MicroPython BLE HID Keyboard Controller

This project turns an ESP32-S2 (or similar MicroPython-capable board with BLE support) into a **Bluetooth HID Keyboard**.  
Five input pins are monitored and mapped to various keyboard actions such as:

- Arrow keys  
- `Ctrl + Tab`  
- `Ctrl + Shift + Tab`  
- Sending characters  
- Sending strings

The device advertises itself as a standard BLE keyboard and works with Windows, macOS, Linux, Android, and iOS.

---

## ✨ Features
- BLE HID Keyboard using the `hid_services` library  
- Five GPIO-triggered key actions  
- Functions for single keys, shifted keys, and full string typing  
- Automatic advertising + reconnection  
- Example-friendly class design

---

## 🛠 Hardware Setup

| Pin | Action |
|-----|--------|
| GPIO 19 | Forward key → HID `0x4F` (Right Arrow) |
| GPIO 18 | Backward key → HID `0x50` (Left Arrow) |
| GPIO 17 | Second tab → `Ctrl + Tab` |
| GPIO 16 | First tab → `Ctrl + Shift + Tab` |
| GPIO 0  | "S" key |

All pins use **Pin.PULL_UP**, so each switch should short the pin to **GND** when pressed.

---

## 📦 Requirements

### MicroPython firmware with BLE support  
ESP32-S2 / ESP32-S3 recommended.

### Libraries  
Required modules:

- `hid_services`
- `machine`
- `time`

---

# ⌨️ Full HID Keyboard Key Code List

Below is a complete list of HID keyboard scan codes (0x00–0xE7).  
These can be used with:

```python
self.set_key(HID_CODE)
self.keyboard.set_modifiers(left_shift=1, left_control=1)
