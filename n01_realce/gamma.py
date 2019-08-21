import cv2
import argparse
from matplotlib import pyplot as plt

# Receber o diretorio da imagem e o valor do gamma
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a image")
ap.add_argument("-g", "--gamma", required=True,	help="valor do gamma")
args = vars(ap.parse_args())
 
img = cv2.imread(args["image"], 0) #Abrir a imgem 

#Criar uma imagem normalizada
imgN = img.astype('float32')
imgN /= 255
gamma = float(args["gamma"])


for i in range (0, imgN.shape[0]):
    for j in range (0, imgN.shape[1]):
        imgN.itemset((i, j), imgN.item(i, j) ** (1 / gamma)) 

imgN *= 255
imgN = imgN.astype('uint8')
        

#plotar histograma
plt.hist(imgN.ravel(),256,[0,256])
plt.hist(img.ravel(),256,[0,256])
plt.title('Histograma_1')
plt.show()

#salvar imagem
salvar = "resultados/" + args["image"][7:]
cv2.imwrite(salvar, imgN)

#plotar imagem
cv2.imshow("imagem_1", imgN)
cv2.waitKey(0)
cv2.destroyAllWindows()

