### Custom Dataset Generation
Custom dataset generation for image classification based on images downloaded from Google.

- [image_download.py](https://github.com/sotirismos/Custom-Dataset-Generation/blob/main/src/utils/image_download.py) is a script containing class methods related to images download and saving, plus the creation of a directory to store those downloaded images.

- [logging.py](https://github.com/sotirismos/Custom-Dataset-Generation/blob/main/src/utils/logging.py) is an auxiliary script used for logging.

- [train_test_split.py](https://github.com/sotirismos/Custom-Dataset-Generation/blob/main/src/utils/train_test_split.py) is a script containing functions to split the download images to train, test subsets based on **train_ratio** argument of `split` function.

- [detect_n_crop.py](https://github.com/sotirismos/Custom-Dataset-Generation/blob/main/src/detect_n_crop.py) applies a deep learning model pretrained on BDD100K dataset and is able to detect the following objects from the downloaed images.
  - Pedestrian
  - Rider
  - Car
  - Truck
  - Bus
  - Train
  - Motorcycle
  - Bicycle
  - Traffic light
  - Traffic sign
  
  **In our case, we downloaded pictures from different car models, applied the car detection model to clean up the dataset, resulting to a car brand      detection dataset with minimal effort, as analyzed in the notebook**.
