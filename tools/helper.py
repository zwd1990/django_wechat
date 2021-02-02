import os
import sys
import locale
from datetime import datetime

from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import redirect


FILE_PATH = 'F:\\git\\fileSave'
BDB_URL = '192.168.0.212:9984'
template_file_path = 'F:/git/fileSave/example.txt'


# 保存算法文件
def save_file(entity, key, request_field, path=FILE_PATH):
    code = 0
    message = '上传成功'
    path_root = FILE_PATH  # 上传文件的主
    path_dst_file = '' # 文件存储路径
    # print(request_field)
    print('good')
    if request_field is None:
        code = -1
        message = 'upload fail'
        print(message)
    else:
        file_prex = ''.join(datetime.now().strftime("%Y-%m-%d-%H-%M-%S").split('-'))
        request_field.name = file_prex + '-' + request_field.name
        path_dst_file = os.path.join(path_root, request_field.name)
        print(request_field.name)
        if os.path.isfile(path_dst_file):
            code = -1
            message = '%s 已存在' % (request_field.name)
            print(message)
        else:
            print('文件路径为：',path_dst_file)
            destination = open(path_dst_file, 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in request_field.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
    entity.response['code'] = code
    entity.response['message'] = message
    entity.data[key] = path_dst_file
    return entity


# 下载文件
def download_file(filePath = template_file_path):
    fileName = filePath.split('/')[-1]
    response = StreamingHttpResponse(readFile(filePath))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fileName)
    return response


def readFile(filename, chunk_size=512):
    try:
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    except:
        print('无法打开该文件')


def process_request(request, entity, file_field=None):
    # POST request
    # print(entity.InPut)
    code = 0
    message = '成功'
    data = {}

    for key, field in entity.InPut.items():
        body = request.POST.get(key)
        if key == file_field:
            body = request.FILES.get(key)
            print('读取文件', body)

        if body is None:
            message = field + '缺失'
            code = -1
        data[key] = body
    # print(data)
    entity.data = data
    entity.response['code'] = code
    entity.response['message'] = message
    return entity


def db_save(db, entity):
    code = 0
    message = '保存数据库成功'
    id = -1
    DBData = {}

    for key, field in entity.DBOutPut.items():
        body = entity.data[key]
        if body is None:
            print('缺失键==',key)
            message = field + '数据缺失'
            code = -1
        DBData[key] = body
    if code == 0:
        try:
            print('DBData: {0}'.format(DBData))
            object = db.objects.create(**DBData)
            id = object.id
        except:
            code = -1
            message = '保存失败'
            print('保存数据到数据库失败')
    entity.response['id'] = id # 每次保存完，把id传过去
    entity.response['code'] = code
    entity.response['message'] = message
    return entity