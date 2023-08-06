import os
import shutil
import urllib
import uuid
from base64 import b64decode
from io import BytesIO
from pathlib import Path
from time import time
from zipfile import ZipFile, ZipInfo

import cv2
import numpy as np
from fastapi import HTTPException
from PIL import Image
from PIL import ImageFile
from six import moves
from tqdm import tqdm
import logging
from .bases import DataLoader
import subprocess as sp
import json


logging.basicConfig(
    format="============ %(asctime)s [%(pathname)s:%(lineno)d] ============ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
# import zipfile
def _extract_member(self, member, targetpath,
                    pwd):  # To fix the Windows zip problem
    """Extract the ZipInfo object 'member' to a physical
       file on the path targetpath.
    """
    if not isinstance(member, ZipInfo):
        member = self.getinfo(member)

    if os.path.sep == '/':
        arcname = member.filename.replace('\\', os.path.sep)
    else:
        arcname = member.filename.replace('/', os.path.sep)

    if os.path.altsep:
        arcname = arcname.replace(os.path.altsep, os.path.sep)
    # interpret absolute pathname as relative, remove drive letter or
    # UNC path, redundant separators, "." and ".." components.
    arcname = os.path.splitdrive(arcname)[1]
    invalid_path_parts = ('', os.path.curdir, os.path.pardir)
    arcname = os.path.sep.join(x for x in arcname.split(os.path.sep)
                               if x not in invalid_path_parts)
    if os.path.sep == '\\':
        # filter illegal characters on Windows
        arcname = self._sanitize_windows_name(arcname, os.path.sep)

    targetpath = os.path.join(targetpath, arcname)
    targetpath = os.path.normpath(targetpath)

    # Create all upper directories if necessary.
    upperdirs = os.path.dirname(targetpath)
    if upperdirs and not os.path.exists(upperdirs):
        os.makedirs(upperdirs)

    if member.is_dir():
        if not os.path.isdir(targetpath):
            os.mkdir(targetpath)
        return targetpath

    with self.open(member, pwd=pwd) as source, \
            open(targetpath, "wb") as target:
        shutil.copyfileobj(source, target)

    return targetpath


ZipFile._extract_member = _extract_member

IMG_FORMATS = [
    'bmp',
    'jpg',
    'JPG',
    'jpeg',
    'JPEG',
    'png',
    'tif',
    'tiff',
    'dng',
    'webp',
    'mpo',
]  # acceptable image suffixes
VID_FORMATS = [
    'mov',
    'avi',
    'mp4',
    'mpg',
    'mpeg',
    'm4v',
    'wmv',
    'mkv',
]  # acceptable video suffixes

ImageFile.LOAD_TRUNCATED_IMAGES = True


def load_data(data: list, type: str, mode='BGR', video_sample_rate=1):
    if type == 'b64' or type == 'base64':
        return B64ImageLoader(data, mode)

    elif type == 'stream':
        return UrlStreamLoader(data, mode, video_sample_rate)

    elif type == 'url':
        data_format = data[0].split('.')[-1].lower()
        if data_format in IMG_FORMATS:
            return UrlImageLoader(data, mode)

        elif data_format in VID_FORMATS:
            return UrlVideoLoader(data, mode, video_sample_rate)

        else:
            print('ERROR ---> Unsupported data format {}.'.format(data_format))
            raise HTTPException(
                status_code=500,
                detail='Unsupported data format {}.'.format(data_format),
            )

    elif type == 'local':
        data_format = data[0].split('.')[-1].lower()
        if data_format in IMG_FORMATS:
            return LocalImageLoader(data, mode)

        elif data_format in VID_FORMATS:
            return LocalVideoLoader(data, mode, video_sample_rate)

        else:
            raise HTTPException(
                status_code=600,
                detail='Unsupported data format {}.'.format(data_format),
            )

    elif type == 'zip':
        return ZipImageLoader(data, mode)

    else:
        print('ERROR ---> Unsupported data type {}.'.format(type))
        raise HTTPException(
            status_code=500, detail='Unsupported data type {}.'.format(type)
        )


# def image_resize(img: Image, resize_param: int = EnvVar.RESIZE_PARAM):
#     """
#     Resize image so that the short side match the resize_param
#     :img: PIL image
#     :resize_param: Expected image short side
#     """
#     short_side = min(img.size[0], img.size[1])
#
#     scale = resize_param / short_side
#
#     return img.resize(
#         (int(img.size[0] * scale), int(img.size[1] * scale)), Image.BICUBIC
#     )


class Downloader:
    def __init__(self) -> None:
        dest_folder = os.path.join(os.getcwd(), 'data', str(uuid.uuid1()))
        if os.path.exists(dest_folder):
            raise RuntimeError('Data folder already exists!')
        os.makedirs(dest_folder)
        self.dest_folder = dest_folder

    def download(self, urls: list):
        print('--- Start downloading data ---')
        data_paths = []
        for i, url in tqdm(enumerate(urls)):
            name = url.split('/')[-1]
            name = moves.urllib.parse.unquote(name)
            data_path = os.path.join(self.dest_folder, name)
            try:
                moves.urllib.request.urlretrieve(url, data_path)
            except Exception as error:
                print('!!! Download failed for the file {}'.format(url))
                print('ERROR >>> {}'.format(str(error)))
                data_paths.append(None)
                continue
            data_paths.append(data_path)

        print('--- Finish download data {}/{} ---'.format(len(data_paths),
                                                          len(urls)))
        if not data_paths:
            raise HTTPException(status_code=501, detail='No data collected')

        return data_paths, self.dest_folder


class B64ImageLoader(DataLoader):
    def __init__(self, images: list, mode: str) -> None:
        super().__init__(images, mode)

        self.type = 'base64'

    def __next__(self):
        if self.count == self.img_size:
            raise StopIteration

        img = self.images[self.count]
        self.count += 1
        img, img_size = self._load_image_b64(img, self.mode)
        return img, None, img_size

    def _load_image_b64(self, data, mode):
        img_b = b64decode(data)
        im = Image.open(BytesIO(img_b)).convert('RGB')

        # im = image_resize(im)
        img_size = im.size
        res = np.array(im)
        if self.mode == 'BGR':
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)

        return res, img_size


class UrlImageLoader(DataLoader):
    def __init__(self, images: list, mode: str) -> None:
        super().__init__(images, mode)

        self.type = 'image'
        self.shape = (720, 1280, 3)

    def __next__(self):
        if self.count == self.img_size:
            raise StopIteration

        url = self.images[self.count]
        self.count += 1
        try:
            s_time = time()
            # im = Image.open(io.BytesIO(requests.get(url).content))
            im = Image.open(urllib.request.urlopen(url)).convert('RGB')
            print('###### Get image from [{}] use: {}'.format(url,
                                                              time() - s_time))
        except Exception as e:
            print('!!!!!!! pass an illegal frame !!!!!!! -> {}'.format(url))
            im = Image.fromarray(np.zeros(self.shape).astype(np.uint8))

        # print('Old image size = ', im.size)
        # im = image_resize(im)
        # print('New image size = ', im.size)
        img_size = im.size
        res = np.array(im)
        if self.mode == 'BGR':
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
        self.shape = res.shape
        return res, None, img_size


class LocalImageLoader(DataLoader):
    def __init__(self, images: list, mode: str) -> None:
        super().__init__(images, mode)

        self.type = 'image'

    def __next__(self):
        if self.count == self.img_size:
            raise StopIteration

        path = self.images[self.count]
        self.count += 1

        im = Image.open(path)

        if self.mode:
            im = im.convert(self.mode)

        # im = image_resize(im)
        # print('New image size = ', im.size)
        img_size = im.size
        res = np.array(im)
        if self.mode == 'BGR':
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)

        return res, None, img_size


class ZipImageLoader(DataLoader):
    def __init__(self, zip_files: list, mode: str) -> None:
        s_time = time()
        downloader = Downloader()
        data_paths, self.dest_path = downloader.download(zip_files)
        print('###### Get image from [{}] use: {}'.format(zip_files,
                                                          time() - s_time))

        for path in data_paths:
            self.unzip(path, self.dest_path)
        data_path = Path(self.dest_path).rglob("*")
        self.images = [str(path) for path in data_path if
                       str(path).split('.')[-1] in IMG_FORMATS]
        self.img_size = len(self.images)
        self.mode = mode

        self.type = 'zip'

    def __next__(self):
        if self.count == self.img_size:
            raise StopIteration

        path = self.images[self.count]
        self.count += 1
        try:
            im = Image.open(path)
        except Exception as e:
            print('!!!!!!! pass an illegal zip file !!!!!!! -> {}'.format(path))
            im = Image.open('image.jpeg')

        # print('Old image size = ', im.size)
        # im = image_resize(im)
        # print('New image size = ', im.size)
        img_size = im.size
        res = np.array(im)
        if self.mode == 'BGR':
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)

        return res, '-'.join(path.split('_')[-1].split('-')[:-1]), img_size

    def release(self):
        try:
            shutil.rmtree(self.dest_path)
        except Exception as error:
            print(str(error))
            print(
                '!!! Data remove error, useless files left. Please remove manually [{}]'.format(
                    self.dest_path
                )
            )

    def unzip(self, zipfile_path, dest_path):
        try:
            files = ZipFile(zipfile_path, "r")
            name_list = files.namelist()
            files.extractall(dest_path)
            print('Total {} images extracted from zip file {}.'.format(
                len(name_list), zipfile_path))
        except Exception as error:
            shutil.rmtree(dest_path)
            raise RuntimeError(
                'Damaged Zip file {}. [{}]'.format(zipfile_path, error))
        files.close()


class UrlVideoLoader:
    def __init__(self, urls: list, mode: str, sample_rate: int) -> None:
        assert len(urls) == 1, '!!! Only support one video a time'

        self.cap = cv2.VideoCapture(urls[0])
        self.frames_num = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.pass_frame = max(1, self.fps / sample_rate)
        self.timestamp = 0

        self.mode = mode
        self.type = 'video'

    def __len__(self):
        return self.frames_num

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count == self.frames_num:
            raise StopIteration

        frame_counter = 0
        while frame_counter < self.pass_frame:
            if self.count == self.frames_num:
                break

            ret_val, frame = self.cap.read()

            self.count += 1
            ret_timestamp = int(self.timestamp)
            self.timestamp += 1000 / self.fps
            frame_counter += 1

        im = Image.fromarray(frame)

        # im = image_resize(im)
        img_size = im.size
        res = np.array(im)
        if self.mode == 'BGR':
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)

        return res, ret_timestamp, img_size

    def release(self):
        try:
            self.cap.release()

        except Exception as error:
            print(str(error))

class LocalVideoLoader(UrlVideoLoader):
    def __init__(self, path: list, mode: str, sample_rate: int) -> None:
        assert len(path) == 1, '!!! Only support one video a time'

        data_path = path[0]

        self.cap = cv2.VideoCapture(data_path)
        self.frames_num = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.pass_frame = max(1, self.fps * sample_rate)
        self.timestamp = 0

        self.mode = mode
        self.type = 'video'

    def release(self):
        self.images = None
        self.img_size = None
        self.mode = None

class UrlStreamLoader:
    def __init__(self, path: list, mode: str, sample_rate: int):
        assert len(path) == 1, '!!! Only support one stream a time'
        self._stream_url = path[0]
        stream_para = self.get_info_from_stream()
        print(stream_para)
        self.width = stream_para["streams"][0]["width"]
        self.height = stream_para["streams"][0]["height"]
        if self.width == 0 or self.height == 0:
            self.width, self.height = 800, 600
        self.codec_name = stream_para["streams"][0]["codec_name"]
        self.pipe = self.rtsp_client()
        self.mode = mode
        self.count = 0
        self.timestamp = 0
        self.type = 'video'

    def get_info_from_stream(self):
        '''
        Parameters
        ----------
        stream_url

        Returns
        -------
        json_out["streams"]["codec_name"]
        json_out["streams"]["width"]
        json_out["streams"]["height"]
        json_out["streams"]["avg_frame_rate"]
        '''
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            self._stream_url,
        ]
        proc = sp.Popen(cmd, stdout=sp.PIPE, bufsize=10 ** 8)
        stdout = proc.communicate()[0]
        bio = BytesIO(stdout)
        json_out = json.load(bio)
        proc.terminate()
        return json_out

    def rtsp_client(self):
        if self.codec_name == "h264":
            decoder_type = "h264_cuvid"
        elif self.codec_name == "hevc" or self.codec_name == "mpeg4":
            decoder_type = "hevc_cuvid"
        else:
            raise Exception(f"This decoder type is {self.codec_name}, Only H.264 and HEVC are supported!")
        command = [
            'ffmpeg',
            '-rtsp_transport', 'tcp',
            '-c:v', decoder_type,
            '-i', self._stream_url,
            '-vf', 'fps=fps=5',
            '-f', 'rawvideo',  # 输出numpy可读取的rawvideo
            '-s', '%dx%d' % (self.width, self.height),  # 指定宽高
            '-pix_fmt', 'bgr24',  # 输出一般cv2的像素格式
            '-'  # 输出到管道
        ]
        pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
        return pipe

    def __iter__(self):
        return self

    def __next__(self):
        try:
            while True:
                raw_image = self.pipe.stdout.read(self.width * self.height * 3)  # 从管道里读取一帧，字节数为(宽*高*3)有三个通道
                image = np.frombuffer(raw_image, dtype='uint8')  # 把读取到的二进制数据转换成numpy数组
                if len(image) == 0:  # 如果全部读取完了就结束循环
                    break
                image = image.reshape((self.height, self.width, 3))  # 把图像转变成应有形状
                # cv2.imwrite('img/%05d.jpg'%self.count, image)  # 用 cv2保存图像
                self.pipe.stdout.flush()  # 充管道
                self.count += 1
                return image, self.timestamp, (self.width, self.height)
        except Exception as e:
            raise StopIteration

    def release(self):
        try:
            self.cap.release()
        except Exception as error:
            print(str(error))

if __name__ == "__main__":
    pass