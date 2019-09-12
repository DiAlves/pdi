import cv2
import numpy as np
from matplotlib import pyplot as plt

# Função do ruido gaussiano com media 15 e desvio-padrão 10
def ruidoGau(img):
    for k in range(img.shape[2]):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                    img[i, j, k] += np.random.normal(loc=15, scale=10)
    
    return img

# Função do ruido gaussiano com media 15 e desvio-padrão 10
def ruidoGau2(img):
    
      row,col,ch = img.shape
      m = 15
      d = 10
      gauss = np.random.normal(m, d,(row,col,ch))
      gauss = gauss.reshape(row,col,ch)
      ruido = img + gauss
      
      return ruido

img = cv2.imread("images/image_03.png") #Abrir a imgem 
#Histrograma Imagem Original
plt.hist(img.ravel(),256,[0,256])
plt.title('Histograma Imagem Original')
plt.show()

imgRuidosa = ruidoGau2(img)

#plotar histograma imagem ruidosa
plt.hist(imgRuidosa.ravel(),256,[0,256])
plt.title('Histograma Imagem Ruidosa')
plt.show()

#salvar imagem
salvar = "resultados/(M2)image_03.png"
cv2.imwrite(salvar, imgRuidosa)

#plotar imagem
cv2.imshow("imagem_1", imgRuidosa)
cv2.waitKey(0)
cv2.destroyAllWindows()