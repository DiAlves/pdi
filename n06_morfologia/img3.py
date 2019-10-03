import cv2
import numpy as np

def erosao(img, t):
    es = np.ones((t, t))
    imgAux = np.zeros((t, t))
    imgPadding = np.zeros((img.shape[0]+(t-1), img.shape[1]+(t-1)))
    hAux = imgPadding.shape[0] - int((t - 1)/2)
    wAux = imgPadding.shape[1] - int((t - 1)/2)
    imgPadding[int((t - 1)/2):hAux, int((t - 1)/2):wAux] = img
    imgR = imgPadding.copy()

    for i in range (imgPadding.shape[0]):
        for j in range (imgPadding.shape[1]):
            imgAux = imgPadding[i:(i+t), j:(j+t)]
            
            if imgAux.shape == (t, t):
                r = sum(sum(imgAux + es))
                #print (r)
                if (r == (t*t)) or (r == (2*(t*t))):
                    imgR[i+1, j+1] = imgPadding.item(i+1, j+1)
                else:
                    imgR[i+1, j+1] = 0
            else:
                continue
            
    imgR = imgR[int((t - 1)/2):hAux, int((t - 1)/2):wAux]
    return imgR

def dilatacao(img, t):
    es = np.ones((t, t))
    imgAux = np.zeros((t, t))
    imgPadding = np.zeros((img.shape[0]+(t-1), img.shape[1]+(t-1)))
    hAux = imgPadding.shape[0] - int((t - 1)/2)
    wAux = imgPadding.shape[1] - int((t - 1)/2)
    imgPadding[int((t - 1)/2):hAux, int((t - 1)/2):wAux] = img
    imgR = imgPadding.copy()

    for i in range (imgPadding.shape[0]):
        for j in range (imgPadding.shape[1]):
            imgAux = imgPadding[i:(i+t), j:(j+t)]
            
            if imgAux.shape == (t, t):
                r = sum(sum(imgAux + es))
                #print (r)
                if (r > (t*t)):
                    imgR[i+1, j+1] = 1
                else:
                    imgR[i+1, j+1] = imgPadding.item(i+1, j+1)
            else:
                continue
            
    imgR = imgR[int((t - 1)/2):hAux, int((t - 1)/2):wAux]
    return imgR


#abrir imagem
img = cv2.imread("images/image_3.png", 0)

img = img.astype('float32')
img /= 255

#dilatacao1
imgR = dilatacao(img, 3)
imgR *= 255
imgR = imgR.astype('uint8')
salvar = "resultados/dilatacao1" + "image_3.png"
cv2.imwrite(salvar, imgR)

imgR = imgR.astype('float32')
imgR /= 255

#erosao1
imgR = erosao(imgR, 3)
imgR *= 255
imgR = imgR.astype('uint8')
salvar = "resultados/erosao1" + "image_3.png"
cv2.imwrite(salvar, imgR)

imgR = imgR.astype('float32')
imgR /= 255

#erosao2
imgR = erosao(imgR, 3)
imgR *= 255
imgR = imgR.astype('uint8')
salvar = "resultados/erosao2" + "image_3.png"
cv2.imwrite(salvar, imgR)

#plotar imagem
cv2.imshow("imagem", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()