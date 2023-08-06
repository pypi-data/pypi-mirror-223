"""pyperclipimg
By Al Sweigart al@inventwithpython.com

Cross-platform copy() and paste() Python functions for images."""

__version__ = '0.1.0'

import sys
import subprocess
import shutil
import os
import tempfile
from pathlib import Path

from PIL import Image, ImageGrab
import PIL

class PyperclipImgException(Exception):
    pass

def _get_image_from_arg_if_arg_is_filename(arg):
    if isinstance(arg, PIL.Image.Image):
        return arg  # Return the image object
    if isinstance(arg, (str, Path)):
        if not os.path.isfile(arg):
            raise PyperclipImgException('No file named ' + str(arg))
        try:
            return Image.open(arg)  # Get an Image object from the filename and return it.
        except PIL.UnidentifiedImageError:
            raise PyperclipImgException('File ' + str(arg) + ' is not an image file.')
    else:
        raise PyperclipImgException('arg ' + str(arg) + ' is not an Image or filename of an image.')


def _copy_windows(image):
    image = _get_image_from_arg_if_arg_is_filename(image)
    
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()



def _copy_macos(image):
    image = _get_image_from_arg_if_arg_is_filename(image)
    
    # Convert the Pillow image object to TIFF format
    output = io.BytesIO()
    image.save(output, format="TIFF")
    tiff_data = output.getvalue()
    output.close()

    # Create an NSImage from the TIFF data
    NSImage.alloc().initWithData_(tiff_data)

    # Create a bitmap representation
    image_rep = NSBitmapImageRep.alloc().initWithData_(tiff_data)

    # Set the image to the clipboard
    pasteboard = NSPasteboard.generalPasteboard()
    pasteboard.declareTypes_owner_([NSPasteboardTypeTIFF], None)
    pasteboard.setData_forType_(image_rep.TIFFRepresentation(), NSPasteboardTypeTIFF)


def _copy_linux_xclip(image):
    image = _get_image_from_arg_if_arg_is_filename(image)
    
    with tempfile.NamedTemporaryFile() as temp_file_obj:
        image.save(temp_file_obj.name)
        subprocess.Popen(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', temp_file_obj.name], close_fds=True)
          

def _copy_linux_wlcopy(image):
    image = _get_image_from_arg_if_arg_is_filename(image)
    
    with tempfile.NamedTemporaryFile() as temp_file_obj:
        image.save(temp_file_obj.name)
        with open(temp_file_obj.name, 'rb') as image_file:
            subprocess.run(['wl-copy'], stdin=image_file)  # Note that this code fails on Python 3.4 and before.


def paste():
    # ImageGrab.grabclipboard() is new in Pillow version 1.1.4: (Windows), 3.3.0 (macOS), 9.4.0 (Linux)
    return ImageGrab.grabclipboard()


if sys.platform == 'win32':
    import win32clipboard
    import io
    copy = _copy_windows

elif sys.platform == 'darwin':
    from Quartz import NSPasteboard, NSPasteboardTypeTIFF
    from Cocoa import NSImage, NSBitmapImageRep
    import io
    copy = _copy_macos

elif sys.platform == 'linux':
    if shutil.which('xclip'):
        copy = _copy_linux_xclip
    elif shutil.which('wl-copy'):
        copy = _copy_linux_wlcopy
    else:
        raise NotImplementedError('pyperclipimg on Linux requires the xclip or wl-copy command. Run either `sudo apt install xclip` or `sudo apt install wl-clipboard` and restart')

else:
    assert False, "Unrecognized platform " + sys.platform
