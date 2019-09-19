img=imread('teste.png');
figure,imshow(img)


T = imhist(img);
[m,n] = size(img);

N = m*n;
G =256;

pn = T/N;

pth(1)=pn(1)
for i=2:G
    pth(i)=pth(i-1)+pn(i);
end

E =[];
for t = 1:256
    hf=0;
    hb=0;
    if pth(t)>0
        for i=1:t
            if pn(i)>0
                hf = hf - pn(i)/pth(t)*log(pn(i)/pth(t));
            end
        end
    end
    
    
    if 1-pth(t)>0
        for i =t+1:256
            if pn(i)>0
                hb = hb-pn(i)/(1-pth(t))*log(pn(i)/(1-pth(t)));
            end
        end
    end
    
    E(t) = hf+hb
    
end

position = find(E==(max(E)));
threshold = position-1;


I = zeros(size(img));
I(img<threshold)=0;
I(img>threshold)=255;
figure,imshow(I)