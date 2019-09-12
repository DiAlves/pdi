import cv2
import argparse
from matplotlib import pyplot as plt
import random

def unipolar(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # Calculo da probablidade, no caso uma probabilidade de 15%
            if random.randint(0, 19) in [0, 1, 2]:
                img[i, j] = 0
    
    return img

# Receber o diretorio da imagem
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"], 0) #Abrir a imgem
plt.hist(img.ravel(),256,[0,256])
plt.title('Histrograma Imagem Original')
plt.show()

imgResultante = unipolar(img) 

#plotar histograma
plt.hist(imgResultante.ravel(),256,[0,256])
plt.title('Histrograma Imagem Resultante')
plt.show()


#salvar imagem
salvar = "resultados/" + args["image"][7:]
cv2.imwrite(salvar, imgResultante)

#plotar imagem
cv2.imshow("imagem_1", imgResultante)
cv2.waitKey(0)
cv2.destroyAllWindows()

