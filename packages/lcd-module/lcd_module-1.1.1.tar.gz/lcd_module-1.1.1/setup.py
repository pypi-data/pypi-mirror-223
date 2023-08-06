from setuptools import setup

setup(
    name='lcd_module',
    version='1.1.1',
    description='A module to control the LCD display via I2C.',
    py_modules=['lcd_module'],
    install_requires=[
        'smbus2',  # Install the 'smbus2' package for I2C communication
        'RPLCD',   # Install the 'RPLCD' package for the LCD library
    ],
)
