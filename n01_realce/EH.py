import cv2
import argparse
import numpy as np
from matplotlib import pyplot as plt

# Receber o diretorio da imagem e o valor do gamma
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"], 0) #Abrir a imgem 
imgR = cv2.imread(args["image"], 0) #Abrir a imgem 
n = plt.hist(img.ravel(),256,[0,256])
escala = np.amax(np.array(img))


# probabilidade de cada pixel
p = []
for i in range (0, 256):
    p.append(n[0][i]/(img.shape[0]*img.shape[1]))
    
# calculo da probabilidade acumulativa 
cp = []
cp.append(p[0])

for i in range (1, 256):
    cp.append(cp[i-1] + p[i])

# multiplicando pelo fator
cpf = []
for i in range (0, 256):
    cpf.append(int(cp[i]*(255)))
    
for i in range (0, img.shape[0]):
    for j in range (0, img.shape[1]):
        imgR.itemset((i, j), cpf[img.item(i, j)]) 
        
# plotagem dos histogramas
plt.hist(imgR.ravel(),256,[0,256])
plt.hist(img.ravel(),256,[0,256])
plt.title('Histograma_1')
plt.show()

#salvar imagem
salvar = "resultados/EH" + args["image"][7:]
cv2.imwrite(salvar, imgR)

#plotar imagem
cv2.imshow("imagem", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()
    