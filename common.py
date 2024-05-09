#!/usr/bin/env python
import os.path
import pathlib
import sys
import tempfile
import customtkinter as ctk
from PIL import Image
import configparser
from ctkmessagebox import CTkMessagebox as Box
from dataclasses import dataclass


@dataclass
class DataFild:
    """Данные для холста"""
    glub: int = 0
    day: str = '00.00'
    time: str = '00:00:00'
    shir: str = '00.000.00'
    dolg: str = '000.00.000'


path = pathlib.Path(os.path.abspath("."))
bakdir = tempfile.mkdtemp()

img_path = path.joinpath("img")

config = configparser.ConfigParser()
file = path.joinpath('view_config.ini')

if not file.exists():
    Box(title="", message='Отсутствует \nили поврежден\nфайл view_config.ini',
        font=("Roboto Medium", -16), icon="cancel")
    sys.exit(0)


def read_config() -> None:
    """Прочитать файл конфигурации"""
    config.read(file, encoding='utf-8')


read_config()


def write_config() -> None:
    """Сохранение файла конфигурации"""
    with open(file, "w", encoding="utf-8") as config_file:
        config.write(config_file)


def load_image(im, im_2=None, size: tuple = ()) -> ctk.CTkImage:
    """Загрузить изображения"""
    path_to_image = img_path.joinpath(im)
    if not size:
        size = (20, 20)
    if im_2:
        path_to_image2 = img_path.joinpath(im_2)
        return ctk.CTkImage(
            light_image=Image.open(path_to_image),
            dark_image=Image.open(path_to_image2),
            size=size,
        )
    else:
        return ctk.CTkImage(Image.open(path_to_image), size=size)


im_dict = {}
im_list = ('pui', 'mem', 'print', 'pdf', 'link', 'exit', 'im16', 'tema', 'number',
           'grid', 'dno', 'avto', 'left', 'right', 'up', 'down', 'expand', 'man')

for name in im_list:
    im_dict[name] = load_image(f"{name}2.png", f"{name}.png", size=(20, 20))


if getattr(sys, "frozen", False):
    bundle_dir = sys._MEIPASS                           # PyInstaller
else:
    bundle_dir = path

imgdir = path.joinpath(bundle_dir, "img")

scheme = config.get('Sys', 'scheme')
family = config.get('Font', 'family')
font_size = config.getint('Font', 'size')
font_size_16 = config.getint('Font', 'size_16')
font_size_14 = config.getint('Font', 'size_14')
