clc
clear all
close all
%abrindo as imagens do dataset
myFolder1 = 'C:\Users\aline\OneDrive\Documents\Mestrado\PDI\n07_representacao\images\train';
filePattern1 = fullfile(myFolder1, '*.png');
jpegFiles1   = dir(filePattern1);

iteracoes=12;

for k=1:iteracoes
    baseFileName = jpegFiles1(k).name;
  fullFileName = fullfile(myFolder1, baseFileName);
  fprintf('Now reading %s\n', fullFileName)
  
  img = double(imread(fullFileName));
  %realizado o cálculo dos 7 momentos de Hu
  I= moment_hu (img);
  fprintf ('Hu Moment: %s\n',I)
  dlmwrite(sprintf('%d.txt', k), I);
end

