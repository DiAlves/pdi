clc
close all
clear all

% read image 
I=imread('image_4.png');  
figure, imshow (I)

% create structuring element               
se= ones (3,3); 
  
% store number of rows in P and number of columns in Q.             
[P, Q]=size(se);  
  
% create a zero matrix of size I.         
In=zeros(size(I, 1), size(I, 2));  
  
for i=ceil(P/2):size(I, 1)-floor(P/2) 
    for j=ceil(Q/2):size(I, 2)-floor(Q/2) 
  
        % take all the neighbourhoods. 
        on=I(i-floor(P/2):i+floor(P/2), j-floor(Q/2):j+floor(Q/2));  
  
        % take logical se 
        nh=on(logical(se)); 
                % compare and take minimum value of the neighbor  
        % and set the pixel value to that minimum value.  
        In(i, j)=min(nh(:));       
    end
end

Im=zeros(size(In, 1), size(In, 2));  
  
for i=ceil(P/2):size(In, 1)-floor(P/2) 
    for j=ceil(Q/2):size(In, 2)-floor(Q/2) 
  
        % take all the neighbourhoods. 
        on=In(i-floor(P/2):i+floor(P/2), j-floor(Q/2):j+floor(Q/2));  
  
        % take logical se 
        nh=on(logical(se)); 
                % compare and take minimum value of the neighbor  
        % and set the pixel value to that minimum value.  
        Im(i, j)=min(nh(:));       
    end
end

Id = dilation (Im);


figure, imshow (Id)