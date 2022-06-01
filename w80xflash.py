import sys, serial, time
import logging
from xmodem import XMODEM1k


'''
ser = serial.Serial('/dev/cu.wchusbserial1410', baudrate=115200, timeout=None) # or whatever port you need
def getc(size, timeout=1):
    return ser.read(size) or None

def putc(data, timeout=1):
    return ser.write(data)  # note that this ignores the timeout

def proc_cb(total, succ, err):
    wmax = 40
    w = total>wmax and wmax or (total or 1)
    p = int((total+w-1)/w)
    if succ+err == 1:
        sys.stdout.write("pkgCnt=%s |%s|" % (total,'-'*w))
        sys.stdout.write('\b'*(w+1))
    elif succ+err == total:
        sys.stdout.write('*|\n')
    elif succ%p == 0:
        sys.stdout.write('*')
    else:
        sys.stdout.write(['\\','|','/','-'][succ%4])
        sys.stdout.write('\b')
    sys.stdout.flush()


print('RTS reboot')
sys.stdout.flush()
ser.rts = True
time.sleep(0.5)
ser.rts = False

for k in range(10):
    putc(b'\x1B')
    time.sleep(0.01)
time.sleep(0.5)
dat = ser.read(ser.in_waiting).decode('ascii')
if dat[-1] != 'C':
    sys.stderr.write('serial sync timeout\n')
    sys.exit()
print(dat.replace('C',''))


#logging.basicConfig(level=logging.DEBUG)
modem = XMODEM1k(getc, putc)
stream = open('/Users/zyy/Workspace/project/openluat/w80x/build_host/wm-sdk-w80x/bin/w800/w800.fls', 'rb')
ser.reset_input_buffer()
modem.send(stream, callback=proc_cb)
'''

class SerLoader(object):
    def __init__(self, port, baud, timeout=None):
        self.com = serial.Serial(port, baud, timeout=timeout)
        self.log = logging.getLogger('w80xflash')

    def reset(self, action='rts'):
        """reboot device"""
        self.com.rts = True
        time.sleep(0.5)
        self.com.rts = False

    def sync(self):
        """sync serial"""
        for k in range(10):
            self.putc(b'\x1B')
            time.sleep(0.01)
        dat = self.com.read(self.com.in_waiting).decode('ascii')
        if dat[-1] != 'C':
            sys.stderr.write('serial sync timeout\n')
            return False
        return dat.replace('C','')

    def erase(self):
        """erase device"""
        self.log.info('erase all')

    def download(self, fls):
        """flash device"""
        self.log.info('download: %s' % fls)
        self.reset()
        ack = self.sync()
        self.log.info('sync: %s' % ack)
        if ack:
            xmodem = XMODEM1k(
                lambda x,t=1:self.getc(x,t),
                lambda x,t=1:self.putc(x,t)
                )
            with open('/Users/zyy/Workspace/project/openluat/w80x/build_host/wm-sdk-w80x/bin/w800/w800.fls', 'rb') as stream:
                self.com.reset_input_buffer()
                xmodem.send(stream,
                    callback=lambda t,s,e:self.dlcb(t,s,e))

    def dlcb(self, total, succ, err):
        wmax = 40
        w = total>wmax and wmax or (total or 1)
        p = int((total+w-1)/w)
        if succ+err == 1:
            sys.stdout.write("pkgCnt=%s |%s|" % (total,'-'*w))
            sys.stdout.write('\b'*(w+1))
        elif succ+err == total:
            sys.stdout.write('*|\n')
        elif succ%p == 0:
            sys.stdout.write('*')
        else:
            sys.stdout.write(['\\','|','/','-'][succ%4])
            sys.stdout.write('\b')
        sys.stdout.flush()
    def getc(self, size, timeout=1):
        return self.com.read(size) or None
    def putc(self, data, timeout=1):
        return self.com.write(data)



def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="w80xflash - flash downloader of w80x/air101/air103/xt804.")

    group = parser.add_argument_group("port settings")
    group.add_argument(
        "-p", "--port",
        metavar="PORT",
        help="serial port name",
        default=None)
    group.add_argument(
        "-b", "--baud",
        metavar="PORT",
        help="set baud rate, default: %(default)s",
        default='115200')

    group = parser.add_argument_group("flash handling")
    group.add_argument(
        "-e", "--erase",
        action="store_true",
        help="erase all areas",
        default=False)
    group.add_argument(
        "-d", "--download",
        metavar="FILE",
        help="firmware to be download",
        default=None)

    args = parser.parse_args()

    if args.port is None:
        parser.error('port is not given')

    sl = SerLoader(args.port, args.baud)
    if args.erase:
        sl.erase()
    if args.download:
        sl.download(args.download)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
