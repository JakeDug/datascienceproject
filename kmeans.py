import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime

def listFiles(path):
	return os.listdir(path)

def main():

	path = "C:/Users/Jake/Documents/chest_xray/test/NORMAL/" #input dir

	file_names = listFiles(path)
	outputPath = "C:/Users/Jake/Documents/chest_xray/kmeans/train/normal/" #output dir dont forget backslash
	
	startTime = datetime.datetime.now()

	for i in range(len(file_names)):

		imgName = file_names[i]
		imgpath = path + imgName

		img = cv2.imread(imgpath, 1)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		
		Z = img.reshape((-1,3))
		Z = np.float32(Z)
		
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
		
		# Change the value of K to change number of clusters
		K=8
		
		print(path + imgpath)
		
		ret, label1, center1 = cv2.kmeans(Z, K, None,
										  criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
		center1 = np.uint8(center1)
		res1 = center1[label1.flatten()]
		output = res1.reshape((img.shape))

		output = [img, output]
		titles = ['Original Image', imgName + ' K = ' + str(K)]
		

		plt.imshow(output[1], aspect='auto')
		plt.xticks([])
		plt.yticks([])
		plt.savefig(outputPath + "clustered_" + imgName);

		print("---> " + str(i+1) + " OF " + str(len(file_names)) + " PROCESSED")
		
		
	print("\n\n\n Start Time: " + str(startTime) + " End Time " + str(datetime.datetime.now()))


if __name__ == "__main__":
	main()
