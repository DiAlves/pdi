clc
clear all
close all

A = imread('image_3.png');
figure, imshow (A)
B = [1 1 1; 1 1 1; 1 1 1]; 
Xk = zeros(size(A)); 
Xk1 = Xk; 
Xk(50, 35) = 1;

%dilatação 1
A1 = dilation (A);

%erosão 1
se= ones (3,3);
[P, Q]=size(se);

A2=zeros(size(A1, 1), size(A1, 2));  
  
for i=ceil(P/2):size(A1, 1)-floor(P/2) 
    for j=ceil(Q/2):size(A1, 2)-floor(Q/2) 
  
        % take all the neighbourhoods. 
        on=A1(i-floor(P/2):i+floor(P/2), j-floor(Q/2):j+floor(Q/2));  
  
        % take logical se 
        nh=on(logical(se)); 
                % compare and take minimum value of the neighbor  
        % and set the pixel value to that minimum value.  
        A2(i, j)=min(nh(:));       
    end
end


while any(Xk(:) ~= Xk1(:))
    Xk1  =  Xk;     
    Xk = dilation(Xk1) & ~A2;
end 
  
A3 = Xk | A2;
A4= ~A3
figure, imshow (A4)