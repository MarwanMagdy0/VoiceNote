import json
import os, sys
import time
from typing import Any

# if len(sys.argv)==1:
#     sys.argv.append(r"C:\Users\hp\Desktop\new.vnote")

SCRIPT_DIRECTORY    = os.path.dirname(os.path.realpath(__file__)) + "\\"
# USER_FILE_DIRECTORY = sys.argv[1][:-6] # C:\Users\hp\Desktop\new

class JsonIt:
    def __init__(self,file_directory):
        self.file_directory = file_directory
        try:
            f=open(f'{self.file_directory}','r')
            data=json.load(f)
            f.close()
        except:
            data = {}
            dump =json.dumps(data)
            file = open(f'{file_directory}','w')
            file.write(dump)
            file.close()

    def save_data(self,Data):
        with open(f'{self.file_directory}','w') as f:
            dic=json.dumps(Data)
            f.write(dic)

    def read_data(self):
        f=open(f'{self.file_directory}','r')
        data=json.load(f)
        f.close()
        return data
    
    def __getitem__(self,key):
        f=open(f'{self.file_directory}','r')
        data=json.load(f)
        f.close()
        return data.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        with open(self.file_directory, "r") as f:
            data = json.load(f)
        if key not in data.keys():
            os.mkdir(USER_FILE_DIRECTORY + "//" + key)
        with open(self.file_directory, "w") as f:
            data[key] = value
            f.write(json.dumps(data))


def get_time():
    return str(int(time.time()))



if __name__ == "__main__":
    json_file = JsonIt(sys.argv[1])
    init_group = {"group-name":"Title_0", "items":[]}

    # Checking if the .vnote file is not empty and if it was , dump the initial directory data to it
    with open(sys.argv[1], "r") as f:
        if f.read() == "":
            group_fname = get_time()
            if not os.path.isdir(USER_FILE_DIRECTORY):
                os.mkdir(USER_FILE_DIRECTORY)
    print(USER_FILE_DIRECTORY)