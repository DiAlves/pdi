import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse 

def BHPF(img, c, nO):
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
    salvar = "resultados/" + "(F - Antes - BHPF)" + args["image"][7:] 
    cv2.imwrite(salvar, s)
    
    d0 = c
    n = nO
    h = np.zeros((p, q))
    
    #Criação do filtro
    for i in range(p):
        for j in range(q):
            d = np.sqrt((i - p/2)**2 + (j - q/2)**2)
            h[i, j] = (1/(1 + (d0/d)**(2*n)))
                
    salvar = "resultados/" + "(Filtro-BHPF)" + args["image"][7:] 
    cv2.imwrite(salvar, 255*h)
    
    #Convolução no dominio da frequência
    g = imgFShift * h
    salvar = "resultados/" + "(F - Depois - BHPF)" + args["image"][7:] 
    cv2.imwrite(salvar, 20*np.log(np.abs(g)))
    
    #Recuperação da imagem
    imgResultShift = np.fft.ifftshift(g)
    imgResult = np.fft.ifft2(imgResultShift)
    imgResult = np.abs(imgResult)
    imgResult *= 255
    
    imgResult = imgResult[0:limFimH, 0:limFimW]
    imgResultF = imgResult.copy()
    
    for i in range(imgResult.shape[0]):
        for j in range(imgResult.shape[1]):
           imgResultF[i, j] = img[i, j] + imgResult[i, j]
           
    return imgResultF

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="caminho para a image")
ap.add_argument("-c", "--corte", required=True,	help="valor do frequência de corte")
ap.add_argument("-n", "--ordem", required=True,	help="ordem do filtro")
args = vars(ap.parse_args())

img = cv2.imread(args["image"], 0)
c = int(args["corte"])
nO = int(args["ordem"])
imgResult = BHPF(img, c, nO)

salvar = "resultados/" + "(BHPF(" + str(c) + "-" + str(nO) + "))" + args["image"][7:] 
cv2.imwrite(salvar, imgResult)
plt.imshow(imgResult, cmap = 'gray')