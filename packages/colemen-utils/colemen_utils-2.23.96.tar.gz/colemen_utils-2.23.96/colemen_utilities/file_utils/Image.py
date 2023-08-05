# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel
import hashlib
import json
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


'''
IPTC NEWSCODES:
    - https://www.iptc.org/std/NewsCodes/treeview/mediatopic/mediatopic-en-GB.html
    - https://cv.iptc.org/newscodes/mediatopic/

'''


class MetaKeys:


    # from PIL import Image as _pil_image
    copyright = ["IPTC:CopyrightNotice","XMP:Rights"]
    comment = ["EXIF:UserComment","EXIF:XPComment","XMP:UserComment"]
    authors = ["XMP:Creator","IPTC:By-line","EXIF:Artist"]
    description = ["EXIF:ImageDescription","XMP:Description","IPTC:Caption-Abstract","XMP:Caption"]
    instructions = ["XMP:Instructions","IPTC:SpecialInstructions"]
    title = ["XMP:Title","IPTC:ObjectName"]
    subject = ["EXIF:XPSubject"]
    headline = ["XMP:Headline","IPTC:Headline"]
    source = ["XMP:Source","IPTC:Source"]
    credits = ["XMP:Credit","IPTC:Credit"]
    job_identifier = ["XMP:TransmissionReference","IPTC:OriginalTransmissionReference"]
    legal_url = ["XMP:WebStatement"]
    usage_terms = ["XMP:UsageTerms"]
    job_title = ["XMP:AuthorsPosition","IPTC:By-lineTitle"]
    address = ["XMP:CreatorAddress"]
    city = ["XMP:CreatorCity"]
    region = ["XMP:CreatorRegion"]
    postal_code = ["XMP:CreatorPostalCode"]
    country = ["XMP:CreatorCountry"]
    phone = ["XMP:CreatorWorkTelephone"]
    email = ["XMP:CreatorWorkEmail"]
    creator_url = ["XMP:CreatorWorkURL"]









@dataclass
class Image(_File.File):
    name:str=None
    '''The file name of this image with the file extension'''
    name_no_ext:str=None
    '''The file name of this image without the file extension'''
    file_path:str=None
    dir_path:str=None
    extension:str=None
    synonyms:list=None
    changes_made:bool=False
    _tags:List=None
    _meta:Dict=None
    _created = time.time()
    _modified:bool = False
    _format_tags:bool = False
    _stable_diffusion_data:dict = None
    _synonyms_applied:str = None
    _original_tags_hash:str = None
    '''The sha256 hash of the tags when this image was imported'''
    _content_hash:str = None
    _img:pil_image = None
    _width:int = None
    _height:int = None
    _orientation:str = None
    _area:int = None



    _address:str = None
    _authors:str = None
    _city:str = None
    _comment:str = None
    _copyright:str = None
    _country:str = None
    _creator_url:str = None
    _credits:str = None
    _description:str = None
    _email:str = None
    _headline:str = None
    _instructions:str = None
    _job_identifier:str = None
    _job_title:str = None
    _legal_url:str = None
    _phone:str = None
    _postal_code:str = None
    _region:str = None
    _source:str = None
    _subject:str = None
    _title:str = None
    _usage_terms:str = None


    def __init__(self,file:dict=None,file_path:str=None):
        self.settings = {}
        self.data = {}

        if file is None and file_path is not None:
            if _f.exists(file_path) is False:
                raise ValueError("You must provide a file dictionary or file_path")
            files = _get_meta([_f.get_data(file_path)])
            file= files[0]
        if file is not None:
            file_path = _obj.get_arg(file,["file_path","SourceFile"],None)
        super().__init__(file_path)
            # print(f"file: {file}")
        self._meta = file
        self._tags = _arr.force_list(_obj.get_arg(file,['IPTC:Keywords'],[],None))
        # self._copyright = _obj.get_arg(file,self._get_meta_tags("copyright"),"",None)
        # self._comment = _obj.get_arg(file,self._get_meta_tags("comment"),"",None)
        # self._copyright = _arr.force_list(_obj.get_arg(file,MetaKeys.copyright,[],None))
        # self._comment = _arr.force_list(_obj.get_arg(file,COMMENT,[],None))
        self._original_tags_hash = _csu.to_hash(self._tags)
        self.file_path = file['SourceFile']
        self.name = file['File:FileName']
        self.name_no_ext = _f.get_name_no_ext(file['SourceFile'])
        self.dir_path = file['File:Directory']
        self.extension = _f.get_ext(file['SourceFile'])

    @property
    def summary(self):
        '''
            Get this Image's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-21-2023 08:08:29
            `@memberOf`: Image
            `@property`: summary
        '''
        value = {
            "name":self.name,
            "name_no_ext":self.name_no_ext,
            "file_path":self.file_path,
            "dir_path":self.dir_path,
            "extension":self.extension,
            "tags":self._tags,
            "_meta":self._meta,
            "_created":self._created,
            "_modified":self._modified,
            "_format_tags":self._format_tags,
            "comment":self.comment,
            }
        return value

    def save(self,force=False):
        '''
            Save this image if changes have been made

            ----------

            Arguments
            -------------------------
            [`force`=False] {bool}
                If True, the image will be saved regardless of if changes have been made.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:11:33
            `memberOf`: Image
            `version`: 1.0
            `method_name`: save
            * @xxx [02-21-2023 10:12:38]: documentation for save
        '''

        if self.changes_made is True or force is True:
            # @Mstep [] retrieve all tag keys and the values from this instance.
            tags = self._meta_key_props()
            tags["Keywords"]= self._tags

            from exiftool import ExifToolHelper
            with ExifToolHelper() as et:
                # print(f"self._tags: {self._tags}")
                self.img.close()
                et.set_tags(
                    [self.path],
                    tags=tags
                    # tags={
                    #     "Keywords": self._tags,
                    #     "CopyrightNotice": self._copyright,
                    #     "UserComment": self._comment,
                    #     "XMP:CreatorAddress": self._address,

                    #     }
                )
            self.clean()

    @property
    def content_hash(self):
        '''
            Get this Image's content_hash

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-10-2023 11:27:07
            `@memberOf`: Image
            `@property`: content_hash
        '''
        value = self._content_hash
        if value is None:

            # if self._img is None:
            #     self._img = Image.open(self.path)
            value = _csu.md5(str(self.img.tobytes()))
            # value = _csu.to_hash(str(img.tobytes()))
            # value = hashlib.md5(str(img.tobytes()))
            self._content_hash = value
        return value

    @property
    def img(self)->pil_image:
        '''
            Get this Image's img

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-11-2023 07:56:18
            `@memberOf`: Image
            `@property`: img
        '''
        value = self._img
        if value is None:
            value = pil_img_mod.open(self.path)
            self._img = value
        return value



    @property
    def width(self):
        '''
            Get this Image's width

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-11-2023 07:56:54
            `@memberOf`: Image
            `@property`: width
        '''

        value = self._width
        if value is None:
            value = self.img.width
            self._width = value
        return value

    @property
    def height(self):
        '''
            Get this Image's height

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-11-2023 07:56:54
            `@memberOf`: Image
            `@property`: height
        '''

        value = self._height
        if value is None:
            value = self.img.height
            self._height = value
        return value

    @property
    def area(self):
        '''
            Get this Image's area

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-11-2023 10:24:24
            `@memberOf`: Image
            `@property`: area
        '''
        value = self._area
        if value is None:
            value = self.width * self.height
            self._area = value
        return value

    def smaller_than(self,width,height):
        if self.width < width and self.height < height:
            return True
        return False

    def bigger_than(self,width,height):
        if self.orientation in ["landscape","square"]:
            if self.width > width:
                return True
        if self.orientation in ["portrait"]:
            if self.height > height:
                return True

        # if self.width > width and self.height > height:
            # return True
        return False

    @property
    def orientation(self):
        '''
            Get this Image's orientation

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 07-11-2023 08:04:43
            `@memberOf`: Image
            `@property`: orientation
        '''
        value = self._orientation
        if value is None:
            if self.width > self.height:
                value = "landscape"
            if self.width < self.height:
                value = "portrait"
            if self.width == self.height:
                value = "square"

            self._orientation = value
        return value


    @property
    def tags_hash(self):
        '''
            Get this Image's tags_hash
            Generate a sha256 hash of the current tag list.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-22-2023 08:19:23
            `@memberOf`: Image
            `@property`: tags_hash
        '''
        value = _csu.to_hash(self._tags)
        return value




    def format_tags(self):
        '''Format all tags to be in snake case.'''
        if self._format_tags is True:
            return

        tags = []
        for tag in self._tags:
            tags.append(_csu.to_snake_case(tag))
        self._tags = tags
        self._format_tags = True

    def has_tag(self,tag:Union[str,list],regex:bool=False,match_all:bool=False):
        '''
            Check if this image has a matching tag or matches one of many tags.

            ----------

            Arguments
            -------------------------
            `tag` {str,list}
                The tag or list of tags to search for.
                This can also be a comma delimited list of tags.

            [`regex`=False] {bool}
                if True, the tag will use regex for searching.

            [`match_all`=False] {bool}
                if True, the image must contain all tags provided in order to pass.

            Return {bool}
            ----------------------
            True if this image contains the search tag(s), False otherwise

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:15:17
            `memberOf`: Image
            `version`: 1.0
            `method_name`: has_tag
            * @xxx [02-21-2023 10:23:20]: documentation for has_tag
        '''
        self.format_tags()
        if "," in tag:
            tag = tag.split(",")
        tags = _arr.force_list(tag)
        has_tag = False
        for tag in tags:
            if "|" in tag:
                options = tag.split("|")
                for o in options:
                    o = _csu.strip(o," ")
                    snake_tag = _csu.to_snake_case(o)
                    # print(f"snake_tag:{snake_tag}")
                    # print(f"self._tags:{self._tags}")
                    if snake_tag in self._tags:
                        has_tag = True
                continue

            tag = _csu.strip(tag," ")
            if len(tag) == 0:
                continue
            if regex is True:
                for tg in self._tags:
                    if len(re.findall(tag,tg)) > 0:
                        has_tag = True

            else:
                snake_tag = _csu.to_snake_case(tag)
                # print(f"snake_tag:{snake_tag}")
                # print(f"self._tags:{self._tags}")
                if snake_tag in self._tags:
                    has_tag = True

            if match_all is True:
                if has_tag is False:
                    return False
        return has_tag

    def add_tag(self,tag:Union[str,list]):
        '''
            Add a new tag to this image.
            ----------

            Arguments
            -------------------------
            `tag` {str}
                The tag to add.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:24:49
            `memberOf`: Image
            `version`: 1.0
            `method_name`: add_tag
            * @xxx [02-21-2023 10:25:13]: documentation for add_tag
        '''
        self.format_tags()
        tags = _arr.force_list(tag)
        tags = [_csu.to_snake_case(x) for x in tags]
        new_tags = []
        for tag in tags:
            if tag not in self._tags:
                new_tags.append(tag)
        if len(new_tags) > 0:
            self._tags = self._tags + new_tags
            self.changes_made = True

        # new_tags = _arr.remove_duplicates(self._tags + tag)
        # if _csu.to_hash(self._tags) != _csu.to_hash(new_tags):

    def remove_tag(self,tag):
        '''
            Remove a tag from the file.
            ----------

            Arguments
            -------------------------
            `tag` {str}
                The tag to remove

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:13:08
            `memberOf`: Image
            `version`: 1.0
            `method_name`: remove_tag
            * @xxx [02-21-2023 10:13:40]: documentation for remove_tag
        '''
        self.format_tags()
        tag = _arr.force_list(tag)
        tag = [_csu.to_snake_case(x) for x in tag]
        tags = []
        for tg in self._tags:
            if tg not in tag:
                tags.append(tg)
                self.changes_made = True
        # tag = [x not in tag for x in self._tags]
        self._tags = tags

    def replace_tag(self,tag,replace,regex:bool=False,partial_match:bool=False):
        '''
            Replace a tag on this image.
            ----------

            Arguments
            -------------------------
            `tag` {str}
                The tag value to replace

            `repalce` {str}
                The value to replace the matching tag with.

            [`regex`=False] {bool}
                if True, the tag will use regex for searching.

            [`partial_match`=False] {bool}
                if True, the search tag can be found as a part of a tag.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:25:21
            `memberOf`: Image
            `version`: 1.0
            `method_name`: replace_tag
            * @xxx [02-21-2023 10:38:11]: documentation for replace_tag
        '''
        # @Mstep [] force the search tag to be a list.
        if "," in tag:
            tag = tag.split(",")
        tags = _arr.force_list(tag)

        # @Mstep [] format the already existing tags.
        self.format_tags()
        # @Mstep [] convert the replacement to snake case.
        replace = _csu.to_snake_case(replace)
        # tag = _arr.force_list(tag)
        # tag = [_csu.to_snake_case(x) for x in tag]
        new_tags = []

        tag:str
        # @Mstep [LOOP] iterate the tag search list
        for tag in tags:
            otg:str
            # @Mstep [LOOP] iterate this images tags.
            for otg in self._tags:
                # @Mstep [ELSE] if regex is True
                if regex is True:
                    # @Mstep [IF] if the regex matches.
                    if len(re.findall(tag,otg)) > 0:
                        # @Mstep [] push the replacement
                        new_tags.append(replace)
                    # @Mstep [IF] if the regex matches nothing.
                    else:
                        # @Mstep [] push the original
                        new_tags.append(otg)
                # @Mstep [ELSE] if regex is False.
                else:
                    tag = _csu.to_snake_case(tag)
                    if partial_match is False:
                        # @Mstep [IF] if the tag matches the original exactly.
                        if otg == tag:
                            # @Mstep [] push the replacement
                            new_tags.append(replace)
                        # @Mstep [IF] if the tag does not match the original exactly.
                        else:
                            # @Mstep [] push the original
                            new_tags.append(otg)
                    # @Mstep [ELSE] if partial_match is True
                    else:
                        # @Mstep [IF] if the tag is contained in the original tag.
                        if tag in otg:
                            # @Mstep [] push the replacement
                            new_tags.append(replace)
                        else:
                            # @Mstep [] push the original
                            new_tags.append(otg)


        # @Mstep [IF] if new_tags has changed
        if new_tags != self._tags:
            # @Mstep [] update the _tags property
            self._tags = new_tags
            # @Mstep [] set changes_made to True.
            self.changes_made = True

    def tag_commands(self,tag:Union[str,list]):
        self.format_tags()
        if "," in tag:
            tag = tag.split(",")
        tag = _arr.force_list(tag)
        add_tags = []
        remove_tags = []
        for tg in tag:
            if tg[0] == "-":
                tg = re.sub(r"^-","",tg)
                remove_tags.append(tg)
                # c.con.log(f"    removing tag: {tg}","red")
            else:
                add_tags.append(tg)
                # c.con.log(f"    adding tag: {tg}","green")
        add_tags = [x for x in add_tags if x not in self._tags]
        if len(add_tags) > 0:
            self.add_tag(add_tags)

        remove_tags = [x for x in remove_tags if x in self._tags]
        if len(remove_tags) > 0:
            self.remove_tag(remove_tags)

    def clean(self):
        '''
            The exif tool will create a backup copy of this image, this method will
            delete that file.

            ----------


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:38:23
            `memberOf`: Image
            `version`: 1.0
            `method_name`: clean
            * @xxx [02-21-2023 10:39:03]: documentation for clean
        '''
        if _f.exists(f"{self.file_path}_original"):
            _f.delete(f"{self.file_path}_original")

    def delete(self,shred:bool=False):
        '''
            Delete this image.
            ----------

            Arguments
            -------------------------
            [`shred`=False] {bool}
                If True, this image will be shredded and securely deleted.
                This is obviously a slower process than normal deletion.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:39:13
            `memberOf`: Image
            `version`: 1.0
            `method_name`: delete
            * @xxx [02-21-2023 10:40:41]: documentation for delete
        '''
        self.format_tags()
        _f.delete(self.file_path,shred=shred)

    def apply_synonyms(self):
        '''
            Apply synonyms to this file's tags

            ----------


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-21-2023 10:41:24
            `memberOf`: Image
            `version`: 1.0
            `method_name`: apply_synonyms
            * @xxx [02-21-2023 10:41:55]: documentation for apply_synonyms
        '''
        if self._synonyms_applied != self.tags_hash:
            for syn in self.synonyms:
                if len(syn) == 2:
                    if self.has_tag(syn[0],regex=True):
                        # c.con.log(f"    Synonym Found: {syn[0]}    ","magenta invert")
                        self.tag_commands(syn[1])
            if self.is_stable_diffusion_render:
                if self.has_tag("stable_diffusion") is False:
                    self.add_tag("stable_diffusion")
            self._synonyms_applied = self.tags_hash

    def move(self,new_directory:str):
        new_path = _csu.file_path(f"{new_directory}/{self.name}")
        # print(f"move.new_path:{new_path}")
        _f.move(self.file_path,new_path)
        self.file_path = new_path
        self.dir_path = new_directory

    def copy(self,new_directory:str)->_config._image_type:
        new_path = _csu.file_path(f"{new_directory}/{self.name}")
        # print(f"copy.new_path:{new_path}")
        _f.copy(self.file_path,new_path)
        # new_image = Image(file_path=new_path)
        # new_image._tags = self.tags
        # new_image._meta = self._meta
        new_image = self.copy_meta_to_file(new_path)
        return new_image

    def copy_meta_to_file(self,file_path:str):
        '''
            Copy this files meta data to another file.
            ----------

            Arguments
            -------------------------
            `file_path` {str}
                The path to the subject file that will have its meta data overwritten.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-22-2023 13:00:41
            `memberOf`: Image
            `version`: 1.0
            `method_name`: copy_meta_to_file
            * @xxx [02-22-2023 13:01:30]: documentation for copy_meta_to_file
        '''
        # pylint: disable=protected-access
        img = Image(file_path=file_path)
        img._tags = self.tags
        img._meta = self._meta
        img.created = self.created
        # img.accessed = self.accessed_datetime
        img.save(True)
        img.modified = self.modified_datetime
        return img

    def convert_to_jpg(self)->_config._image_type:
        if self.extension in [".jpg"]:
            return
        jpg_path = f"{self.dir_path}/{self.name_no_ext}.jpg"
        paths = _f.convert.to_jpg(self.file_path,jpg_path)
        if len(paths) > 0:
            return self.copy_meta_to_file(paths[0])

    def convert_to_png(self,delete_original=False)->_config._image_type:
        '''
            Convert this image to a PNG


            Arguments
            -------------------------
            `delete_original`=False {bool}
                Delete this image after creating the converted copy.

            Return {Image}
            ----------------------
            A new image instance for the png file if successful, False otherwise

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 08-03-2023 05:30:42
            `memberOf`: Image
            `version`: 1.0
            `method_name`: convert_to_png
            * @xxx [08-03-2023 05:32:15]: documentation for convert_to_png
        '''
        new_path = f"{self.dir_path}/{self.name_no_ext}.png"
        self.img.save(new_path)
        if _f.exists(new_path):
            png_image = self.copy_meta_to_file(new_path)
            if delete_original is True:
                self.delete()
            return png_image
        return False

    def rename(self,new_name:str):
        new_name = new_name.replace(self.extension,'')
        new_path = f"{self.dir_path}/{new_name}{self.extension}"
        # print(f"new_path:{new_path}")
        if _f.rename(self.file_path,new_path):
            self.file_path = new_path
            self.name_no_ext = _f.get_name_no_ext(self.file_path)
            self.name = f"{self.name_no_ext}{self.extension}"
        else:
            print(f"file_path:{self.file_path}")
            print(f"new_path:{new_path}")
            raise OSError("Failed to rename file")

    @property
    def tags(self)->Iterable[str]:
        '''
            Get this Image's tags

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-21-2023 11:40:46
            `@memberOf`: Image
            `@property`: tags
        '''
        value = self._tags
        return value




    # ---------------------------------------------------------------------------- #
    #                          META TAG GETTERS & SETTERS                          #
    # ---------------------------------------------------------------------------- #

    def _handle_comma_delimited_value(self,value):
        '''
        Attempts to split the value by commas
        '''

        if isinstance(value,(str)) is False:
            return value
        a = value.split(",")
        if len(a) == 1:
            return a[0]
        return a


    @property
    def comment(self):
        '''
        Get or Set the comment meta property

        A user description of this image.
        '''
        return self._get_meta_key("comment")

    @comment.setter
    def comment(self,value):
        self._set_meta_key("comment",value)

    @property
    def copyright(self):
        '''
            Enter a Notice on the current owner of the Copyright for this image, such as ©2008 Jane Doe

            @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#copyright-notice
        '''
        return self._get_meta_key("copyright")

    @copyright.setter
    def copyright(self,value):
        self._set_meta_key("copyright",value)

    @property
    def authors(self):
        '''
        Get or Set the authors meta property

        The name of the person that created this image
        Separate multiple values with commas.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#creator
        '''
        a = self._get_meta_key("authors")
        return self._handle_comma_delimited_value(a)

    @authors.setter
    def authors(self,value:Union[str,Iterable[str]]):
        '''The name of the person that created this image'''
        self._set_meta_key("authors",value)

    @property
    def description(self):
        '''
        Get or Set the description meta property

        Enter a "caption" describing the who, what, and why of what is happening in this image, this might include names of people, and/or their role in the action that is taking place within the image

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#description
        '''
        return self._get_meta_key("description")

    @description.setter
    def description(self,value):
        self._set_meta_key("description",value)

    @property
    def instructions(self):
        '''
        Get or Set the instructions meta property

        Enter information about embargoes, or other restrictions not covered by the Rights Usage field

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#instructions
        '''
        return self._get_meta_key("instructions")

    @instructions.setter
    def instructions(self,value):
        self._set_meta_key("instructions",value)

    @property
    def title(self):
        '''
        Get or Set the title meta property

        A shorthand reference for the digital image. Title provides a short human readable name which can be a text and/or numeric reference. It is not the same as Headline.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#title
        '''
        return self._get_meta_key("title")

    @title.setter
    def title(self,value):
        self._set_meta_key("title",value)

    @property
    def subject(self):
        '''
        Get or Set the subject meta property

        EXIF:subject

        Info about the subject of the image

        '''
        return self._get_meta_key("subject")

    @subject.setter
    def subject(self,value):
        self._set_meta_key("subject",value)

    @property
    def headline(self):
        '''
        Get or Set the headline meta property

        A brief synopsis of the caption. Headline is not the same as Title.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#headline
        '''
        return self._get_meta_key("headline")

    @headline.setter
    def headline(self,value):
        self._set_meta_key("headline",value)

    @property
    def source(self):
        '''
        Get or Set the source meta property

        XMP:source

        Info about the source
        '''
        return self._get_meta_key("source")

    @source.setter
    def source(self,value):
        self._set_meta_key("source",value)

    @property
    def credits(self):
        '''
        Get or Set the credits meta property

        ["XMP:Credit","IPTC:Credit"]

        Info about the credits for this image
        '''
        return self._get_meta_key("credits")

    @credits.setter
    def credits(self,value):
        self._set_meta_key("credits",value)

    @property
    def job_identifier(self):
        '''
        Get or Set the job_identifier meta property

        Number or identifier for the purpose of improved workflow handling. This is a user created identifier related to the job for which the image is supplied.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#job-id
        '''
        return self._get_meta_key("job_identifier")

    @job_identifier.setter
    def job_identifier(self,value):
        self._set_meta_key("job_identifier",value)

    @property
    def legal_url(self):
        '''
        Get or Set the legal_url meta property

        URL referencing a web resource providing a statement of the copyright ownership and usage rights of the image.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#web-statement-of-rights
        '''
        return self._get_meta_key("legal_url")

    @legal_url.setter
    def legal_url(self,value):
        self._set_meta_key("legal_url",value)

    @property
    def usage_terms(self):
        '''
        Get or Set the usage_terms meta property

        The licensing parameters of the image expressed in free-text.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#rights-usage-terms
        '''
        return self._get_meta_key("usage_terms")

    @usage_terms.setter
    def usage_terms(self,value):
        self._set_meta_key("usage_terms",value)

    @property
    def job_title(self):
        '''
        Get or Set the job_title meta property

        Contains the job title of the photographer. As this is sort of a qualifier the Creator element has to be filled in as mandatory prerequisite for using Creator’s Jobtitle.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#creators-jobtitle
        '''
        return self._get_meta_key("job_title")

    @job_title.setter
    def job_title(self,value):
        self._set_meta_key("job_title",value)

    @property
    def address(self):
        '''
        Get or Set the address meta property

        Enter Address for the person that created this image

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#contact-information-structure
        '''
        return self._get_meta_key("address")

    @address.setter
    def address(self,value):
        self._set_meta_key("address",value)

    @property
    def city(self):
        '''
        Get or Set the city meta property

        Enter City for the person that created this image

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#contact-information-structure
        '''
        return self._get_meta_key("city")

    @city.setter
    def city(self,value):
        self._set_meta_key("city",value)

    @property
    def region(self):
        '''
        Get or Set the region meta property

        The contact information part denoting regional information such as state or province.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#contact-information-structure
        '''
        return self._get_meta_key("region")

    @region.setter
    def region(self,value):
        self._set_meta_key("region",value)

    @property
    def postal_code(self):
        '''
        Get or Set the postal_code meta property

        The contact information part denoting the postal_code.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#contact-information-structure
        '''
        return self._get_meta_key("postal_code")

    @postal_code.setter
    def postal_code(self,value):
        self._set_meta_key("postal_code",value)

    @property
    def country(self):
        '''
        Get or Set the country meta property

        The contact information part denoting the country.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#contact-information-structure
        '''
        return self._get_meta_key("country")

    @country.setter
    def country(self,value):
        self._set_meta_key("country",value)

    @property
    def phone(self):
        '''
        Get or Set the phone meta property

        The contact information part denoting the creators phone number.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#contact-information-structure
        '''
        return self._get_meta_key("phone")

    @phone.setter
    def phone(self,value):
        self._set_meta_key("phone",value)

    @property
    def email(self):
        '''
        Get or Set the email meta property

        The contact information part denoting the creators email.
        separate multiple emails with commas.

        @see https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata#contact-information-structure
        '''
        a = self._get_meta_key("email")
        return self._handle_comma_delimited_value(a)

    @email.setter
    def email(self,value:Union[str,Iterable[str]]):
        self._set_meta_key("email",value)

    @property
    def creator_url(self):
        '''
        Get or Set the creator_url meta property

        The contact information part denoting the creators creator_url.

        XMP:CreatorWorkURL
        '''
        return self._get_meta_key("creator_url")

    @creator_url.setter
    def creator_url(self,value):
        self._set_meta_key("creator_url",value)



    @property
    def contact_info(self):
        value = {
            "authors":self.authors,
            "job_title":self.job_title,
            "address":self.address,
            "city":self.city,
            "country":self.country,
            "region":self.region,
            "postal_code":self.postal_code,
            "phone":self.phone,
            "email":self.email,
            "creator_url":self.creator_url,
        }
        return value

    @contact_info.setter
    def contact_info(self,value:dict):
        for k,v in value.items():
            if hasattr(self,k):
                setattr(self,k,v)
        # self._contact_info = value




    def _meta_key_props(self)->Iterable[str]:
        '''
            This will retrieve all of the meta tags from the MetaKeys class and retrieve the associated
            values from this instance.

            This is used for saving all tags with their corresponding values.

            Return {dict}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 08-03-2023 08:33:58
            `memberOf`: Image
            `version`: 1.0
            `method_name`: _meta_key_props
            * @TODO []: documentation for _meta_key_props
        '''

        props = dir(MetaKeys)
        out = {}
        for p in props:
            if p.startswith("_"):
                continue
            if p not in out:
                tags = getattr(MetaKeys,p)
                val = getattr(self,p)
                for t in tags:
                    if val is not None:
                        out[t] = val

                # out.append(p)
        return out

    def _get_meta_tags(self,name)->list:
        '''
            Method used internally to retrieve a list of meta tag names from the MetaKeys setting class.

            Arguments
            -------------------------
            `name` {str}
                The name of the tag list to retrieve

            Return {list}
            ----------------------
            A list of meta tag names or an empty list if the name is not found.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 08-03-2023 07:22:01
            `memberOf`: Image
            `version`: 1.0
            `method_name`: _get_meta_tags
            * @xxx [08-03-2023 07:23:13]: documentation for _get_meta_tags
        '''
        if hasattr(MetaKeys,name):
            return getattr(MetaKeys,name)
        return []

    def _get_meta_key(self,key:str,meta_tags:Union[str,Iterable[str]]=None)->Union[str,None]:
        '''
            Method used to internally retrieve a meta tag value.

            If the value is not already set on this instance it will attempt to retrieve it from the meta data

            Arguments
            -------------------------
            `key` {str}
                The name of the attribute to retrieve the value for.

            `meta_tags`=None {str,list[str]}
                The meta tag or list of meta tags to assign the new value to.

                If not provided it will use the key to search the MetaKeys for the tag names.

                You should pretty much never need to provide this.

            Return {str,None}
            ----------------------
            The value of the attribute if it exists, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 08-03-2023 07:23:20
            `memberOf`: Image
            `version`: 1.0
            `method_name`: _get_meta_key
            * @xxx [08-03-2023 07:25:19]: documentation for _get_meta_key
        '''
        if hasattr(self,f"_{key}"):
            value = getattr(self,f"_{key}")

            if value is None:
                value = _obj.get_arg(self._meta,self._get_meta_tags(key),None,str)
                setattr(self,f"_{key}",value)
            return value
        return None

    def _set_meta_key(self,key:str,value,meta_tags:Union[str,Iterable[str]]=None):
        '''
            Used Internally to set EXIF,IPTC and XMP tags on this image.

            Arguments
            -------------------------
            `key` {str}
                The name of this Image property to update.

            `value` {any}
                The value to assign to the key

                If a dict is provided, it will attempt to convert it to JSON first.

                If a list or tuple is provided, it will concatenate them with a comma delimiter.

            `meta_tags` {str,list[str]}
                The meta tag or list of meta tags to assign the new value to.

                If not provided it will use the key to search the MetaKeys for the tag names.

                You should pretty much never need to provide this.


            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 08-03-2023 07:04:35
            `memberOf`: Image
            `version`: 1.0
            `method_name`: _set_meta_key
            * @xxx [08-03-2023 07:28:39]: documentation for _set_meta_key
        '''
        if meta_tags is None:
            meta_tags = self._get_meta_tags(key)
        meta_tags = _arr.force_list(meta_tags)

        if value is None:
            value = ''

        if isinstance(value,(int,float)):
            value = str(value)

        if isinstance(value,(dict)):
            value = json.dumps(value)

        if isinstance(value,(tuple,list)):
            value = ','.join(value)

        if isinstance(value,(str)) is True:
            if hasattr(self,f"_{key}"):
                setattr(self,f"_{key}",value)

            for meta_tag in meta_tags:
                oval = _obj.get_arg(self._meta,[meta_tag],None,str)
                if oval is None:
                    self.changes_made = True
                elif self._meta[meta_tag] != value:
                    # if self._meta[meta_tag] != value:
                    self.changes_made = True
                self._meta[meta_tag] = value
            return getattr(self,f"_{key}")
        return False

    @property
    def stable_diffusion_params(self)->dict:
        '''
            Get this Image's stable_diffusion_params

            If this file was generated by stable diffusion, this will parse
            the comment into its options.

            If it was not, it will return None.

            `default`:None


            `example`:
                data = {
                    "prompts":[],
                    "negative_prompt":[],
                    "steps":None,
                    "sampler":None,
                    "cfg_scale":None,
                    "seed":None,
                    "face_restoration":None,
                    "size":None,
                    "model_hash":None,
                    "model":None,
                }

            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-21-2023 08:21:07
            `@memberOf`: Image
            `@property`: stable_diffusion_params
        '''
        value = self._stable_diffusion_data
        if value is None:
            value = _parse_stable_diffusion_comment(self)
            self._stable_diffusion_data = value
        return value

    @property
    def is_stable_diffusion_render(self)->bool:
        '''
            Get this Image's is_stable_diffusion_render

            returns True if this file has stable diffusion data in its comment.

            `default`:False


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-21-2023 08:53:46
            `@memberOf`: Image
            `@property`: is_stable_diffusion_render
        '''
        options = ["Steps","Sampler","CFG scale","Seed","Face restoration","Size","Model hash","Model"]
        options_found = False
        for op in options:
            if op in self.comment:
                options_found = True
        return options_found














    # ---------------------------------------------------------------------------- #
    #                          IMAGE MANIPULATION METHODS                          #
    # ---------------------------------------------------------------------------- #

    # def scale(self,width=None,height=None):
    #     img = self.img
    #     wpercent = (basewidth/float(img.size[0]))
    #     hsize = int((float(img.size[1])*float(wpercent)))
    #     pil_image.resam
    #     img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
    #     img.save(self.path)

    def scale_fit(self,width,height,create_copy=False):
        # if width >= height and self.orientation in ["landscape","square"]:
        #     print(f"fitting image width to {width}")
        #     self.fit_width(width)
        if self.orientation == "portrait":
            if self.height != height:
                # print(f"fitting image height to {height}")
                self.fit_height(height,create_copy)
        if self.orientation in ["landscape","square"]:
            if self.width != width:
                # print(f"fitting image width to {width}")
                self.fit_width(width)

    def fit_height(self,base_height=2160,create_copy=False):
        img = self.img
        if img.height == base_height:
            img.close()
            return


        wpercent = (base_height/float(img.size[1]))
        wsize = int((float(img.size[0])*float(wpercent)))
        img = img.resize((wsize,base_height), pil_img_mod.Resampling.LANCZOS)
        if create_copy is True:
            if base_height < self.height:
                tmp_path = f"{self.dir_path}/{self.name_no_ext}_SMALL{self.ext}"
                img.save(tmp_path)
                img.close()
                self.copy_meta_to_file(tmp_path)
                self.rename(f"{self.name_no_ext}_LARGE")
                return

        tmp_path = f"{self.dir_path}/tmp_{_csu.rand()}{self.ext}"
        img.save(tmp_path)
        img.close()
        self.copy_meta_to_file(tmp_path)
        _f.delete(self.path)
        _f.rename(tmp_path,self.path)
        self.reset_pillow_props()

    def fit_width(self,base_width=3840):
        img = self.img
        if img.width == base_width:
            img.close()
            return
        wpercent = (base_width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        # orig = img.copy()
        img = img.resize((base_width,hsize), pil_img_mod.Resampling.LANCZOS)
        # orig.paste(img)
        # orig.save(self.path)
        # orig.close()
        tmp_path = f"{self.dir_path}/tmp_{_csu.rand()}{self.ext}"
        img.save(tmp_path)
        img.close()
        self.copy_meta_to_file(tmp_path)
        _f.delete(self.path)
        _f.rename(tmp_path,self.path)
        self.reset_pillow_props()

    def reset_pillow_props(self):
        self._height = None
        self._width = None
        self._orientation = None
        self._content_hash = None
        self._area = None


    def __repr__(self):
        return f"<Image : {self.name_no_ext} {self.width}x{self.height}>"




def _parse_stable_diffusion_comment(img:Image):
    options = ["Steps","Sampler","CFG scale","Seed","Face restoration","Size","Model hash","Model"]
    options_found = False

    data = {
        "prompts":[],
        "negative_prompt":[],
        "steps":None,
        "sampler":None,
        "cfg_scale":None,
        "seed":None,
        "face_restoration":None,
        "size":None,
        "model_hash":None,
        "model":None,
    }

    cmt = img.comment
    for op in options:
        if op in cmt:
            options_found = True
    if options_found is False:
        return None

    cmt = cmt.replace("Negative prompt","negative_prompt")
    for op in options:
        op_snake = _csu.to_snake_case(op)
        cmt = cmt.replace(op,op_snake)
        reg = rf'(\s?{op_snake}:\s?([^\n,]*),?\s?)'
        match = re.findall(reg,cmt)
        if len(match)>0:
            match = match[0]
            # print(f"match:{match}")
            data[op_snake] = match[1]
            cmt = cmt.replace(match[0],'')

    # @Mstep [] capture the negative prompt list.
    match = re.findall(r'(\s?negative_prompt:\s?(.*))',cmt)
    if len(match)>0:
        match = match[0]
        data['negative_prompt'] = match[1].split(",")
        cmt = cmt.replace(match[0],'')
    # @Mstep [] anything that remains are positive prompts
    data['prompts'] = cmt.replace("\n","").split(",")

    return data

def apply_synonyms(images):
    # c.con.log("Applying Tag Synonyms","info invert")
    synonyms = _f.read.as_json(f"{os.getcwd()}/alice/image_organizer/synonyms.json")
    img:Image
    for img in images:
        for syn in synonyms:
            if len(syn) == 2:
                if img.has_tag(syn[0],regex=True):
                    # c.con.log(f"    Synonym Found: {syn[0]}    ","magenta invert")
                    img.tag_commands(syn[1])
        if img.is_stable_diffusion_render:
            img.add_tag("stable_diffusion")

def _get_meta(files):
    '''
        Iterate the file dictionaries provided and add the image meta data.
        ----------

        Arguments
        -------------------------
        `files` {list}
            The list of file dictionaries from colemen_utils.get_files/ get_data


        Return {list}
        ----------------------
        A list of file dictionaries with the meta data added.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-21-2023 09:52:13
        `memberOf`: Image
        `version`: 1.0
        `method_name`: _get_meta
        * @xxx [02-21-2023 09:54:00]: documentation for _get_meta
    '''
    # c.con.log(f"Retrieving meta data for {len(files)} images","info")
    result_array = []
    paths = [_csu.file_path(x['file_path'],url=True) for x in files]
    import exiftool
    with exiftool.ExifToolHelper() as et:
        try:
            result_array = et.get_metadata(paths)
        except UnicodeDecodeError as e:
            # c.con.log("Failed to retrieve meta data","red invert")
            print(e)

    return result_array

# def get_images(path)->Iterable[Image]:
#     files = _f.get_files(path,extensions=['.jpg','.jpeg','.png','.jfif','.gif','.webp'])
#     synonyms = _f.read.as_json(f"{os.getcwd()}/alice/image_organizer/synonyms.json") or []
#     if len(files) == 0:
#         return []
#     files = _get_meta(files)
#     output = []
#     for file in files:
#         # print(f"file:{file}")
#         image = Image(file)
#         image.synonyms = synonyms
#         output.append(image)
#     return output




# if __name__ == "__main__":
#     imgs = get_images("C:/Users/Colemen/Desktop/TEST_FOLDER/PurgeAllButNewest")
#     for img in imgs:
#         print(f"img.tags:{img.tags}")
        # if img.is_stable_diffusion_render:
        #     for k,v in img.stable_diffusion_params.items():
        #         if k not in ["prompts","negative_prompt"]:
        #             img.add_tag(f"{k}:{v}")
        #         else:
        #             img.add_tag(v)
        # img.apply_synonyms()
        # img.save()











