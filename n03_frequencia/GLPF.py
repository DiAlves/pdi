import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse 

def GLPF(img, n):
    imgAux = np.zeros((2*img.shape[0], 2*img.shape[1]))
    limFimH = int(imgAux.shape[0]/2)
    limFimW = int(imgAux.shape[1]/2)
    imgAux[0:limFimH, 0:limFimW] = img 
    imgAux /= 255
    
    p = imgAux.shape[0]
    q = imgAux.shape[1]
    
    #Transformada de fourier
    imgF = np.fft.fft2(imgAux)
    imgFShift = np.fft.fftshift(imgF)
    s = 20*np.log(np.abs(imgFShift))
    salvar = "resultados/" + "(F - Antes - GLPF)" + args["image"][7:] 
    cv2.imwrite(salvar, s)
    
    n = 220
    h = np.zeros((p, q))
    
    #Criação do filtro
    for i in range(p):
        for j in range(q):
            d = np.sqrt((i - p/2)**2 + (j - q/2)**2)
            h[i, j] = np.exp(-(d**2)/(2*(n**2)))
                
    salvar = "resultados/" + "(Filtro-GLPF)" + args["image"][7:] 
    cv2.imwrite(salvar, 255*h)
    
    #Convolução no dominio da frequência
    g = imgFShift * h
    salvar = "resultados/" + "(F - Depois - GLPF)" + args["image"][7:] 
    cv2.imwrite(salvar, 20*np.log(np.abs(g)))
    
    #Recuperação da imagem
    imgResultShift = np.fft.ifftshift(g)
    imgResult = np.fft.ifft2(imgResultShift)
    imgResult = np.abs(imgResult)
    imgResult *= 255
    
    imgResult = imgResult[0:limFimH, 0:limFimW]
    return imgResult

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a image")
ap.add_argument("-n", "--dispersao", required=True,	help="dispersao centro")
args = vars(ap.parse_args())

img = cv2.imread(args["image"], 0)
n = int(args["dispersao"])
imgResult = GLPF(img, n)

salvar = "resultados/" + "(GLPF(" + str(n) + "))" + args["image"][7:] 
cv2.imwrite(salvar, imgResult)
plt.imshow(imgResult, cmap = 'gray')