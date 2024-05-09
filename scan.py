
import serial
from tkinter.filedialog import askopenfilename, asksaveasfilename
from common import path, DataFild
import os
import fnmatch
import sys
import glob

trace = print if False else lambda *x: None


class RS232:
    """Протокол обмена с ПУИ по RS 232
        baudrate = 4800 запрос <MR> ответ <OK> baudrate = 115200 запрос <N> передача по 16 байт
        ст б. глубины, мл б. глубины, день, месяц, час, мин, сек, широта 5 б., долгота 4 б. выход <O>
        всего 52224 б. глубина в двоичном виде в дециметрах остальное в десятичном виде"""

    def __init__(self, parent=None, byte_size=52224, dir_=None):
        self.parent = parent
        self.byte_size = byte_size
        if dir_ is None:
            self.dir_data = path.joinpath('data')
        else:
            if not os.path.exists(dir_):
                self.dir_data = path.joinpath('data')
            else:
                self.dir_data = dir_
        self.tty = None
        self.ok = None
        self._cancel = False
        self.filename = None
        parent.bind('<Escape>', self.cancel)

    def scan(self):
        """Сканируем порты и возврвщаем доступные в виде tuples (номер, имя) и в self.ok
        записываем имя порта на котором подключен ПУИ или None"""
        self.ok = None
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # это исключает ваш текущий терминал "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        trace(result)
        if result:
            for j in result:
                try:
                    self.tty = serial.Serial(j, timeout=0.3, baudrate='4800')
                    self.tty.reset_input_buffer()
                    self.tty.write(b"MR")
                    trace("-> MR")
                    if self.tty.read(2) == b'OK':
                        trace("<- OK")
                    else:
                        return
                    self.tty.baudrate = 115200
                    self.ok = self.tty.portstr          # COM1
                    self._cancel = True
                    trace(f':: {self.ok}')
                    break
                except serial.SerialException:
                    pass

    def cancel(self, arg=None):
        self._cancel = False

    def receiv_pui(self, f) -> int:
        """Принимаем из ПУИ bytesize данных по 16 байт и сохраняем их построчно в файле datapui#N.txt"""
        with open(f, 'w') as file:
            i = 0
            step = 1
            while i < self.byte_size:          # 52224 :50 = 1045
                i += 1
                self.tty.write(b'N')
                data = self.tty.read(16)
                if self._cancel:
                    new_data = self.parse_data(data)
                    file.write(new_data + '\n')
                    self.parent.update()
                    step += 1
                    if step == 1044:
                        self.parent.stbar.progress.step()
                        step = 0
                else:
                    trace('break')
                    break
            self.tty.write(b'O')
            trace("-> O")
            self.tty.close()
            self.tty = None
            return i

    @staticmethod
    def parse_data(data: bytes) -> str:
        """dat = 'глуб(2байта) день.месяц час:мин:сек широта(00.000.00) долгота(000.00.000)'"""
        # array.array('B', data).tolist() ord('A') == ord(b'A') == b'A'[0] = 65
        if len(data) != 16:
            return ""
        s = [i for i in data]
        d0 = int.from_bytes(s[0:2], 'big')
        d1 = int.from_bytes(s[8:10], 'big')
        d2 = int.from_bytes(s[11:13], 'big')
        d3 = int.from_bytes(s[14:16], 'big')
        dat = (f"{d0:05d} {s[2]:02x}.{s[3]:02x} {s[4]:02x}:{s[5]:02x}:{s[6]:02x} "
               f"{s[7]:02x}.{d1:03x}.{s[10]:02x} {d2:03x}.{s[13]:02x}.{d3:03x}")
        return dat

    @staticmethod
    def par_dir(dir_name) -> int:
        """Выбирает из директории наибольший номер файла datapui#N.txt"""
        items = [dir_.lower() for dir_ in os.listdir(dir_name) if
                 fnmatch.fnmatch(dir_.lower(), 'datapui#*.txt')]
        if items:
            lst = [int(i.split('.')[0].split('#')[-1]) for i in items]
            lst.sort()
            return lst[-1]
        return 0

    def save_file(self):
        """Вернуть путь к файлу"""
        l_num = self.par_dir(self.dir_data) + 1
        o_name = asksaveasfilename(initialdir=self.dir_data, initialfile=f'datapui#{l_num}.txt',
                                   filetypes=[("TXT files", ".txt")])
        if o_name:
            o_name = os.path.normpath(o_name)
            self.dir_data = os.path.split(o_name)[0]
            return o_name

    def open_file(self):
        """Вернуть путь к файлу"""
        v = self.par_dir(self.dir_data)
        ftypes = [('TXT files', '.txt'), ('CGF files', '.cgf'), ('All files', '*')]
        inifile = f'datapui#{v}' + '.txt' if v else 'datapui#0.txt'
        o_name = askopenfilename(initialdir=self.dir_data, filetypes=ftypes, initialfile=inifile)
        if o_name:
            o_name = os.path.normpath(o_name)
            self.dir_data = os.path.split(o_name)[0]
            return o_name

    def canvas_data(self, filename=None) -> list:
        """Формируем из файла datapui#N.txt данные для просмотра в виде
        data=[(gl0,'dat0','tm0','shir0','dolg0'),(gl1,'dat1','tm1','shir1'),'dolg1'),...
        (glN,'datN','tmN','shirN','dolgN')]"""
        if not filename:
            filename = self.open_file()
        if filename:
            data = []
            ds = DataFild()
            with open(filename) as file:
                self.filename = filename
                self.dir_data = os.path.split(filename)[0]
                for line in file:
                    line.rstrip()
                    s = line.split()                # ['глубина','день.месяц','ч:м:с',' широта','долгота']
                    try:
                        t = DataFild(int(s[0]), s[1], s[2], s[3], s[4])
                        data.append(t)
                    except (IndexError, ValueError):
                        data.append(ds)                  # не уменьшит длину данных 52224
                data.extend([ds]*(52224-len(data)))    # дописать данные до длины 52224 если файл короче
                return data

    def get_path(self):
        """Вернуть путь и имя файла с данными или None"""
        return self.filename, self.dir_data
