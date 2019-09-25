from fastai.vision import ImageList, imagenet_stats, get_transforms

# Notebook helper functions


def get_data_from_folder(path, bs, img_size, tfms=get_transforms(), extensions=[".jpg"]):
    """Takes Imagenet style folder structure of test/train/valid and returns DataBunch with different
    batch and image sizes to train with PyTorch.

    Args
    ----------
    path : path to folder with data in train/valid/test folder structure
    bs : batch size
    img_size : resize to img_size for training
    tfms : transformations to do
    extensions : extensions to grab from the folder path

    Returns
    -------
    data : DataBunch from fastai library for training images in PyTorch

    """
    data = (ImageList.from_folder(path, extensions=extensions)
            .split_by_folder()
            .label_from_folder()
            .transform(tfms, size=img_size)
            .databunch(bs=bs, num_workers=0).normalize(imagenet_stats))
    return data
