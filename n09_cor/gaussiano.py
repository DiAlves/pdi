import cv2
import numpy as np

def componenteH(img):
    h = np.zeros((img.shape[0], img.shape[1]))
    r = img[:,:,2]
    g = img[:,:,1]
    b = img[:,:,0]
    
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            o = (0.5*((r[i, j] - g[i, j]) + (r[i, j] - b[i, j])))/np.sqrt(((r[i, j]-g[i,j])**2) +(r[i,j] - b[i,j])*(g[i, j] - b[i,j]))
            o = np.arccos(o)
            if b[i, j] <= g[i, j]:
                h[i, j] = o
            else:
                h[i, j] = 2*np.pi - o
    h =(h / np.pi)
    h *= 180
    return h

def componenteS(img):
    s = np.zeros((img.shape[0], img.shape[1]))
    r = img[:,:,2]
    g = img[:,:,1]
    b = img[:,:,0]
    
    minimo = np.minimum(np.minimum(r, g), b)
    s = 1 - (3 / (r + g + b) * minimo)
    
    s *= 100
    return s

def componenteI(img):
    i = np.zeros((img.shape[0], img.shape[1]))
    r = img[:,:,2]
    g = img[:,:,1]
    b = img[:,:,0]
    
    i = (1./3)*(r+g+b)
    
    i *= 255.
    return i

def filtroGaussiano(img):
    imgAux = np.zeros((img.shape[0]+6, img.shape[1]+6))
    hAux = imgAux.shape[0]-3
    wAux = imgAux.shape[1]-3
    imgAux[3:hAux, 3:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    
    gaussiano = (1.0/57) * np.array(
        [[0, 1, 2, 1, 0],
        [1, 3, 5, 3, 1],
        [2, 5, 9, 5, 2],
        [1, 3, 5, 3, 1],
        [0, 1, 2, 1, 0]])
    
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
    imgFiltrada = imgFiltrada.astype('float64')
    return imgFiltrada

def passagemFiltro(img, n):
    imgAux = img
    for i in range(n):
        imgAux = filtroGaussiano(imgAux)
        
    return imgAux
     
def hsoToRGB(imgHSI, imgRGB):
    r = imgRGB[:,:,2]
    g = imgRGB[:,:,1]
    b = imgRGB[:,:,0]
    
    h = imgHSI[:,:,0]*np.pi/180
    s = imgHSI[:,:,1]/100
    i = imgHSI[:,:,2]/255
    
    
    for l in range(img.shape[0]):
        for c in range(img.shape[1]):
            if h[l, c] < 2*np.pi/3:
                x = i[l,c]*(1-s[l, c])
                y = i[l, c]*(1 + (s[l, c]*np.cos(h[l, c]))/np.cos((np.pi/3) - h[l, c])) 
                z = 3*i[l, c] - (x + y)
                b[l, c] = x
                r[l, c] = y
                g[l, c] = z
                
            elif h[l, c] >= 2*np.pi/3 and h[l, c] < 4*np.pi/3:
                h[l, c] = h[l, c] - 2*np.pi/3
                x = i[l,c]*(1-s[l, c])
                y = i[l, c]*(1 + (s[l, c]*np.cos(h[l, c]))/np.cos((np.pi/3) - h[l, c])) 
                z = 3*i[l, c] - (x + y)
                r[l, c] = x
                g[l, c] = y
                b[l, c] = z
                
            elif h[l, c] >= 4*np.pi/3 and h[l, c] <= 2*np.pi:
                h[l, c] = h[l, c] - 4*np.pi/3
                x = i[l,c]*(1-s[l, c])
                y = i[l, c]*(1 + (s[l, c]*np.cos(h[l, c]))/np.cos((np.pi/3) - h[l, c])) 
                z = 3*i[l, c] - (x + y)
                g[l, c] = x
                b[l, c] = y
                r[l, c] = z
    
    r *= 255
    g *= 255
    b *= 255    
    imgFinal = cv2.merge((b, g, r))
    return imgFinal
                 
img = cv2.imread("images/image_2a.png") #Abrir a imgem 
imgAux = img.copy()
img = img/255
'''
imgH = componenteH(img)
salvar = "resultados/(H)image_2a.png"
cv2.imwrite(salvar, imgH)

imgS = componenteS(img)
salvar = "resultados/(S)image_2a.png"
cv2.imwrite(salvar, imgS)

imgI = componenteI(img)
salvar = "resultados/(I)image_2a.png"
cv2.imwrite(salvar, imgI)

hsi = cv2.merge((imgH, imgS, imgI))
salvar = "resultados/(hsi-antes)image_2a.jpg"
cv2.imwrite(salvar, hsi)

imgH = passagemFiltro(imgH, 1)
salvar = "resultados/(FiltradaH)image_2a.png"
cv2.imwrite(salvar, imgH)

imgS = passagemFiltro(imgS, 1)
salvar = "resultados/(FiltradaS)image_2a.png"
cv2.imwrite(salvar, imgS)

imgI = passagemFiltro(imgI, 1)
salvar = "resultados/(FiltradaI)image_2a.png"
cv2.imwrite(salvar, imgI)

hsi = cv2.merge((imgH, imgS, imgI))
salvar = "resultados/(filtrada3Componentes-HSI)image_2a.jpg"
cv2.imwrite(salvar, hsi)


imgRGB = hsoToRGB(hsi, img)
salvar = "resultados/(filtrada3Componentes-RGB)image_2a.png"
cv2.imwrite(salvar, imgRGB)'''


#Tirando o ruido sem fazer a transformação para hsi
imgR = imgAux[:,:,0]
salvar = "resultados/(R)image_2a.png"
cv2.imwrite(salvar, imgR)

imgG = imgAux[:,:,1]
salvar = "resultados/(G)image_2a.png"
cv2.imwrite(salvar, imgG)

imgB = imgAux[:,:,2]
salvar = "resultados/(B)image_2a.png"
cv2.imwrite(salvar, imgB)

imgR = passagemFiltro(imgR, 1)
salvar = "resultados/(RF)image_2a.png"
cv2.imwrite(salvar, imgR)

imgG = passagemFiltro(imgG, 1)
salvar = "resultados/(GF)image_2a.png"
cv2.imwrite(salvar, imgG)

imgB = passagemFiltro(imgB, 1)
salvar = "resultados/(BF)image_2a.png"
cv2.imwrite(salvar, imgB)


imgRGBF = cv2.merge((imgR, imgG, imgB))
salvar = "resultados/(filtradaRGBsemTransformacao)image_2a.png"
cv2.imwrite(salvar, imgRGBF)