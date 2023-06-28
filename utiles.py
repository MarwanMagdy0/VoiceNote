import json
import os
class JsonIt:
    def __init__(self,name):
        self.name = name
        try:
            f=open(f'{self.name}','r')
            data=json.load(f)
            f.close()
        except:
            data = {}
            dump =json.dumps(data)
            file = open(f'{name}','w')
            file.write(dump)
            file.close()
    def save_data(self,Data):
        with open(f'{self.name}','w') as f:
            dic=json.dumps(Data)
            f.write(dic)

    def read_data(self):
        f=open(f'{self.name}','r')
        data=json.load(f)
        f.close()
        return data
    
    def __getitem__(self,key):
        f=open(f'{self.name}','r')
        data=json.load(f)
        f.close()
        return data.get(key)
    
    def __repr__(self):
        f=open(f'{self.name}','r')
        f.close()
        return str(json.load(f))


def folder2dict(folder_name = "test_folder"):
    structure = {}
    for groups in os.listdir(folder_name):
        print(groups)


if __name__ == "__main__":
    folder2dict()