%---------Square Wave created by Harmonics of Sin ------
clc, clear all;
mekadem=1; % set the coefficient (mekadem)
n=input('No. of Harmonics= ');
t=[0:0.1:20]; % t is the time
wave=0; % wave is the vector of the  Square wave we want to plot
for i=1:n % Loop to sum  n harmonics
     v=(1/mekadem)*sin(mekadem*t); % v  is a vector of the added harmonics
     mekadem=mekadem+2; % odd (e-Zoogi) coefficient
     wave=wave+v; % wave contains  now the accomulated result
end
plot(t,wave)
title('Square Wave Built from n Sin - Harmonics')
legend('Yaron Broda')
%-------Yaron Broda---------