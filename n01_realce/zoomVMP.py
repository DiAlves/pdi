import cv2
import argparse
import numpy as np

# Receber o diretorio da imagem e o valor do gamma
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a image")
ap.add_argument("-w", "--width", required=True,	help="valor do redimensionamento desejado na largura")
ap.add_argument("-he", "--height", required=True, help="valor do redimensionamento desejado na altura")
args = vars(ap.parse_args())

img = cv2.imread(args["image"], 0)
h = int(args["height"])
w = int(args["width"])

# Fatores do redimensionamento
novaEscalaH = float(h)/float(img.shape[0])
novaEscalaW = float(w)/float(img.shape[1])

auxImg = np.zeros((h, w)) 

for i in range(auxImg.shape[0]):
    for j in range(auxImg.shape[1]):
        auxImg[i, j] = img[int(i/novaEscalaH), int(j/novaEscalaW)]

#salvar imagem
salvar = "resultados/VMP" + args["image"][7:]
cv2.imwrite(salvar, auxImg)

#plotar imagem
cv2.imshow("imagem", auxImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
            