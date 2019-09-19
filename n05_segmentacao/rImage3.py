import cv2
import numpy as np
import PIL.Image as pil

#2356x2087

def lim(img):
    t = 183
    
    for i in range (img.shape[0]):
        for j in range (img.shape[1]):
            if img[i,j] < t:
                img[i, j] = 0
            else:
                img[i, j] = 255
    salvar = "resultados/(limiarizacacao50)" + "image_3.png"
    cv2.imwrite(salvar, img)
    return img

def sepLinhas(img):
    
    #Transforma imagem em RGB
    h = img.shape[0]
    w = img.shape[1]
    imgR = img.reshape(h, w, 1)
    imgRAux = imgR.copy()
    imgR = np.concatenate((imgR, imgRAux), axis = 2)
    imgR = np.concatenate((imgR, imgRAux), axis = 2)
    imgR = pil.fromarray(imgR)
    imgR = imgR.convert("RGB")
    
    pixels = imgR.load()
    
    '''for i in range(img.shape[1]):
        imgR[190, i] = 0'''
    cor = (255, 255, 0) # cor primeira linha   
    for i  in range(imgR.size[0]):
        for j in range(200):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
            
    '''for i in range(img.shape[1]):
        imgR[380, i] = 0'''
    cor = (47, 79, 79) # cor segunda linha   
    for i  in range(imgR.size[0]):
        for j in range(200, 380):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
                
    '''for i in range(img.shape[1]):
        imgR[570, i] = 0'''
    cor = (128, 0, 128) # cor terceira linha   
    for i  in range(imgR.size[0]):
        for j in range(380, 570):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
    
    '''for i in range(img.shape[1]):
        imgR[760, i] = 0'''
    cor = (178, 34, 34) # cor quarta linha   
    for i  in range(imgR.size[0]):
        for j in range(570, 760):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
        
    '''for i in range(img.shape[1]):
        imgR[950, i] = 0'''
    cor = (0, 255, 0) # cor quinta linha   
    for i  in range(imgR.size[0]):
        for j in range(760, 950):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
        
    '''for i in range(img.shape[1]):
        imgR[1140, i] = 0'''
    cor = (255, 140, 0) # cor sexta linha   
    for i  in range(imgR.size[0]):
        for j in range(950, 1140):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor   
        
    '''for i in range(img.shape[1]):
        imgR[1300, i] = 0'''
    cor = (0, 0, 255) # cor setima linha   
    for i  in range(imgR.size[0]):
        for j in range(1140, 1300):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
                
    '''for i in range(img.shape[1]):
        imgR[1490, i] = 0'''
    cor = (250, 128, 114) # cor oitava linha   
    for i  in range(imgR.size[0]):
        for j in range(1300, 1490):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
        
    '''for i in range(img.shape[1]):
        imgR[1650, i] = 0'''
    cor = (139, 69, 19) # cor nona linha   
    for i  in range(imgR.size[0]):
        for j in range(1490, 1650):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
        
    '''for i in range(img.shape[1]):
        imgR[1840, i] = 0'''
    cor = (0, 255, 255) # cor decima linha   
    for i  in range(imgR.size[0]):
        for j in range(1650, 1840):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
                
    cor = (0, 100, 0) # cor ultima linha   
    for i  in range(imgR.size[0]):
        for j in range(1840, 2087):
            if imgRAux[j, i] == 0:    
                pixels[i, j] = cor
        
    #salvar imagem
    salvar = "resultados/(teste33)" + "image_3.png"
    imgR.save(salvar)
    return imgR

img = cv2.imread("images/image_3.png", 0)

imgR = sepLinhas(lim(img))

"""#plotar imagem
cv2.imshow("imagem", imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()"""