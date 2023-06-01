import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode() # dilakukan encode decode agar dapat mengubah biner menjadi text
            print(f"tipe data isifile adalah {type(isifile)}")
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
        
    def post(self,params=[]):
        try:
            filename = params[0]
            isifile = base64.b64decode(params[1])
            if filename == '' or isifile == '':
                return None
            with open(filename, 'wb+') as fp:
                fp.write(isifile)
            return self.list()
        except Exception as e:
            return dict(status='ERROR',data=str(e))
    
    def delete(self, params=[]):
        try:
            filename = params[0]
            os.remove(filename)
            return self.list()
        except Exception as e:
            return dict(status='ERROR',data=str(e))

if __name__=='__main__':
    f = FileInterface()
    # print(f.list())
    print(f.get(['pokijan.jpg']))
