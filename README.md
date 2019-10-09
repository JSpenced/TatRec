# TatRec #

A tattoo artist recommendation web app ([www.tatrec.xyz](http://www.tatrec.xyz)). The app simplifies the process of finding local tattoo artists that specialize in the style and content of your desired tattoo. You simply put in an image of your favorite tattoo or a tattoo similar to one that you want to get, and TatRec recommends local tattoo artists that have done similar tattoos.  
<img src="tatrec/static/img/tatrec_screenshot.png" width="600">

### Contents ###
* [Installation](#installation)
* [Running the Project](#running-the-project)
* [Demo](#demo)
* [Next Steps](#next-steps)
* [Links](#links)

##  Installation ##

If you have `conda` installed, then create a new virtual environment (using python 3.6+ as did not test whether fully compatible with lower versions) and activate the virtual environment:  
```
conda create -n tatrec python=3.6
conda activate tatrec
```

or if you use the normal python virtual environment package `venv` then run:  
```
python3 -m venv tatrec
source tatrec/bin/activate
```

Then clone the repo and enter the directory:  
```
git clone https://github.com/JspenceD/tatrec.git
cd tatrec
```

Install the packages from `requirements.txt`:  
```
pip install -r requirements.txt
```

## Running the Project ##

### Overview ###

The path to download the data is in the `<project_path>/scripts`. If you want to train the network yourself, the notebooks in `<project_path>/notebooks` can be used. The `<project_path>/tatrec` has files with supporting functions and classes including the `TatRecommender` class which is used on the back-end to perform similarity matching on the server when the user inputs an image.  

To run the flask server locally,  run `./server.py` at the command line in the `<project_path>` folder.  

### Download Data ###

To download the Instagram data used for the project, first create an Instagram credentials file `.insta-credentials` in the `scripts/` folder. This file is used to read in the username and password, so put on the first line in the file: `<username>,<password>`. After run on the command line, `chmod 400 .insta-credentials` to enable only the local user to read this file.

Next, run `scripts/instagram_scraping_images.py`, which will download the files into `data/raw/instagram/<city>/` folder.

### Tattoo vs Non-Tattoo Training ###

The neural network trained to recognize tattoo vs non-tattoo began with a ResNet50 network architecture trained on ImageNet and performed transfer learning using the notebook: `notebooks/transfer-learning-resnet50-tat-notat-images-v1.ipynb`. The final trained model was saved as `data/cleaned/models/tatrec-stage-2-1.pth`.

### CNN Feature Extraction and Inference ###

Then all the tattoo images were ran through the network and the second to last layer was extracted and flattened to use for LSH. The notebook `notebooks/image-similarity-for-tattoos-using-lsh-v1.ipynb` was ran to perform this step and build the LSH map using `LSHash` package. 

A list of the raw features extracted from the CNN are saved to `data/cleaned/chicago/feature_dict.pkl` and the LSH map is saved to `data/cleaned/models/<city>/lsh.pkl`. You can use `plot_simmilar_tats_idx()` to get the most similar tattoos to any image in `feature_dict.pkl` to check how well the similarity matching performs. The similarity matching uses `hamming distance` to calculate the similarity between images in the LSH index.

## Demo ##

### Overview ###

The first image under __*Get Recs*__ is the input tattoo and the four tattoos at the bottom are the recommendations. The top recommendation goes from left to right, so the most similar tattoo is on the left and the fourth most similar is on the right. The Instagram username and the link to their Instagram profile is provided below the image. Also, the number of followers for each user and the number of likes for that post is shown.
<img src="tatrec/static/img/tatrec_screenshot.png" width="900">

### Video ###

![Video of screen cast](tatrec/static/img/tatrec_screencast.gif)  

## Next Steps ##

  * [ ] Hand-label dataset into different tattoo styles and train the CNN to classify based on style instead of tattoo vs non-tattoo.
  * [ ] Hand-label a subset of the data to train a tattoo object detection network to extract just the tattoo from each image.
  * [ ] Train GAN to generate new tattoos using a style image and content image.
  * [ ] Download more cities tattoo artists.

## Links ##

[Slides](http://bit.ly/30VKjgB)  
[Website](http://www.tatrec.xyz)  
[Demo Video](https://youtu.be/2BRBcs8JVos)
