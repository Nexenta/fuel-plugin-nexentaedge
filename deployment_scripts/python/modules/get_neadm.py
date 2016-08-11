import os
import tarfile
import tempfile
from nexentaedge.settings import Settings
from utils import download

if os.path.exists(Settings.NEADM_FOLDER_PATH):
    print('NEADM is already present')
else:
    print('Downloading NEADM')
    path = os.path.join(tempfile.gettempdir(), Settings.NEADM_FILE_NAME)
    download(Settings.NEADM_REPO_PATH, path)
    print('NEADM has been downloaded successfully')
    print('Unpacking NEADM')
    tar = tarfile.open(path)
    tar.extractall(Settings.NEDGE_FOLDER_PATH)
    tar.close()
    print('NEADM has been unpacked successfully')
