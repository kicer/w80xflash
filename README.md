# w80xflash

Flash downloader for w800/w806/air101/air103/xt804 devices with xmodem 1k.


## Usage

```
# python w80xflash.py -p /dev/cu.wchusbserial1410 -d <filename> -r

usage: w80xflash.py [-h] [-p PORT] [-b PORT] [-e SIZE] [-d FILE] [-r]

w80xflash - flash downloader of w80x/air101/air103/xt804.

optional arguments:
  -h, --help            show this help message and exit

port settings:
  -p PORT, --port PORT  serial port name
  -b PORT, --baudrate PORT
                        set baudrate, default: 921600

flash handling:
  -e SIZE, --erase SIZE
                        erase flash, size: 1M,2M
  -d FILE, --download FILE
                        firmware to be download
  -r, --reboot          reboot to run
```


## xmodem

Thanks for [xmodem 0.4.6](https://pypi.org/project/xmodem/)
