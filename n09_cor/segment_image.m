clear all;
clc;
close all
itemp = imread('image_3.png');%l� a imagem
%image = itemp(:,:,1);
rmin = 0;         %valor m�n de n�vel de intensidade
rmax = 255;         %valor max de n�vel de intensidade
R (:,:,1) = itemp; 
G (:,:,2) = itemp; 
B (:,:,3) = itemp;

rgbImage = cat(3, itemp, itemp, itemp);

%imshow(rgbImage);
%pause;
[r,c,m]= size(rgbImage); % dimens�es da imagem
s = zeros(r,c,m);     % guarda as variav�is da imagem resultante

%rgbImage = rgbImage(:,:,1) >= rmin .* 255;

%teste = uint8(((rgbImage(:,:,1) >= rmin && rgbImage(:,:,1) <= rmax) .*
%255) + rgbImage);
imshow(rgbImage)
for i = 1:r
    for j = 1:c
       % se o pixel estiver no range ele � setado para 30
        if (rmin < rgbImage(i,j,3) && rgbImage(i,j,3) < rmax)  
            rgbImage(i,j,1) = 255;
            rgbImage(i,j,2) = 255;
        end
    end
end
imshow(rgbImage)
%figure,imshow(uint8(itemp))  %imagem original
%figure,imshow(uint8(s))      %resultado