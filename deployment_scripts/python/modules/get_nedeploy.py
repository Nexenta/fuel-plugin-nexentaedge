import urllib
import os
import tarfile
import tempfile
from nexentaedge.settings import Settings

if os.path.exists(Settings.NEDEPLOY_FOLDER_PATH):
    print('NEDEPLOY is already present')
else:
    print('Downloading NEDEPLOY')
    path = os.path.join(tempfile.gettempdir(), Settings.NEDEPLOY_FILE_NAME)
    urllib.urlretrieve(Settings.NEDEPLOY_REPO_PATH, path)
    print('NEDEPLOY has been downloaded successfully')
    print('Unpacking NEDEPLOY')
    tar = tarfile.open(path)
    tar.extractall(Settings.NEDGE_FOLDER_PATH)
    tar.close()
    print('NEDEPLOY has been unpacked successfully')
