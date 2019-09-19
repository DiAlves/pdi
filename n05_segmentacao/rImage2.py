import cv2
import numpy as np

def gaussiana(dim, desvio):
    
    gaussian = np.zeros((dim, dim))
    
    for i in range(dim):
        for j in range(dim):
            gaussian[i, j] = np.exp(-((i**2 + j**2)/(2*desvio**2)))
    
    gaussian /= np.sum(gaussian)
            
    return gaussian

def filtroGaussiano(img):
    imgAux = np.zeros((img.shape[0]+12, img.shape[1]+12))
    hAux = imgAux.shape[0]-6
    wAux = imgAux.shape[1]-6
    imgAux[6:hAux, 6:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    gaussiano = gaussiana(7, 1)
    
    
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
    
    imgFiltrada = imgFiltrada[6:hAux, 6:wAux]
    return imgFiltrada

def linhasV(img):
    
    imgAux = np.zeros((img.shape[0]+4, img.shape[1]+4))
    hAux = imgAux.shape[0]-2
    wAux = imgAux.shape[1]-2
    imgAux[2:hAux, 2:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    
    verticais = np.array([[-1, 2, -1],
                            [-1, 2, -1],
                            [-1, 2, -1]])
    
    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = verticais[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
           
    imgFiltrada = imgFiltrada[2:hAux, 2:wAux]
    
    #salvar imagem
    salvar = "resultados/(linhasVerticais)" + "image_2.png"
    cv2.imwrite(salvar, imgFiltrada)

    return imgFiltrada

def lim1(img):
    t = 85
    
    for i in range (img.shape[0]):
        for j in range (img.shape[1]):
            if img[i,j] < t:
                img[i, j] = 0
                
    salvar = "resultados/(limiarizacacao85)" + "image_2.png"
    cv2.imwrite(salvar, img)
    return img

def lim2(img):
    maxV = np.amax(np.abs(img)) 
    t = 0.12*maxV
    for i in range (img.shape[0]):
        for j in range (img.shape[1]):
            if img[i,j] < t:
                img[i, j] = 0
            else:
                img[i, j] = 255
                
    #salvar imagem
    salvar = "resultados/(limiarizacao2(12%))" + "image_2.png"
    cv2.imwrite(salvar, img)
    return img

def laplaciano(img):
    
    imgAux = np.zeros((img.shape[0]+4, img.shape[1]+4))
    hAux = imgAux.shape[0]-2
    wAux = imgAux.shape[1]-2
    imgAux[2:hAux, 2:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    laplaciano = np.array([[-1, -1, -1],
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
    
    #salvar imagem
    salvar = "resultados/(laplaciano)" + "image_2.png"
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
    salvar = "resultados/(cruzamentoPorZero)" + "image_2.png"
    cv2.imwrite(salvar, imgR)
                
    return imgR 
      
def filtroMediana(img, filtro):
    imgAux = np.zeros((img.shape[0]+6, img.shape[1]+6))
    hAux = imgAux.shape[0]-3
    wAux = imgAux.shape[1]-3
    imgAux[3:hAux, 3:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    tamanhoFiltro = filtro-3


    for i in range(3, h-3):
        for j in range(3, w-3):
            vizinhos = []
            for k in range(-3, tamanhoFiltro):
                for l in range(-3, tamanhoFiltro):
                    v = imgAux.item(i+k, j+l)
                    vizinhos.append(v)
            vizinhos.sort()
            mediana = vizinhos[int(((filtro*filtro)-1)/2)]
            imgFiltrada.itemset((i, j), mediana)

    imgFiltrada = imgFiltrada[3:hAux, 3:wAux]
    return imgFiltrada

def soma(img1, img2):
    imgR = np.zeros((img1.shape[0], img1.shape[1]))
    for i in range (img1.shape[0]):
        for j in range (img.shape[1]):
            imgR[i, j] = img1[i, j] + img2[i, j]
    #salvar imagem
    salvar = "resultados/(gaus+lim+lapla+cru+linhasV)" + "image_2.png"
    cv2.imwrite(salvar, imgR)
    return imgR
        
img = cv2.imread("images/image_2.png",0)
imgR = lim2(cruzamentoPorZero(laplaciano(filtroMediana(lim1(filtroGaussiano(img)), 3))))
imgRV = linhasV(filtroMediana(lim1(filtroGaussiano(img)), 3))

imgR = soma(imgR, imgRV)

#plotar imagem
cv2.imshow("imagem", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()