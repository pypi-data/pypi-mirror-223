from os import path


class sdk_data():
    urls=[]
    files=[]

    def add_data(self,url:str, encrypt_remote: True):
        self.urls.append({"url":url,"encrypt":encrypt_remote})

    def add_data(self,data:path, encrypt_remote: True):
        self.files.append({"file":data,"encrypt":encrypt_remote})
        
    def write_json(self,notebook:str):
        try:
            f = open(notebook+".data","w")
            f.write('{\n')
            for url in self.urls:
                f.write("   {'url':{'name':%s,'encrypt':%s}}\n" % (url["url"],url("encrypt")))
            for file in self.files:
                f.write("   {'file':{'name':%s,'encrypt':%s}}\n" % (file["file"],file("encrypt")))
            f.write('\n}')
        finally:
            if f != None:
                f.close()


