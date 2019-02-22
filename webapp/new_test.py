# classify_image.py

import os
import tensorflow as tf
import numpy as np
import cv2

RETRAINED_GRAPH_PB_FILE_LOC = os.getcwd() + "\\" + "retrained_graph.pb"
TEST_IMAGES_DIR = os.getcwd() + "static\\user_xrays"

def classify_image(image_path, filename):

    classifications = ['NORMAL', 'PNEUMONIA']

    with tf.gfile.FastGFile(RETRAINED_GRAPH_PB_FILE_LOC, 'rb') as retrainedGraphFile:
        # instantiate a GraphDef object
        graphDef = tf.GraphDef()
        # read in retrained graph into the GraphDef object
        graphDef.ParseFromString(retrainedGraphFile.read())
        # import the graph into the current default Graph, note that we don't need to be concerned with the return value
        _ = tf.import_graph_def(graphDef, name='')
    # end with

    with tf.Session() as sess:
        imageFileWithPath = os.path.join(image_path, filename)

        openCVImage = cv2.imread(imageFileWithPath)

        finalTensor = sess.graph.get_tensor_by_name('final_result:0')

        # convert the OpenCV image (numpy array) to a TensorFlow image

        tfImage = np.array(openCVImage)[:, :, 0:3]

        # run the network to get the predictions
        predictions = sess.run(finalTensor, {'DecodeJpeg:0': tfImage})

        # sort predictions from most confidence to least confidence
        sortedPredictions = predictions[0].argsort()[-len(predictions[0]):][::-1]

        return classifications[sortedPredictions[0]], "{0:.2f}".format(predictions[0][sortedPredictions[0]]*100)

