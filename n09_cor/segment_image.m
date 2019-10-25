clear all;
clc;
close all
itemp = imread('image_3.png');%lê a imagem
%image = itemp(:,:,1);
rmin = 0;         %valor mín de nível de intensidade
rmax = 255;         %valor max de nível de intensidade
R (:,:,1) = itemp; 
G (:,:,2) = itemp; 
B (:,:,3) = itemp;

rgbImage = cat(3, itemp, itemp, itemp);

%imshow(rgbImage);
%pause;
[r,c,m]= size(rgbImage); % dimensões da imagem
s = zeros(r,c,m);     % guarda as variavéis da imagem resultante

%rgbImage = rgbImage(:,:,1) >= rmin .* 255;

%teste = uint8(((rgbImage(:,:,1) >= rmin && rgbImage(:,:,1) <= rmax) .*
%255) + rgbImage);
imshow(rgbImage)
for i = 1:r
    for j = 1:c
       % se o pixel estiver no range ele é setado para 30
        if (rmin < rgbImage(i,j,3) && rgbImage(i,j,3) < rmax)  
            rgbImage(i,j,1) = 255;
            rgbImage(i,j,2) = 255;
        end
    end
end
imshow(rgbImage)
%figure,imshow(uint8(itemp))  %imagem original
%figure,imshow(uint8(s))      %resultado