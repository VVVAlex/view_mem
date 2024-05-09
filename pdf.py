#!/usr/bin/env python
import os.path
import time
import pathlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics, ttfonts
from common import imgdir, bakdir

# import sys, subprocess

#  система координат x0, y0 левый нижний угол x1, y1 правый верхний угол


class Pdf:
    """Создание и печать pdf документа"""
    # w=768, data=None, src=None, scale = None, filename=None, verbose=None
    def __init__(self, master, verbose):
        self.master = master            # show_bso
        self.w, self.data, self.scr, self.scale, self.name = self.master.get_pdf_data()
        self.W = 756.0              # слева на право 768.0
        self.H = 450                # снизу вверх                   # 400 !!!
        self.dx = 30                # слева
        self.dy = 90                # снизу
        self.stic = 7               # засечка на осях
        self.dl = 15                # удление надписий от осей
        self.k = self.W / self.w
        self.list_scale = [(0, 2.0), (1, 1.0), (2, 0.4), (3, 0.2), (4, 0.1), (5, 0.05),
                           (6, 0.02), (7, 0.01), (8, 4/600)]            # (10, 0.005), (11, 0.004) 8 и 10км
        my_font_object = ttfonts.TTFont('Arial', 'arial.ttf')
        pdfmetrics.registerFont(my_font_object)
        self.dir = '.'
        cur_path = pathlib.Path('temp.pdf')
        self.tmp_name = cur_path.joinpath(bakdir, cur_path)
        if self.data:
            # name = os.path.join(bakdir, 'temp.pdf')
            # self.c = canvas.Canvas("temp.pdf", pagesize=landscape(A4))  # файл "temp.pdf" в текущем каталоге
            self.c = canvas.Canvas(f"{self.tmp_name}", pagesize=landscape(A4))
            # print(self.c.getAvailableFonts())                         # все зарегистрированные шрифты
            self.asix()
            self.grid()
            self.c.setFillColor('darkblue')
            self.c.drawString(self.dx + self.W + self.dl, self.dy + self.H - 5, "0")
            self.data_pdf()
            self.pasteimg()
            self.run()
            self.go(verbose)

    def pasteimg(self) -> None:
        """Рисуем кораблик и логотип"""
        file = os.path.join(imgdir, 'korabl.gif')
        self.c.drawInlineImage(file, self.W, self.dy // 2 - 20, 48, 24)    # 5

    def data_pdf(self) -> None:
        """Рисуем данные в масштабе, масштаб, как и в просмоторщеке
        'глубина','амплитуда','%d.%m.%y %H:%M:%S','широта','долгота'
        """
        w, h, dx, dy = self.W, self.H, self.dx, self.dy
        dat = [i.glub / 1.0 for i in self.data]             # глубина [1]
        scal = ([5, 10, 15, 20], [10, 20, 30, 40], [25, 50, 75, 100], [50, 100, 150, 200], [100, 200, 300, 400],
                [200, 400, 600, 800], [500, 1000, 1500, 2000], [1000, 2000, 3000, 4000],
                [1500, 3000, 4000, 6000])               # [2000, 4000, 6000, 8000], [2500, 5000, 7500, 10000]
        j, n = self.list_scale[self.scale] if self.scale else self.list_scale[0]
        self.c.saveState()
        self.c.setDash([])
        self.c.setFont('Helvetica', 10)
        self.xy_dat(scal[j])
        self.c.restoreState()
        for i in range(self.w):
            if i >= len(self.data):
                break  # если данных меньше чем w, то будет except
            if dat[i]:                    # 10km
                if dat[i] <= 100000 and dat[i] <= scal[j][-1] * 10:   # выкидываю > 10км,
                    # чтобы не вылезало за ось снизу и подрезка выпадающих за низ холста
                    self.c.setFillColor('red')
                    self.c.setStrokeColor('red')
                    self.c.circle(dx + w - i * self.k - 1, dy + h - round(dat[i] * n) * h / 400,      #
                                  0.80, stroke=0, fill=1)
            self.c.saveState()
            self.c.setDash([])
        self.c.setFillColor('#444')
        self.c.setFont('Arial', 11)
        self.c.drawString(dx * 1.2, dy // 2 - 12, self.info())    # 2

    @staticmethod
    def txt_time(t) -> str:
        """Возвращает отформатированное время"""
        return time.strftime('%H:%M', t)

    def xy_dat(self, y_scal) -> None:
        """Подпись по оси Y и X"""
        w, h, dx, dy, dl = self.W, self.H, self.dx, self.dy, self.dl
        x_string = []
        d_y = 3
        self.c.drawString(dx + w + dl, dy + h * 3 // 4 - d_y, str(y_scal[0]))         # Y
        self.c.drawString(dx + w + dl, dy + h // 2 - d_y, str(y_scal[1]))
        self.c.drawString(dx + w + dl, dy + h // 4 - d_y, str(y_scal[2]))
        self.c.drawString(dx + w + dl, dy - d_y, str(y_scal[3]))
        for i, j, x in ((0, 0, 0), (self.w // 4, 1, w // 4), (self.w // 2, 2, w // 2),
                        (self.w * 3 // 4, 3, w * 3 // 4), (self.w - 1, 4, w - 1)):
            try:
                s = self.data[i].day + " / " + self.data[i].time[:5]  # дата / время
                x_string.append(s)
            except IndexError:
                x_string.append('')
            self.c.drawCentredString(dx + w - x, dy - dl - 2, x_string[j])         # X

    def asix(self) -> None:
        """Рисуем оси"""
        w, h, dx, dy = self.W, self.H, self.dx, self.dy
        self.c.setLineWidth(2.0)
        self.c.line(dx + w, dy, dx + self.W, dy + h)                   # Y
        self.c.line(dx, dy + h, dx + self.W, dy + h)                   # X сверху
        self.c.line(dx, dy, dx + self.W, dy)                           # X_ снизу
        for i in [0, h // 4, h // 2, h * 3 // 4, h]:
            self.c.line(dx + w, dy + i, dx + w + self.stic, dy + i)
        for i in [0, w // 4, w // 2, w * 3 // 4, w]:
            self.c.line(dx + i, dy, dx + i, dy - self.stic)

    def grid(self) -> None:
        """Рисуем сетку"""
        w, h, dx, dy = self.W, self.H, self.dx, self.dy
        self.c.setLineWidth(0.5)
        self.c.setDash([1, 2])
        self.c.grid([dx, w // 4 + dx, w // 2 + dx, w * 3 // 4 + dx,
                     w + dx], [dy, h // 4 + dy, h // 2 + dy, h * 3 // 4 + dy, h + dy])

    def info(self) -> str:
        """Формируем строку info"""
        if self.scr is None:
            self.scr = '*'
        # st = time.ctime(time.time())
        # locale.setlocale(locale.LC_ALL, "Russian_Russia.1251")        #####
        # s = "%A %d %B %Y %H:%M:%S"
        s = "%d %B %Y %H:%M:%S"
        st = time.strftime(s)
        istr = f"Файл = {self.name},  экран = {self.scr},  {st}"
        return istr

    def run(self) -> None:
        """Сохранить pdf файл на диск"""
        self.c.showPage()
        self.c.save()

    def go(self, verbose) -> None:
        command = 'open' if verbose else 'print'
        try:
            # os.startfile('temp.pdf', command)
            # cur_path = pathlib.Path('temp.pdf')
            # name = cur_path.joinpath(bakdir, cur_path)
            os.startfile(f'{self.tmp_name}', command)
        except OSError:
            pass
