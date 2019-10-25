import cv2
import numpy as np
from matplotlib import pyplot as plt

def eh(img, n):
    imgE = np.zeros((img.shape[0], img.shape[1]))
    
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
            imgE.itemset((i, j), cpf[int(img.item(i, j))]) 
    
    return imgE

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

img = cv2.imread("images/image_1b.png") #Abrir a imgem 
imgR = componenteR(img)
imgG = componenteG(img)
imgB = componenteB(img)

nR = plt.hist(imgR.ravel(),256,[0,256])
nG = plt.hist(imgG.ravel(),256,[0,256])
nB = plt.hist(imgB.ravel(),256,[0,256])


imgR = eh(imgR, nR)
imgG = eh(imgG, nG)
imgB = eh(imgB, nB)

imgFinalE = juntarComponentes(img, imgR, imgG, imgB)

#salvar imagem
salvar = "resultados/(EH)image_1b.png"
cv2.imwrite(salvar, imgFinalE)

#plotar imagem
cv2.imshow("imagem_1", imgFinalE)
cv2.waitKey(0)
cv2.destroyAllWindows()