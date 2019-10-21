function relMat=runlength(numCode)
    relMat = [];
    numCode = [numCode nan]; % dummy ending

    N = 1;
    for i = 1:length(numCode)-1   
       if numCode(i)==numCode(i+1)
          N = N + 1;
       else
          valuecode = numCode(i);
          lengthcode =  N;
          relMat = [relMat; valuecode lengthcode];
         N = 1;
       end
    end
end