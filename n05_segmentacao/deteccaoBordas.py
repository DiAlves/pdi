import cv2
import numpy as np

def sobel(img):
    
    imgAux = np.zeros((img.shape[0]+4, img.shape[1]+4))
    hAux = imgAux.shape[0]-2
    wAux = imgAux.shape[1]-2
    imgAux[2:hAux, 2:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    kernelV = np.array([[0, 1, 2],
                   [-1, 0, 1],
                   [-2, -1, 0]])
    
    kernelH = np.array([[-2, -1, 0],
                       [-1, 0, 1],
                       [0, 1, 2]])
    
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
    #salvar imagem
    salvar = "resultados/(sobelDiagonais)" + "image_2.png"
    cv2.imwrite(salvar, imgFiltrada)

    return imgFiltrada

def prewitt(img):
    
    imgAux = np.zeros((img.shape[0]+4, img.shape[1]+4))
    hAux = imgAux.shape[0]-2
    wAux = imgAux.shape[1]-2
    imgAux[2:hAux, 2:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    pV = np.array([[-1, 0, 1],
                   [-1, 0, 1],
                   [-1, 0, 1]])
    
    pH = np.array([[-1, -1, -1],
                       [0, 0, 0],
                       [1, 1, 1]])
    
    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = pV[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
            
    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = pH[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
            
    imgFiltrada = imgFiltrada[2:hAux, 2:wAux]
    #salvar imagem
    salvar = "resultados/(prewitt)" + "image_2.png"
    cv2.imwrite(salvar, imgFiltrada)

    return imgFiltrada

def filtroLoG(img):
    imgAux = np.zeros((img.shape[0]+6, img.shape[1]+6))
    hAux = imgAux.shape[0]-3
    wAux = imgAux.shape[1]-3
    imgAux[3:hAux, 3:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    gaussiano = np.array(
        [[0, 0, -1, 0, 0],
        [0, -1, -2, -1, 0],
        [-1, -2, 16, -2, -1],
        [0, -1, -2, -1, 0],
        [0, 0, -1, 0, 0]])
    
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
    #salvar imagem
    salvar = "resultados/(LoG)TesteNormal" + "image_2.png"
    cv2.imwrite(salvar, imgFiltrada)
    return imgFiltrada

def laplaciano(img):
    
    imgAux = np.zeros((img.shape[0]+4, img.shape[1]+4))
    hAux = imgAux.shape[0]-2
    wAux = imgAux.shape[1]-2
    imgAux[2:hAux, 2:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    laplaciano = np.array([[1, 1, 1],
                   [1, -8, 1],
                   [1, 1, 1]])
    
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
    
    #salvar imagem
    salvar = "resultados/(l)" + "image_1.png"
    cv2.imwrite(salvar, imgFiltrada)

    return imgFiltrada

def horizontal(img, i, j):
    a = img[i, j-1]
    b = img[i, j+1]
    
    if (a > 0 and b < 0) or (a < 0 and b > 0):
        return True
    else:
        return False
    
def vertical(img, i, j):
    a = img[i-1, j]
    b = img[i+1, j]
    
    if (a > 0 and b < 0) or (a < 0 and b > 0):
        return True
    else:
        return False
    
def diagonal1(img, i, j):
    a = img[i-1, j+1]
    b = img[i+1, j-1]
    
    if (a > 0 and b < 0) or (a < 0 and b > 0):
        return True
    else:
        return False

def diagonal2(img, i, j):
    a = img[i-1, j-1]
    b = img[i+1, j+1]
    
    if (a > 0 and b < 0) or (a < 0 and b > 0):
        return True
    else:
        return False    
    
def cruzamentoPorZero(img):
    imgR = np.zeros((img.shape[0], img.shape[1]))
    for i in range (1, img.shape[0] - 1):
        for j in range (1, img.shape[1] - 1):
            listaAux = [vertical(img, i, j)]
            listaAux.append(horizontal(img, i, j))
            listaAux.append(diagonal1(img, i, j))
            listaAux.append(diagonal2(img, i, j))
            contador = 0
            
            for c in listaAux:
                if c == True:
                    contador = contador+1
            if contador >= 2:
                imgR[i][j] = img[i, j]
    #salvar imagem
    salvar = "resultados/(testeCruzamento)" + "image_1.png"
    cv2.imwrite(salvar, imgR)
                
    return imgR 

#abrir imagem
img = cv2.imread("images/image_1.png", 0)

#função
imgR = laplaciano(img)

#plotar imagem
cv2.imshow("imagem", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()