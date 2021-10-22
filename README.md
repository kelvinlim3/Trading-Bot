# Fine-Grained Localisation
Final assignment for Computer Vision (COMP90086). Given a dataset of images with their associated location label, we aim to investigate methods to recognize the location of an unlabelled image. To this end, we benchmarked various feature decriptors/extractors and image matching techniques.

<br/><b>Descriptors/Features:</b>
- SIFT
- ASIFT
- NetVLAD (<a href="https://github.com/crlz182/Netvlad-Keras">Original Code</a>)
- Self-supervised CNN (Rotation)
- Self-supervised CNN (Warping)

<b>Image Matching:</b>
- KNN
- FLANN
- MLP

### Dependencies
This program was developed using:
1. Python 3.9.7
2. Keras 2.6.0
3. Tensorflow 2.6.0

<br/>
Pretrained weights for NetVLAD "netvlad_weights.h5" must be downloaded and put into the <b>checkpoint</b> directory before running. Download <a href="https://onedrive.live.com/?authkey=%21AM3LfsRZTJ1TOHI&cid=318792FBF3A5A7EB&id=318792FBF3A5A7EB%21290981&parId=318792FBF3A5A7EB%21290980&action=locate">here</a> 
(Obtained from Github <a href="https://github.com/crlz182/Netvlad-Keras">repository</a> "Netvlad-Keras")


### How to Run the Code
The main file is "Experiments.ipynb"
After running, the extracted features are stored in the checkpoint directory. Additonally, 'predictions_netvlad_knn.csv' is the final prediction output used for the Kaggle competition (<a href="https://www.kaggle.com/c/comp90086-2021/overview">link</a>).
