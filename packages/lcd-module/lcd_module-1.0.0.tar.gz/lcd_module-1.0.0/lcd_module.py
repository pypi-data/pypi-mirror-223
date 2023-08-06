# lcd_module.py

import smbus
from RPLCD.i2c import CharLCD

I2C_BUS = 1
I2C_ADDRESS = 0x3F
LCD_COLUMNS = 16
LCD_ROWS = 2

bus = smbus.SMBus(I2C_BUS)
lcd = CharLCD(i2c_expander='PCF8574', address=I2C_ADDRESS, port=1, cols=LCD_COLUMNS, rows=LCD_ROWS)

def display_menu(menu_items, current_item):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Menu:")

    lcd.cursor_pos = (1, 0)
    lcd.write_string(menu_items[current_item])

def display_text(line1, line2=""):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1)

    if line2:
        lcd.cursor_pos = (1, 0)
        lcd.write_string(line2)