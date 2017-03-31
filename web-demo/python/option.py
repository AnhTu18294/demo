import os, sys
import json
import numpy as np

def get_collections_dir_name():
    path_to_app = os.path.abspath(os.path.dirname(__file__))
    temp = path_to_app.split('/')
    return '/'.join(temp[0:len(temp)-2]) + '/collections/'

collections_dir_name = get_collections_dir_name()
ALL_IMAGES = 'all/images'


def get_collection():
    res = []
    global collections_dir_name
    for name in os.listdir(collections_dir_name):
        if os.path.isdir(collections_dir_name + name):
            res.append(name)
    print json.dumps(res)

def get_list(collection):
    res = []
    files_folder_name = collections_dir_name + collection + '/list'
    res.append({"id": ALL_IMAGES, "text": "all images"})
    if(not os.path.isdir(files_folder_name)):
        print json.dumps([])

    for name in os.listdir(files_folder_name):
        if(os.path.isfile(files_folder_name + '/' + name)):
            res.append({"id": name, "text": name})
    print json.dumps(res)

def get_dataset(collection):
    res = []
    datasetfolder = collections_dir_name + collection + '/data'
    if(not os.path.isdir(datasetfolder)):
        print json.dumps([])

    for name in os.listdir(datasetfolder):
        if(os.path.isdir(datasetfolder + '/' + name)):
            res.append({"id": name, "text": name})
    print json.dumps(res)

def get_category(collection, dataset):
    res = []
    categories_file = collections_dir_name + collection + '/data/' + dataset + '/categories.txt'

    try:
        fin = open(categories_file, 'r')
    except:
        return json.dumps([])
    line = fin.readline()
    while line:
        temp = line.split(' ')
        res.append({"id": temp[0], "text": temp[1]})
        line = fin.readline()

    print json.dumps(res)

def get_binaryfile(collection, dataset):
    res = []
    binaryfile_folder = collections_dir_name + collection + '/data/' + dataset
    if(not os.path.isdir(binaryfile_folder)):
        print json.dumps([])

    for filename in os.listdir(binaryfile_folder):
        if(os.path.isfile(binaryfile_folder + '/' + filename) and filename.endswith('.bin')):
            res.append({"id": filename, "text": filename})
    print json.dumps(res)

def main(argv):
    if(argv[1] == '0'):
        get_collection()
    elif(argv[1] == '1'):
        get_list(argv[2])
    elif(argv[1] == '2'):
        get_dataset(argv[2])
    elif(argv[1] == '3'):
        params = argv[2].split(',')
        get_category(params[0], params[1])
    elif(argv[1] == '4'):
        params = argv[2].split(',')
        get_binaryfile(params[0], params[1])

if __name__ == "__main__":       
    main(sys.argv)
