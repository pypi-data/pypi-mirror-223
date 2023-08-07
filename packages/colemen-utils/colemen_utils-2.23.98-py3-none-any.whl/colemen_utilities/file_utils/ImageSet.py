# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel
from threading import Thread
import asyncio
import hashlib
import json
from random import randint
import re
from typing import Union
import os
from re import L
import time
from dataclasses import dataclass
from typing import Dict, List,Union,Iterable
from PIL.Image import Image as pil_image
from PIL import Image as pil_img_mod
# from PIL import Image as pil_image

# from collections.abc import Iterable
import colemen_config as _config
import colemen_utilities.file_utils.File as _File


import colemen_utilities.string_utils as _csu
import colemen_utilities.dict_utils as _obj
import colemen_utilities.file_utils as _f
import colemen_utilities.directory_utils as _directory
import colemen_utilities.list_utils as _arr
import colemen_utilities.random_utils as _rand
import colemen_utilities.file_utils.Image as _image
import colemen_utilities.console_utils as _con







@dataclass
class ImageSet():
    _images=None



    def __init__(self,images):
        self._images = []

        self.add_image(images)


    @property
    def length(self):
        '''
            Get this ImageSet's length

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 08-05-2023 15:42:48
            `@memberOf`: ImageSet
            `@property`: length
        '''
        return len(self._images)

    def add_image(self,images:_config._image_type=None):
        images = _arr.force_list(images)
        for img in images:
            if isinstance(img,(str)):
                if _f.exists(img):
                    img = _image.Image(img)
                    self._images.append(img)
            if isinstance(img,_image.Image):
                self._images.append(img)

    def get_by_extension(self,ext:str):
        out = []
        for img in self._images:
            if img.has_extension(ext):
                out.append(img)
        return out

    @property
    def png(self)->Iterable[_config._image_type]:
        return self.get_by_extension("png")

    @property
    def jpg(self)->Iterable[_config._image_type]:
        return self.get_by_extension("jpg")

    def convert_to_png(self,delete_original=False):
        t = Thread(target=_parent_thread_convert_to_png,args=[self._images,delete_original])
        t.start()
        t.join()

        # threads = []
        # for img in self._images:
        #     t = Thread(target=_convert_to_png,args=[img,delete_original])
        #     threads.append(t)
        # for t in threads:
        #     t.start()
        # for t in threads:
        #     t.join()






def _parent_thread_convert_to_png(images,delete_original=False):
    threads = []
    for img in images:
        # t = Thread(target=_convert_to_png,args=[img,delete_original])
        threads.append(Thread(target=_convert_to_png,args=[img,delete_original]))
    [t.start() for t in threads]
    # [t.join() for t in threads]
    # return None


    while True:
        total = 0
        for t in threads:
            if t.is_alive() is False:
                total += 1
                # _con.log(f"total_complete: {total}        ","info",same_line=True)
                # print(f"total_complete: {total}")

        if total >= len(threads):
            return



    # for t in threads:

def _convert_to_png(image,delete_original=False):
    if image.has_extension("png"):
        return image

    new_path = f"{image.dir_path}/{image.name_no_ext}.png"
    # return new_image(new_path,orig_image=image)

    image.img.save(new_path)
    if _f.exists(new_path):
        png_image = image.copy_meta_to_file(new_path)
        if delete_original is True:
            image.delete()
        return png_image
    return False