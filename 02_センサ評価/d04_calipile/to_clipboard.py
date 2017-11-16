# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:05:10 2016

@author: p000495138
"""

from io import StringIO
from time import sleep

from PIL import Image
import win32clipboard


def copy2clipboard(fig=None):
    '''
    copy a matplotlib figure to clipboard as BMP on windows
    http://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard
    '''
    if not fig:
        fig = gcf()
    
    output = StringIO()
    # fig.savefig(output, format='bmp') # bmp not supported
    buf = fig.canvas.buffer_rgba()
    w = int(fig.get_figwidth() * fig.dpi)
    h = int(fig.get_figheight() * fig.dpi)
    im = Image.frombuffer('RGBA', (w,h), buf)
    im.transpose(Image.FLIP_TOP_BOTTOM).convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:] # The file header off-set of BMP is 14 bytes
    output.close()

    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        # win32clipboard.SetClipboardData(win32clipboard.CF_BITMAP, data) # did not work!
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data) # DIB = device independent bitmap 
        win32clipboard.CloseClipboard()
    except:
        sleep(0.2)
        copy2clipboard(fig)
