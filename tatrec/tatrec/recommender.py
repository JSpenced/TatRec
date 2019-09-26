import pickle
import numpy as np
from fastai.metrics import error_rate
from fastai.vision import cnn_learner
from fastai.vision import models
from fastai.basic_data import load_data
# import sys
# Ensure tatrec package is in the path
# sys.path.append(os.path.join(Path.cwd(), "..", "tatrec"))
from .notebook_funcs import get_data_from_folder
from .config import (path_web_models, path_web_cleaned_chicago, path_web_upload,
                     path_web_models_chicago, path_web_data)


class TatRecognizer:
    def __init__(self):
        self.data = load_data(path_web_cleaned_chicago, "databunch-lsh.pkl")
        self.arch = models.resnet50
        self.learn = cnn_learner(self.data, self.arch, metrics=error_rate)
        self.learn.load("tatrec-stage-2-1")
        self.sf = SaveFeatures(self.learn.model[1][5])
        self.lsh = pickle.load(open(path_web_models_chicago + 'lsh.pkl', 'rb'))
        self.n_items = 5
        self.path_img_upload = path_web_upload
        self.distance_func = 'hamming'
        self.input_image = None
        self.preds = None

    def get_tattoo_recs(self, path_img_upload=path_web_upload):
        data = get_data_from_folder(path_img_upload, 1, 64)
        self.learn.data = data
        self.learn.get_preds(data.train_ds)[0]
        query = self.sf.features[-1].flatten()
        response = self.lsh.query(query, num_results=self.n_items,
                                  distance_func=self.distance_func)
        img_rec1 = path_web_data + response[0][0][1][27:]
        img_rec2 = path_web_data + response[1][0][1][27:]
        img_rec3 = path_web_data + response[2][0][1][27:]
        img_rec4 = path_web_data + response[3][0][1][27:]
        img_rec5 = path_web_data + response[4][0][1][27:]
        return (img_rec1, img_rec2, img_rec3, img_rec4, img_rec5)


class SaveFeatures():
    """This is a hook (used for saving intermediate computations) used to extract before the last FC
    layer for use in similarity matching.
    """
    features = None

    def __init__(self, m):
        self.hook = m.register_forward_hook(self.hook_fn)
        self.features = None

    def hook_fn(self, module, input, output):
        out = output.detach().cpu().numpy()
        if isinstance(self.features, type(None)):
            self.features = out
        else:
            self.features = np.row_stack((self.features, out))

    def remove(self):
        self.hook.remove()
