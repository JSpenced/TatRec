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
path_models = path_project / 'models'
path_data_upload = path_data / 'upload'

# City paths
path_raw_chicago = path_data_raw / 'instagram/chicago/'
path_train_chicago = path_data_proc / 'instagram/chicago/'
path_cleaned_chicago = path_data_clean / 'chicago/'
path_models_chicago = path_models / 'chicago/'
