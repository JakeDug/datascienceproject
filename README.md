# Pneumonia Recognition System
This application was created to aid medical profesionals in diagnosing pneumonia through a patients' x-ray

Created as part of 4th year Software Development data science module for lecturer Greg Doyle

# Image Recognition

The image classification training was done through the help of a tensorflow guide: https://www.tensorflow.org/hub/tutorials/image_retraining

The image training ingested a pre-trained model, Inceptionv3. Inceptionv3 is a neural network 
architecture for image classification publshed by Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, Zbigniew Wojna
in their paper ["Rethinking the Inception Architecture for Computer Vision"](https://arxiv.org/abs/1512.00567), 2015.

Our classification training trained another layer onto the inception model which classifies our images into PNEUMONNIA/NON-PNEUMONNIA

The 'image_classification_training' directory contains the Inceptionv3 model along with the training script and the testing script.
It also includes 4 model trained in different ways with different data.
These are:
- Model trained with 900 **clustered** images and tested with 100 images: 50% Accuracy
- Model trained with 900 **unclustered** images and tested with 100 images: 93% Accuracy
- Model trained with 2520 **clustered** images and tested with 200 images: 93.5% Accuracy
- Model trained with 2520 **unclustered** images and tested with 200 images: 95.5% Accuracy
	
Along with each model is a .csv file with logged which predictions were correct from the testing set for each model.
At the bottom of the .csv files there is a count of all the correct and incorrect predictions.

The clustered images and unclustered image sets are identical apart from the clustering and so comparisons can be drawn
between the two sets in relation to accuracy, time taken to train, image size etc.

The image clustering is descibed in the following section

For the web application to make a successful prediction, it requires the retrained_graph.pb file which contains the neural-network

# K-means Clustering 

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
