import cv2
import numpy as np

def firstPoint(img):
    for i in range (img.shape[0]):
        for j in range (img.shape[1]):
            if img[i, j] == 255:
                return (i, j)

def findC(img, b):
    coordList = [(b[0]-1, b[1]), (b[0], b[1]+1), 
                 (b[0]+1, b[1]), (b[0], b[1]-1)]
    for coord in coordList:
        if img[coord[0], coord[1]] == 0:
            return coord
 
def findB(img, b, c):
    caminho = {(b[0]-1,b[1]-1):(b[0]-1,b[1]),
               (b[0]-1,b[1]):(b[0]-1,b[1]+1),
               (b[0]-1,b[1]+1):(b[0],b[1]+1),
               (b[0],b[1]+1):(b[0]+1,b[1]+1),
               (b[0]+1,b[1]+1):(b[0]+1,b[1]),
               (b[0]+1,b[1]):(b[0]+1,b[1]-1),
               (b[0]+1,b[1]-1):(b[0],b[1]-1),
               (b[0],b[1]-1):(b[0]-1,b[1]-1)}
    
    coordAtual = c
    for temp in range(8):
        coord = caminho[coordAtual]
        if img[coord[0], coord[1]] == 255:
            return coord
        coordAtual = coord
                               
def seguidorContorno(img):
    imgR = np.zeros((img.shape[0], img.shape[1]), 'uint8')
    
    partida = firstPoint(img)
    c0 = (partida[0], partida[1] -1)
    
    b = partida
    c = c0
    
    coordList = []
    
    while(True):
        coordList.append(b)
        imgR[b[0], b[1]] = 255
        b = findB(img, b, c)
        c = findC(img, b)
        
        if b in coordList:
            break
    
    return imgR, coordList

def grid(img, e):
    grid = np.zeros((img.shape[0], img.shape[1]), 'uint8')
    coordListGrid = []
    
    for i in range(0, img.shape[0], e):
        for j in range(0, img.shape[1], e):
            coordListGrid.append((i, j))
            grid[i, j] = 255

    salvar = "resultados/(gridG10)" + "image_1.png"
    cv2.imwrite(salvar, grid)
    return grid, coordListGrid

def distanciaPonto(i, j):
    return ((i[0] - j[0])**2 + (i[1] - j[1])**2)**0.5

def reamostragem(img, g):
    gridA, coordGrid = grid(img, g)
    print(len(coordGrid))
    amostragemList = []
    imgR = np.zeros((img.shape[0], img.shape[1]), 'uint8')
    
    #plotar imagem
    cv2.imshow("imagem", gridA)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            amostragemList.append(img[i ,j])
            if (i, j) in coordGrid:
                if 255 in amostragemList:
                    imgR[i ,j] = 255
                amostragemList = []
    
    for j in range(img.shape[1]):
        for i in range(img.shape[0]):
            amostragemList.append(img[i ,j])
            if (i, j) in coordGrid:
                if 255 in amostragemList:
                    imgR[i ,j] = 255
                amostragemList = []
                
    imgAux = imgR[1:868, 1:1077]    
    imgR= np.zeros((imgR.shape[0], imgR.shape[1]))
    imgR[1:868, 1:1077] = imgAux
    
    ll = 0
    for i in range(imgR.shape[0]):
        for j in range(imgR.shape[1]):
            if imgR[i ,j] == 255:
                ll = ll + 1
                
    print("Ponto Brnacps {}".format(ll))
    coordListA = seguidorContornoA(imgR, g)
    return imgR, coordListA


def findCA(img, b, g):
    coordList = [(b[0]-g, b[1]), (b[0], b[1]+g), 
                 (b[0]+g, b[1]), (b[0], b[1]-g)]
    for coord in coordList:
        if img[coord[0], coord[1]] == 0:
            return coord

def findBA(img, b, c, g):
    caminho = {(b[0]-g,b[1]-g):(b[0]-g,b[1]),
               (b[0]-g,b[1]):(b[0]-g,b[1]+g),
               (b[0]-g,b[1]+g):(b[0],b[1]+g),
               (b[0],b[1]+g):(b[0]+g,b[1]+g),
               (b[0]+g,b[1]+g):(b[0]+g,b[1]),
               (b[0]+g,b[1]):(b[0]+g,b[1]-g),
               (b[0]+g,b[1]-g):(b[0],b[1]-g),
               (b[0],b[1]-g):(b[0]-g,b[1]-g)}
    
    
    coordAtual = c
    for temp in range(8):
        coord = caminho[coordAtual]
        if img[coord[0], coord[1]] == 255:
            return coord, coordAtual
        coordAtual = coord
        
def seguidorContornoA(img, g):
    
    partida = firstPoint(img)
    c0 = (partida[0], partida[1] - g)
    
    b = partida
    c = c0
    
    coordListA = []
    
    while(True):
        coordListA.append(b)
        b, c = findBA(img, b, c, g)
        
        if b in coordListA:
            break
    
    return coordListA

def codCadeia4(coordListA, g):
    partida = (coordListA[0][0], coordListA[0][1])
    u = (coordListA[0][0], coordListA[0][1])
    codCadeia = []
    
    for i in range(1, len(coordListA)):
        if ((partida[0]+g, partida[1]+g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(0)
            partida = (partida[0]+g, partida[1]+g)
            
        elif ((partida[0], partida[1]+g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(0)
            partida = (partida[0], partida[1]+g)
            
        elif ((partida[0]-g, partida[1]+g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(1)
            partida = (partida[0]-g, partida[1]+g)
            
        elif ((partida[0]-g, partida[1]) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(1)
            partida = (partida[0]-g, partida[1])
            
        elif ((partida[0]-g, partida[1]-g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(2)
            partida = (partida[0]-g, partida[1]-g)
        
        elif ((partida[0], partida[1]-g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(2)
            partida = (partida[0], partida[1]-g)
            
        elif ((partida[0]+g, partida[1]-g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(3)
            partida = (partida[0]+g, partida[1]-g)
            
        elif ((partida[0]+g, partida[1]) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(3)
            partida = (partida[0]+g, partida[1])
        
    if ((partida[0]+g, partida[1]+g) == (u[0], u[1])):
            codCadeia.append(0)
            
    elif ((partida[0], partida[1]+g) == (u[0], u[1])):
        codCadeia.append(0)
        
    elif ((partida[0]-g, partida[1]+g) == (u[0], u[1])):
        codCadeia.append(1)
    
        
    elif ((partida[0]-g, partida[1]) == (u[0], u[1])):
        codCadeia.append(1)
        
    elif ((partida[0]-g, partida[1]-g) == (u[0], u[1])):
        codCadeia.append(2)
    
    elif ((partida[0], partida[1]-g) == (u[0], u[1])):
        codCadeia.append(2)
        
    elif ((partida[0]+g, partida[1]-g) == (u[0], u[1])):
        codCadeia.append(3)
        
    elif ((partida[0]+g, partida[1]) == (u[0], u[1])):
        codCadeia.append(3)
        
    return codCadeia

def codCadeia8(coordListA, g):
    partida = (coordListA[0][0], coordListA[0][1])
    u = (coordListA[0][0], coordListA[0][1])
    codCadeia = []
    
    for i in range(1, len(coordListA)):
        if ((partida[0]+g, partida[1]+g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(7)
            partida = (partida[0]+g, partida[1]+g)
            
        elif ((partida[0], partida[1]+g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(0)
            partida = (partida[0], partida[1]+g)
            
        elif ((partida[0]-g, partida[1]+g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(1)
            partida = (partida[0]-g, partida[1]+g)
            
        elif ((partida[0]-g, partida[1]) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(2)
            partida = (partida[0]-g, partida[1])
            
        elif ((partida[0]-g, partida[1]-g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(3)
            partida = (partida[0]-g, partida[1]-g)
        
        elif ((partida[0], partida[1]-g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(4)
            partida = (partida[0], partida[1]-g)
            
        elif ((partida[0]+g, partida[1]-g) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(5)
            partida = (partida[0]+g, partida[1]-g)
            
        elif ((partida[0]+g, partida[1]) == (coordListA[i][0], coordListA[i][1])):
            codCadeia.append(6)
            partida = (partida[0]+g, partida[1])
        
    if ((partida[0]+g, partida[1]+g) == (u[0], u[1])):
            codCadeia.append(7)
            
    elif ((partida[0], partida[1]+g) == (u[0], u[1])):
        codCadeia.append(0)
        
    elif ((partida[0]-g, partida[1]+g) == (u[0], u[1])):
        codCadeia.append(1)
    
        
    elif ((partida[0]-g, partida[1]) == (u[0], u[1])):
        codCadeia.append(2)
        
    elif ((partida[0]-g, partida[1]-g) == (u[0], u[1])):
        codCadeia.append(3)
    
    elif ((partida[0], partida[1]-g) == (u[0], u[1])):
        codCadeia.append(4)
        
    elif ((partida[0]+g, partida[1]-g) == (u[0], u[1])):
        codCadeia.append(5)
        
    elif ((partida[0]+g, partida[1]) == (u[0], u[1])):
        codCadeia.append(6)
        
    return codCadeia
           
def primeiraDif4(codCadeia):
    newCod = []
    a = codCadeia[0]
    inicio = codCadeia[0]
    for i in range (1, len(codCadeia)):
        if a == 0:
            if codCadeia[i] == 0:
                newCod.append(0)
            elif codCadeia[i] == 1:
                newCod.append(1)
            elif codCadeia[i] == 2:
                newCod.append(2)
            elif codCadeia[i] == 3:
                newCod.append(3)

        elif a == 1:
            if codCadeia[i] == 0:
                newCod.append(3)
            elif codCadeia[i] == 1:
                newCod.append(0)
            elif codCadeia[i] == 2:
                newCod.append(1)
            elif codCadeia[i] == 3:
                newCod.append(2)

        elif a == 2:
            if codCadeia[i] == 0:
                newCod.append(2)
            elif codCadeia[i] == 1:
                newCod.append(3)
            elif codCadeia[i] == 2:
                newCod.append(0)
            elif codCadeia[i] == 3:
                newCod.append(1)

        elif a == 3:
            if codCadeia[i] == 0:
                newCod.append(1)
            elif codCadeia[i] == 1:
                newCod.append(2)
            elif codCadeia[i] == 2:
                newCod.append(3)
            elif codCadeia[i] == 3:
                newCod.append(0)
        
        a = codCadeia[i]
    
    if a == 0:
        if inicio == 0:
            newCod.append(0)
        elif inicio == 1:
            newCod.append(1)
        elif inicio == 2:
            newCod.append(2)
        elif inicio == 3:
            newCod.append(3)

    elif a == 1:
        if inicio == 0:
            newCod.append(3)
        elif inicio == 1:
            newCod.append(0)
        elif inicio == 2:
            newCod.append(1)
        elif inicio == 3:
            newCod.append(2)

    elif a == 2:
        if inicio == 0:
            newCod.append(2)
        elif inicio == 1:
            newCod.append(3)
        elif inicio == 2:
            newCod.append(0)
        elif inicio == 3:
            newCod.append(1)

    elif a == 3:
        if inicio == 0:
            newCod.append(1)
        elif inicio == 1:
            newCod.append(2)
        elif inicio == 2:
            newCod.append(3)
        elif inicio == 3:
            newCod.append(0)
    
    return newCod

def primeiraDif8(codCadeia):
    newCod = []
    a = codCadeia[0]
    inicio = codCadeia[0]
    for i in range (1, len(codCadeia)):
        if a == 0:
            if codCadeia[i] == 0:
                newCod.append(0)
            elif codCadeia[i] == 1:
                newCod.append(1)
            elif codCadeia[i] == 2:
                newCod.append(2)
            elif codCadeia[i] == 3:
                newCod.append(3)
            elif codCadeia[i] == 4:
                newCod.append(4)
            elif codCadeia[i] == 5:
                newCod.append(5)
            elif codCadeia[i] == 6:
                newCod.append(6)
            elif codCadeia[i] == 7:
                newCod.append(7)


        elif a == 1:
            if codCadeia[i] == 0:
                newCod.append(7)
            elif codCadeia[i] == 1:
                newCod.append(0)
            elif codCadeia[i] == 2:
                newCod.append(1)
            elif codCadeia[i] == 3:
                newCod.append(2)
            elif codCadeia[i] == 4:
                newCod.append(3)
            elif codCadeia[i] == 5:
                newCod.append(4)
            elif codCadeia[i] == 6:
                newCod.append(5)
            elif codCadeia[i] == 7:
                newCod.append(6)

        elif a == 2:
            if codCadeia[i] == 0:
                newCod.append(6)
            elif codCadeia[i] == 1:
                newCod.append(7)
            elif codCadeia[i] == 2:
                newCod.append(0)
            elif codCadeia[i] == 3:
                newCod.append(1)
            elif codCadeia[i] == 4:
                newCod.append(2)
            elif codCadeia[i] == 5:
                newCod.append(3)
            elif codCadeia[i] == 6:
                newCod.append(4)
            elif codCadeia[i] == 7:
                newCod.append(5)

        elif a == 3:
            if codCadeia[i] == 0:
                newCod.append(5)
            elif codCadeia[i] == 1:
                newCod.append(6)
            elif codCadeia[i] == 2:
                newCod.append(7)
            elif codCadeia[i] == 3:
                newCod.append(0)
            elif codCadeia[i] == 4:
                newCod.append(1)
            elif codCadeia[i] == 5:
                newCod.append(2)
            elif codCadeia[i] == 6:
                newCod.append(3)
            elif codCadeia[i] == 7:
                newCod.append(4)
                
        elif a == 4:
            if codCadeia[i] == 0:
                newCod.append(4)
            elif codCadeia[i] == 1:
                newCod.append(5)
            elif codCadeia[i] == 2:
                newCod.append(6)
            elif codCadeia[i] == 3:
                newCod.append(7)
            elif codCadeia[i] == 4:
                newCod.append(0)
            elif codCadeia[i] == 5:
                newCod.append(1)
            elif codCadeia[i] == 6:
                newCod.append(2)
            elif codCadeia[i] == 7:
                newCod.append(3)

        elif a == 5:
            if codCadeia[i] == 0:
                newCod.append(3)
            elif codCadeia[i] == 1:
                newCod.append(4)
            elif codCadeia[i] == 2:
                newCod.append(5)
            elif codCadeia[i] == 3:
                newCod.append(6)
            elif codCadeia[i] == 4:
                newCod.append(7)
            elif codCadeia[i] == 5:
                newCod.append(0)
            elif codCadeia[i] == 6:
                newCod.append(1)
            elif codCadeia[i] == 7:
                newCod.append(2) 

        elif a == 6:
            if codCadeia[i] == 0:
                newCod.append(2)
            elif codCadeia[i] == 1:
                newCod.append(3)
            elif codCadeia[i] == 2:
                newCod.append(4)
            elif codCadeia[i] == 3:
                newCod.append(5)
            elif codCadeia[i] == 4:
                newCod.append(6)
            elif codCadeia[i] == 5:
                newCod.append(7)
            elif codCadeia[i] == 6:
                newCod.append(0)
            elif codCadeia[i] == 7:
                newCod.append(1)
                
        elif a == 7:
            if codCadeia[i] == 0:
                newCod.append(1)
            elif codCadeia[i] == 1:
                newCod.append(2)
            elif codCadeia[i] == 2:
                newCod.append(3)
            elif codCadeia[i] == 3:
                newCod.append(4)
            elif codCadeia[i] == 4:
                newCod.append(5)
            elif codCadeia[i] == 5:
                newCod.append(6)
            elif codCadeia[i] == 6:
                newCod.append(7)
            elif codCadeia[i] == 7:
                newCod.append(0)

        a = codCadeia[i]
    
    if a == 0:
        if inicio == 0:
            newCod.append(0)
        elif inicio == 1:
            newCod.append(1)
        elif inicio == 2:
            newCod.append(2)
        elif inicio == 3:
            newCod.append(3)
        elif inicio == 4:
            newCod.append(4)
        elif inicio == 5:
            newCod.append(5)
        elif inicio == 6:
            newCod.append(6)
        elif inicio == 7:
            newCod.append(7)


    elif a == 1:
        if inicio == 0:
            newCod.append(7)
        elif inicio == 1:
            newCod.append(0)
        elif inicio == 2:
            newCod.append(1)
        elif inicio == 3:
            newCod.append(2)
        elif inicio == 4:
            newCod.append(3)
        elif inicio == 5:
            newCod.append(4)
        elif inicio == 6:
            newCod.append(5)
        elif inicio == 7:
            newCod.append(6)

    elif a == 2:
        if inicio == 0:
            newCod.append(6)
        elif inicio == 1:
            newCod.append(7)
        elif inicio == 2:
            newCod.append(0)
        elif inicio == 3:
            newCod.append(1)
        elif inicio == 4:
            newCod.append(2)
        elif inicio == 5:
            newCod.append(3)
        elif inicio == 6:
            newCod.append(4)
        elif inicio == 7:
            newCod.append(5)

    elif a == 3:
        if inicio == 0:
            newCod.append(5)
        elif inicio == 1:
            newCod.append(6)
        elif inicio == 2:
            newCod.append(7)
        elif inicio == 3:
            newCod.append(0)
        elif inicio == 4:
            newCod.append(1)
        elif inicio == 5:
            newCod.append(2)
        elif inicio == 6:
            newCod.append(3)
        elif inicio == 7:
            newCod.append(4)
            
    elif a == 4:
        if inicio == 0:
            newCod.append(4)
        elif inicio == 1:
            newCod.append(5)
        elif inicio == 2:
            newCod.append(6)
        elif inicio == 3:
            newCod.append(7)
        elif inicio == 4:
            newCod.append(0)
        elif inicio == 5:
            newCod.append(1)
        elif inicio == 6:
            newCod.append(2)
        elif inicio == 7:
            newCod.append(3)

    elif a == 5:
        if inicio == 0:
            newCod.append(3)
        elif inicio == 1:
            newCod.append(4)
        elif inicio == 2:
            newCod.append(5)
        elif inicio == 3:
            newCod.append(6)
        elif inicio == 4:
            newCod.append(7)
        elif inicio == 5:
            newCod.append(0)
        elif inicio == 6:
            newCod.append(1)
        elif inicio == 7:
            newCod.append(2) 

    elif a == 6:
        if inicio == 0:
            newCod.append(2)
        elif inicio == 1:
            newCod.append(3)
        elif inicio == 2:
            newCod.append(4)
        elif inicio == 3:
            newCod.append(5)
        elif inicio == 4:
            newCod.append(6)
        elif inicio == 5:
            newCod.append(7)
        elif inicio == 6:
            newCod.append(0)
        elif inicio == 7:
            newCod.append(1)
            
    elif a == 7:
        if inicio == 0:
            newCod.append(1)
        elif inicio == 1:
            newCod.append(2)
        elif inicio == 2:
            newCod.append(3)
        elif inicio == 3:
            newCod.append(4)
        elif inicio == 4:
            newCod.append(5)
        elif inicio == 5:
            newCod.append(6)
        elif inicio == 6:
            newCod.append(7)
        elif inicio == 7:
            newCod.append(0)
    
    return newCod             
                
                
    
    
def or1(img1, img2):
    imgR = np.zeros((img1.shape[0], img1.shape[1]))
    for i in range (imgR.shape[0]):
        for j in range (imgR.shape[1]):
            if (img1[i, j] == 255 or img2[i, j] == 255):
                imgR[i, j] = 255
   
    return imgR
 
#abrir imagem
img = cv2.imread("images/image_1.png", 0)

imgR, coordList = seguidorContorno(img)
salvar = "resultados/(contorno)" + "image_1.png"
cv2.imwrite(salvar, imgR)

#imgTesteGrid, cGrid = grid(imgR, 15)

imgAmostrada, coordListA = reamostragem(imgR, 10)
p = (coordListA[0][0], coordListA[0][1])
salvar = "resultados/(amostradaG10)" + "image_1.png"
cv2.imwrite(salvar, imgAmostrada)
partida = firstPoint(imgAmostrada)
print("CoordanadasAmostrada = {}".format(len(coordListA)))

gridA, coordGrid = grid(imgR, 10)
imgOr = or1(gridA, imgR)
salvar = "resultados/(OrG10)" + "image_1.png"
cv2.imwrite(salvar, imgOr)

#plotar imagem
cv2.imshow("imagem", imgAmostrada)
cv2.waitKey(0)
cv2.destroyAllWindows()

#imgPontos = aux(imgAmostrada, coordListA)
codCadeia1 = codCadeia4(coordListA, 10)
codCadeia2 = codCadeia8(coordListA, 10)
print(codCadeia1)
print(codCadeia2)

normalizado4 = primeiraDif4(codCadeia1)
normalizado8 = primeiraDif8(codCadeia2)

print(normalizado4)
print(normalizado8)




