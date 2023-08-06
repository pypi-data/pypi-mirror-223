import smbus
from RPLCD.i2c import CharLCD
import time

# I2C bus number (check with 'i2cdetect -y 1' command in the terminal)
I2C_BUS = 1

# I2C address of the LCD
I2C_ADDRESS = 0x3F

# LCD dimensions (number of columns and rows)
LCD_COLUMNS = 16
LCD_ROWS = 2

# Initialize the I2C bus
bus = smbus.SMBus(I2C_BUS)

# Initialize the LCD using the I2C expander (pcf8574)
lcd = CharLCD(i2c_expander='PCF8574', address=I2C_ADDRESS, port=1, cols=LCD_COLUMNS, rows=LCD_ROWS)

def scroll_text(text, line=0, delay=0.5):
    """
    Scroll text on the LCD screen.

    Args:
        text (str): Text to display and scroll.
        line (int): Line number (0 or 1) where the scrolling text should start. Default is 0.
        delay (float): Delay between scroll steps in seconds. Default is 0.5 seconds.
    """
    lcd.cursor_pos = (line, 0)
    lcd.write_string(text[:LCD_COLUMNS])

    while len(text) > LCD_COLUMNS:
        time.sleep(delay)
        text = text[1:] + text[0]
        lcd.cursor_pos = (line, 0)
        lcd.write_string(text[:LCD_COLUMNS])

    lcd.cursor_pos = (line, 0)
    lcd.write_string(text[:LCD_COLUMNS].ljust(LCD_COLUMNS))

def display_text(line1, line2=""):
    """
    Display text on the LCD screen.

    Args:
        line1 (str): Text to display on the first line.
        line2 (str): Text to display on the second line. (optional)
    """
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1)

    if line2:
        lcd.cursor_pos = (1, 0)
        lcd.write_string(line2)

    # If line1 or line2 is longer than LCD_COLUMNS, scroll the text
    if len(line1) > LCD_COLUMNS:
        scroll_text(line1, line=0)

    if len(line2) > LCD_COLUMNS:
        scroll_text(line2, line=1)
