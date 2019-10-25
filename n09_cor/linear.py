import cv2
import numpy as np 

def linear(img, a, b):
    img = np.array(img)*a + b

    return img

img = cv2.imread("images/image_1a.png") #Abrir a imgem 

imgR = img[:,:,0]
imgG = img[:,:,1]
imgB = img[:,:,2]

imgR = linear(imgR, 1.9, 0)
imgG = linear(imgG, 1.9, 0)
imgB = linear(imgB, 1.9, 0)

imgF = cv2.merge((imgR, imgG, imgB))

#salvar imagem
salvar = "resultados/(clarear-linear1.9)image_1a.png"
cv2.imwrite(salvar, imgF)

#plotar imagem
cv2.imshow("imagem_1", imgF)
cv2.waitKey(0)
cv2.destroyAllWindows()