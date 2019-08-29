import cv2
import numpy as np


def filtroGaussiano(img):
    imgAux = np.zeros((img.shape[0]+6, img.shape[1]+6))
    hAux = imgAux.shape[0]-3
    wAux = imgAux.shape[1]-3
    imgAux[3:hAux, 3:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    gaussiano = (1.0/115) * np.array(
        [[2, 4, 5, 4, 2],
        [4, 9, 12, 9, 4],
        [5, 12, 15, 12, 5],
        [4, 9, 12, 9, 4],
        [2, 4, 5, 4, 2]])
    sum(sum(gaussiano))
    
    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 3):
                for l in range(-2, 3):
                    v = imgAux.item(i+k, j+l)
                    p = gaussiano[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
        

    imgFiltrada = imgFiltrada[3:hAux, 3:wAux]
    return imgFiltrada

def filtroLaplaciano(img):
    imgAux = np.zeros((img.shape[0]+4, img.shape[1]+4))
    hAux = imgAux.shape[0]-2
    wAux = imgAux.shape[1]-2
    imgAux[2:hAux, 2:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    laplaciano = np.array(
        [[-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]])
    
    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = laplaciano[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
        

    imgFiltrada = imgFiltrada[2:hAux, 2:wAux]
    return imgFiltrada


def sobel(img):
 
    imgAux = np.zeros((img.shape[0]+4, img.shape[1]+4))
    hAux = imgAux.shape[0]-2
    wAux = imgAux.shape[1]-2
    imgAux[2:hAux, 2:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    kernelV = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])
    
    kernelH = np.array([[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]])
    
    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = kernelV[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
            
    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = kernelH[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
            
    imgFiltrada = imgFiltrada[2:hAux, 2:wAux]
    return imgFiltrada

def recuperar(imgR, img):
    imgRe = np.zeros((img.shape[0], img.shape[1]))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            imgRe[i, j] = imgR.item(i, j) + img.item(i, j)
    
    return imgRe

#abrir imagem
img = cv2.imread("images/agucar_02.png", 0)

imgAux = filtroGaussiano(img)
imgAux1 = sobel(img)
imgR= recuperar(imgAux1, imgAux)

#salvar imagem
salvar = "resultados/(gau+sobel+soma)" + "agucar_02.png"
cv2.imwrite(salvar, imgR)

#plotar imagem
cv2.imshow("imagem", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()