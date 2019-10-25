import cv2

def gamma(img, g):
    imgR = img.copy()
    #Componente R
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            imgR.itemset((i, j, 0), img.item(i, j, 0) ** (1 / g))
    #Componente G
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            imgR.itemset((i, j, 1), img.item(i, j, 1) ** (1 / g))
    
    #Componente B
    for i in range (0, img.shape[0]):
        for j in range (0, img.shape[1]):
            imgR.itemset((i, j, 2), img.item(i, j, 2) ** (1 / g))
            
    return imgR

img = cv2.imread("images/image_1b.png") #Abrir a imgem 

#Criar uma imagem normalizada
imgN = img.astype('float32')
imgN /= 255

imgR = gamma(imgN, 0.7)

imgR *= 255
imgR = imgR.astype('float32')

#salvar imagem
salvar = "resultados/(escurecer-Gamma0.7)image_1b.png"
cv2.imwrite(salvar, imgR)

#plotar imagem
cv2.imshow("imagem_1", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()