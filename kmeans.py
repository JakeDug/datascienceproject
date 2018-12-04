import cv2
import matplotlib.pyplot as plt
import numpy as np

def main():
    
    path = "C:/Users/Jake/Documents/chest_xray/train/NORMAL/"
    imgName = "IM-0115-0001.jpeg"
    imgpath = path + imgName

    img = cv2.imread(imgpath, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    Z = img.reshape((-1,3))
    Z = np.float32(Z)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    # Change the value of K to change number of clusters
    K=2
    
    print(path + imgpath)
    
    ret, label1, center1 = cv2.kmeans(Z, K, None,
                                      criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center1 = np.uint8(center1)
    res1 = center1[label1.flatten()]
    output = res1.reshape((img.shape))

    output = [img, output]
    titles = ['Original Image', imgName + 'K = ' + str(K)]
    
    for i in range(2):
        plt.subplot(2, 1, i+1)
        plt.imshow(output[i])
        plt.title(titles[i])
        plt.xticks([])
        plt.yticks([])
    plt.show()

if __name__ == "__main__":
    main()
