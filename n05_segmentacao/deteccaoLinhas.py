import cv2
import numpy as np

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
    salvar = "resultados/(laplaciano)" + "image_3.png"
    cv2.imwrite(salvar, imgFiltrada)

    return imgFiltrada

def direcoes(img):
    
    imgAux = np.zeros((img.shape[0]+4, img.shape[1]+4))
    hAux = imgAux.shape[0]-2
    wAux = imgAux.shape[1]-2
    imgAux[2:hAux, 2:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    horizontais = np.array([[-1, -1, -1],
                            [2, 2, 2],
                            [-1, -1, -1]])
    
    p45 = np.array([[-1, -1, 2],
                    [-1, 2, -1],
                    [2, -1, -1]])
    
    n45 = np.array([[2, -1, -1],
                    [-1, 2, -1],
                    [-1, -1, 2]])
    
    verticais = np.array([[-1, 2, -1],
                            [-1, 2, -1],
                            [-1, 2, -1]])
    
    '''for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = horizontais[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)'''
    
    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = p45[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)

    for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = n45[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
            
    '''for i in range(2, h-2):
        for j in range(2, w-2):
            soma = 0
            for k in range(-2, 1):
                for l in range(-2, 1):
                    v = imgAux.item(i+k, j+l)
                    p = verticais[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
           
    imgFiltrada = imgFiltrada[2:hAux, 2:wAux]'''
    
    #salvar imagem
    salvar = "resultados/(Diagonais)" + "image_3.png"
    cv2.imwrite(salvar, imgFiltrada)

    return imgFiltrada

#abrir imagem
img = cv2.imread("images/image_3.png", 0)

#função
imgR = direcoes(img)

#plotar imagem
cv2.imshow("imagem", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()
