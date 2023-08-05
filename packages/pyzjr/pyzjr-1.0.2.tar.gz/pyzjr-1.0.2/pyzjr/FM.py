from tqdm import tqdm
import requests
import cv2
import os, shutil
from matplotlib import pyplot as plt
from PIL import Image
import imghdr


def download_file(url):
    """
    :param url:下载文件所在url链接
    :return: 下载的位置处于根目录
    """
    print("------", "Start download with urllib")
    name = url.split("/")[-1]
    resp = requests.get(url, stream=True)
    content_size = int(resp.headers['Content-Length']) / 1024  # 确定整个安装包的大小
    # 下载到上一级目录
    path = os.path.abspath(os.path.dirname(os.getcwd())) + "\\" + name
    # 下载到该目录
    path = os.getcwd() + "\\" + name
    print("File path:  ", path)
    with open(path, "wb") as file:
        print("File total size is:  ", content_size)
        for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k', desc=name):
            file.write(data)
    print("------", "finish download with urllib\n\n")

def getPhotopath(paths):
    """
    * log
        0.0.19以后修改了一个比较大的bug
        1.0.2后将图片和所有文件路径分开
    :param paths: 文件夹路径
    :return: 包含图片路径的列表
    """
    img_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'tiff', 'webp', 'raw']
    imgfile = []
    allfile = []
    file_list = os.listdir(paths)
    for i in file_list:
        if i[0] in ['n', 't', 'r', 'b', 'f'] or i[0].isdigit():
            print(f"Error: 文件名 {i} 开头出现错误！")
        newph = os.path.join(paths, i).replace("\\", "/")
        allfile.append(newph)
        _, file_ext = os.path.splitext(newph)
        if file_ext[1:] in img_formats:
            imgfile.append(newph)

    return imgfile,allfile


def Pic_rename(img_folder,object='Crack',format='jpg',num=0):
    """
    * 用于批量修改图像的命名
    :param img_folder:存放图片的路径
    :param object: 图像的对象
    :param format: 图片格式,可自行命名,这里给出jpg
    :param num: 对图片进行计数
    :return: 用dst替换src
    """
    for img_name in os.listdir(img_folder):
        src = os.path.join(img_folder, img_name)
        dst = os.path.join(img_folder, object+ str(num) +'.'+ format)
        num= num+1
        os.rename(src, dst)

def CreateFolder(folder_path):
    """确保文件夹存在"""
    if not os.path.exists(folder_path):
        try:
            os.mkdir(folder_path)
            print(f"文件夹 {folder_path} 创建成功!")
        except OSError:
            print(f"创建文件夹 {folder_path} 失败!")
    else:
        print(f"文件夹 {folder_path} 已存在!")
    return folder_path

def loadImages(folder_path):
    """加载一个文件夹下的图片，并存入列表中并返回"""
    images = []
    imgfile, _ = getPhotopath(folder_path)
    for img_path in imgfile:
        img = cv2.imread(img_path)
        images.append(img)
    return images


def ImageAttribute(image):
    """获取图片属性"""
    properties = {}
    if isinstance(image, str):  # 如果传入的是文件路径
        properties['name'] = os.path.basename(image)
        properties['format'] = imghdr.what(image)
        properties['fsize'] = os.path.getsize(image)
        image = cv2.imread(image)
    else:  # 如果传入的是图片数据
        properties['name'] = "Nan"
        properties['format'] = "Nan"
        properties['fsize'] = image.nbytes
    properties["shape"] = image.shape
    properties["dtype"] = image.dtype
    properties['size'] = image.size
    return properties
