clc
clear all
close all
myFolder1 = 'C:\Users\aline\OneDrive\Documents\Mestrado\PDI\n07_representacao\images\train';
filePattern1 = fullfile(myFolder1, '*.png');
jpegFiles1   = dir(filePattern1);

iteracoes=12;

for k=1:iteracoes
    baseFileName = jpegFiles1(k).name;
  fullFileName = fullfile(myFolder1, baseFileName);
  fprintf('Now reading %s\n', fullFileName)
  %lê as imagens da pasta de treino
  img = double(imread(fullFileName));
  
tic;
LBP= efficientLBP(img, [2,3]);
effTime=toc;

%mostra as features de textura
figure
imshow(LBP);
title('LBP image');
imwrite (LBP, sprintf('%d.png',k));
 % Verifica se a implementação "wise-pixel" retorna os mesmos valores
tic;
pixelWiseLBP=efficientLBP(img, [2,3], false);
inEffTime=toc;
fprintf('\nRun time ratio %.2f. Is equal result: %o.\n', inEffTime/effTime,...
   isequal(LBP, pixelWiseLBP));
end

