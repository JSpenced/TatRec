# config.py
import os
from pathlib import Path

# Global paths
path_project = Path(os.path.join(os.path.expanduser('~'), 'tatrec'))
path_data = path_project / 'data'
path_data_proc = path_data / 'processed'
path_data_raw = path_data / 'raw'
path_data_clean = path_data / 'cleaned'
path_train_cnn = path_data_proc / 'tat_notat'
path_data_upload = path_data / 'upload'
path_models = path_project / 'models'
path_scripts = path_project / 'scripts'

# City paths
path_raw_chicago = path_data_raw / 'instagram/chicago/'
path_train_chicago = path_data_proc / 'instagram/chicago/'
path_cleaned_chicago = path_data_clean / 'chicago/'
path_models_chicago = path_models / 'chicago/'

# Web server paths
path_web_data = 'static/data/'
path_web_img = 'static/img/'
path_web_upload = path_web_data + 'upload/'
path_web_upload_user = path_web_upload + 'train/user/'
path_web_cleaned_chicago = path_web_data + 'cleaned/chicago/'
path_web_models = path_web_data + 'models/'
path_web_models_chicago = path_web_cleaned_chicago + 'models/chicago/'
