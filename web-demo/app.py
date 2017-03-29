import web
import os
import json
import numpy as np
import struct

def get_collections_dir_name():
    path_to_app = os.path.abspath(os.path.dirname(__file__))
    temp = path_to_app.split('/')
    return '/'.join(temp[0:len(temp)-1]) + '/collections/'

collections_dir_name = get_collections_dir_name()
ALL_IMAGES = 'all/images'

urls = (
    '/', 'Index',
    '/collections', 'Collection',
    '/list', 'List',
    '/dataset', 'Dataset',
    '/categories', 'Category',
    '/binaryfile','BinaryFile',
    '/search','Search',
    '/images', 'Image'
)

render = web.template.render('templates/')

class Index:
    def GET(self):
        return render.index()


class Collection:
    def GET(self):
        res = []
        global collections_dir_name
        for name in os.listdir(collections_dir_name):
            if os.path.isdir(collections_dir_name + name):
                res.append(name)
        return json.dumps(res)

class List:
    def GET(self):
        res = []
        request_data = web.input()
        files_folder_name = collections_dir_name + request_data.collection + '/list'
        res.append({"id": ALL_IMAGES, "text": "all images"})
        if(not os.path.isdir(files_folder_name)):
            print "ERROR: Cannot exits folder : ",files_folder_name
            return json.dumps([])

        for name in os.listdir(files_folder_name):
            if(os.path.isfile(files_folder_name + '/' + name)):
                res.append({"id": name, "text": name})
        return json.dumps(res)

class Dataset:
    def GET(seft):
        res = []
        request_data = web.input()
        datasetfolder = collections_dir_name + request_data.collection + '/data'
        if(not os.path.isdir(datasetfolder)):
            print "ERROR: Cannot exits folder : ",datasetfolder
            return json.dumps([])

        for name in os.listdir(datasetfolder):
            if(os.path.isdir(datasetfolder + '/' + name)):
                res.append({"id": name, "text": name})
        return json.dumps(res)

class Category:
    def GET(self):
        res = []
        request_data = web.input()
        collection = request_data.collection
        dataset = request_data.dataset
        categories_file = collections_dir_name + collection + '/data/' + dataset + '/categories.txt'

        try:
            fin = open(categories_file, 'r')
        except:
            print "ERROR: Cannot open file " + categories_file
            return []
        line = fin.readline()
        while line:
            temp = line.split(' ')
            res.append({"id": temp[0], "text": temp[1]})
            line = fin.readline()

        return json.dumps(res)

class BinaryFile:
    def GET(selt):
        res = []
        request_data = web.input()
        collection = request_data.collection
        dataset = request_data.dataset
        binaryfile_folder = collections_dir_name + request_data.collection + '/data/' + dataset

        if(not os.path.isdir(binaryfile_folder)):
            print "ERROR: Cannot exits folder : ",binaryfile_folder
            return json.dumps([])

        for net_foldername in os.listdir(binaryfile_folder):
            if(os.path.isdir(binaryfile_folder + '/' + net_foldername)):
                temp_group = {"text": net_foldername,"elment": "HTMLOptGroupElement"}
                chidren_array = []
                for name in os.listdir(binaryfile_folder + '/' + net_foldername):
                    if(os.path.isdir(binaryfile_folder + '/' + net_foldername + '/' + name)):
                        for root, dirs, files in os.walk(binaryfile_folder + '/' + net_foldername + '/' + name):
                            for file in files:
                                if file.endswith('.bin'):
                                    filename = root.replace(binaryfile_folder + '/' + net_foldername + '/', '') + '/' + file
                                    chidren_array.append({"id": filename, "text": filename, "element": "HTMLOptionElement"})
                    else:
                        if name.endswith('.bin'):
                            chidren_array.append({"id": net_foldername + '/' + name, "text": name, "element": "HTMLOptionElement"})

            temp_group["children"] = chidren_array
            res.append(temp_group)

        return json.dumps(res)

class Image:
    def GET(self):
        path_to_image = collections_dir_name + web.input().path
        ext = path_to_image.split(".")[-1]
        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"
            }

        try:
            f_in = open(path_to_image,"rb")
        except:            
            print 'ERROR: Cannot open the image at: ',path_to_image
            raise web.notfound()
        
        web.header("Content-Type", cType[ext])
        return f_in.read()

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
        print 'ERROR: Cannot open file : ',path_to_keyfile, path_to_categoryfile, path_to_list_image_file, path_to_bynaryfile
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
            print "ERROR: The image not exists at line : ", image_key
            sys.exit()

        offset = (number_of_category*image_position + category)*4
        f_binaryfile.seek(offset)
        temp = f_binaryfile.read(4)
        prob_image_list_values.append(struct.unpack('<f', temp)[0])
        image_list_name.append(image_key)
        image_key = f_listimage.readline().replace('\n', '')
        
    prob_image_list_values = np.asarray(prob_image_list_values) 
    argsort = prob_image_list_values.argsort()[::-1]
    for i in range(0, len(argsort)):
        res.append({"name": image_list_name[argsort[i]], "prob": str(prob_image_list_values[argsort[i]])})
    
    return res

def sort_image_without_sublist(category, path_to_keyfile, path_to_bynaryfile, path_to_categoryfile):
    res = []
    try:
        f_keyfile = open(path_to_keyfile, 'r')
        f_categoryfile = open(path_to_categoryfile, 'r')
        f_binaryfile = open(path_to_bynaryfile, 'r')
    except:
        print 'ERROR: Cannot open file : ',path_to_keyfile, path_to_categoryfile, path_to_bynaryfile
        return res

    categories = read_categories(f_categoryfile)

    image_list = []
    line = f_keyfile.readline().replace('\n', '')
    while line:
        image_list.append(line)
        line = f_keyfile.readline().replace('\n', '')

    # read probabilities values for category selected that coressponse with each images
    number_of_category = len(categories)
    size_of_float = 4
    number_byte_each_image = number_of_category*size_of_float
    prob_image_list_values = []
    buff_image_probs = f_binaryfile.read(number_byte_each_image)
    while buff_image_probs:
        float_array = np.frombuffer(buff_image_probs, dtype='<f', count = -1, offset = 0)
        prob_image_list_values.append(float_array[category])
        buff_image_probs = f_binaryfile.read(number_byte_each_image)
    
    prob_image_list_values = np.asarray(prob_image_list_values) 
    argsort = prob_image_list_values.argsort()[::-1]
    for i in range(0, len(argsort)):
        res.append({"name": image_list[argsort[i]], "prob": str(prob_image_list_values[argsort[i]])})
    
    return res


class Search:
    def GET(self):
        request_data = web.input()
        collection = request_data.collection
        u_list = request_data.list
        dataset = request_data.dataset
        category = int(request_data.category)
        binaryfile = request_data.binaryfile

        path_to_image_folder = collections_dir_name + collection + '/JPG/images/'
        path_to_keyfile = collections_dir_name + collection + '/JPG/keylist.txt'
        path_to_bynaryfile = collections_dir_name + collection + '/data/' + dataset + '/' + binaryfile
        path_to_categoryfile = collections_dir_name + collection + '/data/' + dataset + '/categories.txt'
        
        if(u_list == ALL_IMAGES):
            res = sort_image_without_sublist(category, path_to_keyfile, path_to_bynaryfile, path_to_categoryfile)
        else:
            path_to_list_image_file = collections_dir_name + collection + '/list/' + u_list
            res = sort_image_with_sublist(category,path_to_keyfile, path_to_list_image_file, path_to_bynaryfile, path_to_categoryfile)

        return json.dumps(res) 


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
