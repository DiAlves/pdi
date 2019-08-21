import cv2
import argparse
import numpy as np

def bilinear(img, posI, posJ):
	#Parte inteira do produto da coordenada pelo fator de atualização
	posI_Inteiro = int(posI)
	posJ_Inteiro = int(posJ)
    
    #Parte decimal do produto da coordenada pelo fator de atualização
	posI_Deci = posI - posI_Inteiro
	posJ_Deci = posJ - posJ_Inteiro
    
    # Compara dois valores para não sair da matriz
	limiteI = min(posI_Inteiro+1,img.shape[1]-1)
	limiteJ = min(posJ_Inteiro+1,img.shape[0]-1)
 
	# Pixels vizinhos para analise
	bl = img[posJ_Inteiro, posI_Inteiro]
	br = img[posJ_Inteiro, limiteI]
	tl = img[limiteJ, posI_Inteiro]
	tr = img[limiteJ, limiteI]
    
 	# Calculo da interpolação
	b = posI_Deci * br + (1. - posI_Deci) * bl
	t = posI_Deci * tr + (1. - posI_Deci) * tl
	pxf = posJ_Deci * t + (1. - posJ_Deci) * b
	
	return int(pxf+0.5)    

# Receber o diretorio da imagem e o valor do gamma
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a image")
ap.add_argument("-w", "--width", required=True,	help="valor do redimensionamento desejado na largura")
ap.add_argument("-he", "--height", required=True, help="valor do redimensionamento desejado na altura")

args = vars(ap.parse_args())

img = cv2.imread(args["image"], 0)
h = int(args["height"])
w = int(args["width"])

# Imagem que será gerada(no método bilinear) a partir da imagem passada
auxImg = np.zeros((h, w)) 

# Fatores do redimensionamento
novaEscalaH = float(img.shape[0])/float(h)
novaEscalaW = float(img.shape[1])/float(w)


for i in range(h):
    for j in range(w):
        # Encontrar a posição original na imagem
        posI = i * novaEscalaH 
        posJ = j * novaEscalaW
        auxImg[i, j] = bilinear(img, posJ, posI)
        

#salvar imagem
salvar = "resultados/" + args["image"][7:]
cv2.imwrite(salvar, auxImg)

#plotar imagem
cv2.imshow("imagem", auxImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
            