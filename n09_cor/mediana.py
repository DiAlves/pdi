import cv2
import numpy as np


def mediana(img, t):
    vizinhos = []
    aux = t // 2
    imgF = np.zeros((img.shape[0], img.shape[1]))
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for z in range(t):
                if i + z - aux < 0 or i + z - aux > img.shape[0] - 1:
                    for c in range(t):
                        vizinhos.append(0)
                else:
                    if j + z - aux < 0 or j + aux > img.shape[1] - 1:
                        vizinhos.append(0)
                    else:
                        for k in range(t):
                            vizinhos.append(img[i + z - aux][j + k - aux])

            vizinhos.sort()
            imgF[i][j] = vizinhos[len(vizinhos) // 2]
            vizinhos = []
            
    return imgF

#função responsavel pelo numero de vezes que o filtro passará na imagem
def passagemFiltro(img, filtro, n):
    imgAux = img
    for i in range(n):
        imgAux = mediana(imgAux, filtro)
    
    return imgAux

def componenteR(img):
    r = np.zeros((img.shape[0], img.shape[1]))
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            r.itemset((i, j), img.item(i, j, 0))
    return r


def componenteG(img):
    g = np.zeros((img.shape[0], img.shape[1]))
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            g.itemset((i, j), img.item(i, j, 1))
    return g

def componenteB(img):
    b = np.zeros((img.shape[0], img.shape[1]))
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            b.itemset((i, j), img.item(i, j, 2))
    return b

def juntarComponentes(img, imgR, imgG, imgB):
    imgFinal = img.copy()
    
    #Componente R
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            imgFinal.itemset((i, j, 0), imgR.item(i, j))
    
    #Componente G
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            imgFinal.itemset((i, j, 1), imgG.item(i, j))
    
    #Componente B
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            imgFinal.itemset((i, j, 2), imgB.item(i, j))
            
    return imgFinal
img = cv2.imread("images/image_2b.png") #Abrir a imgem 

imgR = componenteR(img)
salvar = "resultados/(R)image_2b.png"
cv2.imwrite(salvar, imgR)

imgG = componenteG(img)
salvar = "resultados/(G)image_2b.png"
cv2.imwrite(salvar, imgG)

imgB = componenteB(img)
salvar = "resultados/(B)image_2b.png"
cv2.imwrite(salvar, imgB)

imgR = passagemFiltro(imgR, 3, 6)
imgG = passagemFiltro(imgG, 3, 7)
imgB = passagemFiltro(imgB, 3, 4)

imgFinal = juntarComponentes(img, imgR, imgG, imgB)

#salvar imagem
salvar = "resultados/(mediana-6-7-4)image_2b.png"
cv2.imwrite(salvar, imgFinal)

#plotar imagem
cv2.imshow("imagem_1", imgFinal)
cv2.waitKey(0)
cv2.destroyAllWindows()





