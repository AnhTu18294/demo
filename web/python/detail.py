import os, sys
import json
import numpy as np
import struct

def get_collections_dir_name():
    path_to_app = os.path.abspath(os.path.dirname(__file__))
    temp = path_to_app.split('/')
    return '/'.join(temp[0:len(temp)-2]) + '/collections/'

collections_dir_name = get_collections_dir_name()
ALL_IMAGES = 'all/images'

def read_categories(f_categoryfile):
    res = []
    line = f_categoryfile.readline()
    while line:
        res.append(line.split(' ')[1].replace('\n',''))
        line = f_categoryfile.readline()

    return res

def read_prob_value_image(image_position, path_to_categoryfile, path_to_binaryfile):
    res = []
    try:
        f_categoryfile = open(path_to_categoryfile, 'r')
        f_binaryfile = open(path_to_binaryfile, 'r')
    except:
        print json.dumps([])

    categories = read_categories(f_categoryfile)
    float_size = 4
    number_of_category = len(categories)
    offset = number_of_category*image_position*float_size
    f_binaryfile.seek(offset)
    buff_image_probs = f_binaryfile.read(number_of_category*float_size)
    prob_image_list_values = np.frombuffer(buff_image_probs, dtype='<f', count = -1, offset = 0)
    
    prob_image_list_values = np.asarray(prob_image_list_values) 
    argsort = prob_image_list_values.argsort()[::-1]
    for i in range(0, len(argsort)):
        res.append({"name": categories[argsort[i]], "prob": str(prob_image_list_values[argsort[i]])})
    
    print json.dumps(res)


def main(argv):
    params = argv[1].split(',')
    collection = params[0]
    dataset = params[1]
    binaryfile = params[2]
    image_position = int(params[3])
    path_to_categoryfile = collections_dir_name + collection + '/data/' + dataset + '/categories.txt'
    path_to_binaryfile = collections_dir_name + collection + '/data/' + dataset + '/' + binaryfile

    read_prob_value_image(image_position,path_to_categoryfile, path_to_binaryfile)

if __name__ == "__main__":       
    main(sys.argv)
