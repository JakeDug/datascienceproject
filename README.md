# Pneumonia Recognition System
This application was created to aid medical profesionals in diagnosing pneumonia through a patients' x-ray

Created as part of 4th year Software Development data science module for lecturer Greg Doyle

# Image Recognition

The image classification training was done through the help of a tensorflow guide: https://www.tensorflow.org/hub/tutorials/image_retraining

The image training ingested a pre-trained model, Inceptionv3. Inceptionv3 is a neural network 
architecture for image classification publshed by Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, Zbigniew Wojna
in their paper "Rethinking the Inception Architecture for Computer Vision", 2015.

Our classification training trained another layer onto the inception model which classifies our images into PNEUMONNIA/NON-PNEUMONNIA

The 'image_classification_training' directory contains the Inceptionv3 model along with the training script and the testing script.
It also includes 4 model trained in different ways with different data.
These are:
	- Model trained with 900 **clustered** images and tested with 100 images
	- Model trained with 900 **unclustered** images and tested with 100 images
	- Model trained with 2520 **clustered** images and tested with 200 images
	- Model trained with 2520 **unclustered** images and tested with 200 images
	
Along with each model is a .csv file with logged which predictions were correct from the testing set for each model.

The clustered images and unclustered image sets are identical apart from the clustering and so comparisons can be drawn
between the two sets in relation to accuracy, time taken to train, image size etc.

The image clustering is descibed in the following section 

# K-means Clustering 
The images were clustered in order to minimize storage space for each image without sacrificing too much accuracy. Using the OpenCV library for python the images were clustered with k=8. The clustered images were then re-drawn using matplotlib.
 The clustering aspect of this project is divided into 2 parts.
1. Bulk clustering of images. This clustered the dataset used to train the model, this meant that given a clustered image the model would better be able to identify whether it had pneumonia or not.

2. Individually clustering an image. This clustering was done on an individual image at the time of upload. This ensured that the image was taking up the minimum amount of storage space and that it could be identified with an acceptable level of confidence by the model trained with other clustered images.

The concept of using k-means clustering for this project was originally derived from the reading of: 
Ng, H. P. et al. “Medical Image Segmentation Using K-Means Clustering and Improved Watershed Algorithm.” 2006 IEEE Southwest Symposium on Image Analysis and Interpretation (2006): 61-65.

https://www.semanticscholar.org/paper/Medical-Image-Segmentation-Using-K-Means-Clustering-Ng-Ong/bd7e1df00e462d8272dc2e69639bdb89dfb6340b

# Web application 
Created using Python and FLask with the help of the following libraries
- flask login
- flask sqlalchemy
- wtforms
- flask bootstrap
- flask wtf
- flask_upload
- werkzeug

# Team 
- Adriaan Van Wyk
- Jake Duggan
- Neil Grogan

# Live app on python anywhere (Still in progress)
http://pneumoniarecognition.pythonanywhere.com/

pythonanywhere version is not up to date with working app
