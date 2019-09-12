import cv2
import numpy as np
from matplotlib import pyplot as plt

# Filtragem gamma
def gamma(img, g):
    imgN = img.astype('float32')
    imgN /= 255

    
    for i in range (0, imgN.shape[0]):
        for j in range (0, imgN.shape[1]):
            imgN.itemset((i, j), imgN.item(i, j) ** (1 / g)) 

    imgN *= 255
    imgN = imgN.astype('uint8')
    
    return imgN

# Função do ruido gaussiano com media 0 e variância 100, logo desvio-padrão = 10
def restaurarGau(img, dim):
    
    d = 10
    m = 0
    # Criando a distruição normal
    vetorGau = np.linspace(m-3*d, m+3*d, dim**2)
    gau = (1/(np.sqrt(2*np.pi*d)))*np.exp(-((vetorGau - m)**2)/(2*(d**2)))
    
    # Criar a mattriz
    gau = gau.reshape((dim, dim))
    
    # Filtragem
    imgAux = np.zeros((img.shape[0]+6, img.shape[1]+6))
    hAux = imgAux.shape[0]-3
    wAux = imgAux.shape[1]-3
    imgAux[3:hAux, 3:wAux] = img 
    imgFiltrada = imgAux.copy()
    
    h = imgAux.shape[0] 
    w = imgAux.shape[1]
    tamanhoFiltro = dim-3
    
    for i in range(3, h-3):
        for j in range(3, w-3):
            soma = 0
            for k in range(-3, tamanhoFiltro):
                for l in range(-3, tamanhoFiltro):
                    v = imgAux.item(i+k, j+l)
                    p = gau[2+k, 2+l]
                    soma = soma + (p * v)
            novoValor = soma
            imgFiltrada.itemset((i, j), novoValor)
        

    imgFiltrada = imgFiltrada[3:hAux, 3:wAux]
    return gamma(imgFiltrada, 1.5)


img = cv2.imread("images/image_05.png", 0) #Abrir a imgem
plt.hist(img.ravel(),256,[0,256])
plt.title('Histograma Imagem Original')
plt.show()
 
imgFiltrada = restaurarGau(img, 3)

#plotar histograma
plt.hist(imgFiltrada.ravel(),256,[0,256])
plt.title('Histograma Imagem Resultante')
plt.show()

ruido = plt.hist((img.ravel() - imgFiltrada.ravel()),256,[0,256])
plt.title('Histograma Ruido')
plt.show()

#salvar imagem
salvar = "resultados/(3)image_05.png"
cv2.imwrite(salvar, imgFiltrada)

#plotar imagem
cv2.imshow("imagem_1", imgFiltrada)
cv2.waitKey(0)
cv2.destroyAllWindows()