import cv2
import numpy as np

def log(img, a):
    img = a*(np.log10((np.array(img)/255.)+1)).astype(np.float32)*255

    return img
 
img = cv2.imread("images/image_1b.png") #Abrir a imgem 

imgR = img[:,:,0]
imgG = img[:,:,1]
imgB = img[:,:,2]

imgR = log(imgR, 0.9)
imgG = log(imgG, 0.9)
imgB = log(imgB, 0.9)

imgF = cv2.merge((imgR, imgG, imgB))

#salvar imagem
salvar = "resultados/(escurecer-log0.9)image_1b.png"
cv2.imwrite(salvar, imgF)

#plotar imagem
cv2.imshow("imagem_1", imgF)
cv2.waitKey(0)
cv2.destroyAllWindows()