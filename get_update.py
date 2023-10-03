import os.path
from glob import glob
import zipfile

path = glob("./resource/py/*.*")
path += glob("./resource/src/img/*.*")
path += glob("./resource/src/sound/*.*")
path += glob("./resource/src/ui/*.*")
path += glob("./resource/src/config.json")

with zipfile.ZipFile('update/resource.zip', 'w') as myzip_all:
    for f in path:
        output = f.replace("./resource", ".")
        print(output)
        myzip_all.write(f, compress_type=zipfile.ZIP_DEFLATED)
    myzip_all.close()