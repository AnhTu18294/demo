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

# read keylist
def read_keylist(f_keyfile):
    res = {}
    line = f_keyfile.readline().replace('\n', '')
    i = 0
    while line:
        res[line] = i
        i += 1
        line = f_keyfile.readline().replace('\n', '')

    return res

def read_categories(f_categoryfile):
    res = []
    line = f_categoryfile.readline()
    while line:
        res.append(line.split(' ')[1])
        line = f_categoryfile.readline()

    return res

# Sort image 
def sort_image_with_sublist(category, path_to_keyfile, path_to_list_image_file, path_to_bynaryfile, path_to_categoryfile):
    res = []
    
    try:
        f_keyfile = open(path_to_keyfile, 'r')
        f_categoryfile = open(path_to_categoryfile, 'r')
        f_binaryfile = open(path_to_bynaryfile, 'r')
        f_listimage = open(path_to_list_image_file, 'r')
    except:
        return res

    keylist_dict = read_keylist(f_keyfile)
    categories = read_categories(f_categoryfile)

    # get numerical order follow keylist file
    number_of_category = len(categories)
    size_of_float = 4

    prob_image_list_values = []

    image_list_name = []
    image_key = f_listimage.readline().replace('\n', '')
    while image_key:
        try:
            image_position = keylist_dict[image_key]
        except:
        	return res

        offset = (number_of_category*image_position + category)*4
        f_binaryfile.seek(offset)
        temp = f_binaryfile.read(4)
        prob_image_list_values.append(struct.unpack('<f', temp)[0])
        image_list_name.append(image_key)
        image_key = f_listimage.readline().replace('\n', '')
    
    prob_image_list_values = np.asarray(prob_image_list_values) 
    argsort = prob_image_list_values.argsort()[::-1]
    for i in range(0, len(argsort)):
        res.append({"id": str(keylist_dict[image_list_name[argsort[i]]]),"name": image_list_name[argsort[i]], "prob": str(prob_image_list_values[argsort[i]])})
    
    return res

def sort_image_without_sublist(category, path_to_keyfile, path_to_bynaryfile, path_to_categoryfile):
    res = []
    try:
        f_keyfile = open(path_to_keyfile, 'r')
        f_categoryfile = open(path_to_categoryfile, 'r')
        f_binaryfile = open(path_to_bynaryfile, 'r')
    except:
        return res

    categories = read_categories(f_categoryfile)

    number_of_category = len(categories)
    size_of_float = 4
    prob_image_list_values = []

    image_name_list = []
    line = f_keyfile.readline().replace('\n', '')
    image_position = 0
    while line:
        offset = (number_of_category*image_position + category)*4
        f_binaryfile.seek(offset)
        temp = f_binaryfile.read(4)
        prob_image_list_values.append(struct.unpack('<f', temp)[0])
                
        image_name_list.append(line)

        image_position += 1
        line = f_keyfile.readline().replace('\n', '')
    
    prob_image_list_values = np.asarray(prob_image_list_values) 
    argsort = prob_image_list_values.argsort()[::-1]
    for i in range(0, len(argsort)):
        res.append({"id":str(argsort[i]), "name": image_name_list[argsort[i]], "prob": str(prob_image_list_values[argsort[i]])})
    
    return res

def search(collection, u_list, dataset, category, binaryfile):	
    path_to_image_folder = collections_dir_name + collection + '/JPG/images/'
    path_to_keyfile = collections_dir_name + collection + '/JPG/keylist.txt'
    path_to_bynaryfile = collections_dir_name + collection + '/data/' + dataset + '/' + binaryfile
    path_to_categoryfile = collections_dir_name + collection + '/data/' + dataset + '/categories.txt'
    
    if(u_list == ALL_IMAGES):
        res = sort_image_without_sublist(category, path_to_keyfile, path_to_bynaryfile, path_to_categoryfile)
    else:
        path_to_list_image_file = collections_dir_name + collection + '/list/' + u_list
        res = sort_image_with_sublist(category,path_to_keyfile, path_to_list_image_file, path_to_bynaryfile, path_to_categoryfile)

    print json.dumps(res) 


def main(argv):
    params = argv[1].split(',')
    search(params[0], params[1], params[2], int(params[3]), params[4])

if __name__ == "__main__":       
    main(sys.argv)
