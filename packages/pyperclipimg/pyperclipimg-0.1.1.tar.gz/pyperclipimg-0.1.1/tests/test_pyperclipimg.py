from __future__ import division, print_function
import os
import pytest
import pyperclipimg
import pyperclip
from PIL import Image
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/'

def same_images(image1, image2):
    if image1.size != image2.size or image1.mode != image2.mode:
        return False

    pixels1 = image1.getdata()
    pixels2 = image2.getdata()

    for pixel1, pixel2 in zip(pixels1, pixels2):
        if pixel1 != pixel2:
            return False    
    return True

def test_basic():
    zophie_face_png_im = Image.open(THIS_FOLDER + 'zophie_face.png')
    zophie_face_jpg_im = Image.open(THIS_FOLDER + 'zophie_face.jpg')

    # png str filename
    pyperclip.copy('wipe old contents')
    pyperclipimg.copy(THIS_FOLDER + 'zophie_face.png')
    pasted = pyperclipimg.paste()
    assert same_images(pasted, zophie_face_png_im)

    # jpg str filename
    pyperclip.copy('wipe old contents')
    pyperclipimg.copy(THIS_FOLDER + 'zophie_face.jpg')
    pasted = pyperclipimg.paste()
    assert same_images(pasted, zophie_face_jpg_im)

    # png Path filename
    pyperclip.copy('wipe old contents')
    pyperclipimg.copy(Path(THIS_FOLDER + 'zophie_face.png'))
    pasted = pyperclipimg.paste()
    assert same_images(pasted, zophie_face_png_im)

    # jpg Path filename
    pyperclip.copy('wipe old contents')
    pyperclipimg.copy(Path(THIS_FOLDER + 'zophie_face.jpg'))
    pasted = pyperclipimg.paste()
    assert same_images(pasted, zophie_face_jpg_im)

    # png Image
    pyperclip.copy('wipe old contents')
    im = Image.open(THIS_FOLDER + 'zophie_face.png')
    pyperclipimg.copy(im)
    pasted = pyperclipimg.paste()
    assert same_images(pasted, zophie_face_png_im)

    # jpg Image
    pyperclip.copy('wipe old contents')
    im = Image.open(THIS_FOLDER + 'zophie_face.jpg')
    pyperclipimg.copy(im)
    pasted = pyperclipimg.paste()
    assert same_images(pasted, zophie_face_jpg_im)

if __name__ == "__main__":
    pytest.main()
