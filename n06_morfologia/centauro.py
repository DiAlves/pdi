import cv2
import numpy as np

def and1(img1, img2):
    imgR = np.zeros((img1.shape[0], img1.shape[1]))
    for i in range (imgR.shape[0]):
        for j in range (imgR.shape[1]):
            if (img1[i, j] == 255 and img2[i, j] == 255):
                imgR[i, j] = 255
                
    return imgR

def nand1(img1, img2):
    imgR = np.zeros((img1.shape[0], img1.shape[1]))
    for i in range (imgR.shape[0]):
        for j in range (imgR.shape[1]):
            if (img1[i, j] == 0 or img2[i, j] == 0):
                imgR[i, j] = 255
   
    return imgR

def or1(img1, img2):
    imgR = np.zeros((img1.shape[0], img1.shape[1]))
    for i in range (imgR.shape[0]):
        for j in range (imgR.shape[1]):
            if (img1[i, j] == 255 or img2[i, j] == 255):
                imgR[i, j] = 255
   
    return imgR

def xor1(img1, img2):
    imgR = np.zeros((img1.shape[0], img1.shape[1]))
    for i in range (imgR.shape[0]):
        for j in range (imgR.shape[1]):
            if (img1[i, j] == 0 and img2[i, j] == 255) or (img1[i, j] == 255 and img2[i, j] == 0):
                imgR[i, j] = 255
   
    return imgR


#abrir imagem
imgA = cv2.imread("images/image_1a.png", 0)
imgB = cv2.imread("images/image_1b.png", 0)
imgC = cv2.imread("images/image_1c.png", 0)
imgD = cv2.imread("images/image_1d.png", 0)
imgE = cv2.imread("images/image_1e.png", 0)
imgF = cv2.imread("images/image_1f.png", 0)


imgFlecha = and1(imgA, imgB)
salvar = "resultados/(Flecha)" + "image_1.png"
cv2.imwrite(salvar, imgFlecha)

imgGetPernas = nand1(imgFlecha, imgC)
salvar = "resultados/(pernas)" + "image_1.png"
cv2.imwrite(salvar, imgGetPernas)

imgTirarPernas = and1(imgFlecha, imgGetPernas)
salvar = "resultados/(TirarPernas)" + "image_1.png"
cv2.imwrite(salvar, imgTirarPernas)

imgCavalo = nand1(imgD, imgE)
salvar = "resultados/(cavalo)" + "image_1.png"
cv2.imwrite(salvar, imgCavalo)

imgCabecaCavalo = nand1(imgF, imgCavalo)
salvar = "resultados/(cabecaCavalo)" + "image_1.png"
cv2.imwrite(salvar, imgCabecaCavalo)

imgCorpoCavalo = and1(imgCavalo, imgCabecaCavalo)
salvar = "resultados/(corpoCavalo)" + "image_1.png"
cv2.imwrite(salvar, imgCorpoCavalo)

imgCentauro = or1(imgTirarPernas, imgCorpoCavalo)
salvar = "resultados/(centauro)" + "image_1.png"
cv2.imwrite(salvar, imgCentauro)

#plotar imagem
cv2.imshow("imagem", imgCentauro)
cv2.waitKey(0)
cv2.destroyAllWindows()