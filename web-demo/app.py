import web
import os
import json

collections_dir_name = '/home/anhtu/demo/collections/'

def make_text(string):
    return string+' NGUYEN'

urls = (
    '/', 'Index',
    '/collections', 'Collection',
    '/list', 'List',
    '/categories', 'Category',
    '/binaryfile','BinaryFile'
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
        if(not os.path.isdir(files_folder_name)):
            print "ERROR: Cannot exits folder : ",files_folder_name
            return json.dumps([])

        for name in os.listdir(files_folder_name):
            if(os.path.isfile(files_folder_name + '/' + name)):
                res.append(name)
        return json.dumps(res)

class Category:
    def GET(self):
        res = []
        request_data = web.input()
        categories_file = collections_dir_name + request_data.collection + '/data/categories.txt'
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
        binaryfile_folder = collections_dir_name + request_data.collection + '/data'

        if(not os.path.isdir(binaryfile_folder)):
            print "ERROR: Cannot exits folder : ",binaryfile_folder
            return json.dumps([])


        for foldername in os.listdir(binaryfile_folder):
            if(os.path.isdir(binaryfile_folder + '/' + foldername)):
                temp_group = {"text": foldername,"elment": "HTMLOptGroupElement"}
                chidren_array = []
                for filename in os.listdir(binaryfile_folder + '/' + foldername):
                    if(os.path.isdir(binaryfile_folder + '/' + foldername + '/' + filename)):
                        for root, dirs, files in os.walk(binaryfile_folder + '/' + foldername + '/' + filename):
                            for file in files:
                                filename = root.replace(binaryfile_folder + '/' + foldername + '/', '') + '/' + file
                    chidren_array.append({"id": foldername + '/' + filename, "text": filename, "element": "HTMLOptionElement"})
                    
                temp_group["children"] = chidren_array
                res.append(temp_group)
        return json.dumps(res)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
