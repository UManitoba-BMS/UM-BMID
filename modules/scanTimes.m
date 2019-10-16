function [scanTimes] = scanTimes(iniF, finF, nFreqs)
%GETSCANTIMES Summary of this function goes here
%   Detailed explanation goes here

freqs = linspace(iniF, finF, nFreqs);
freqStep = freqs(2) - freqs(1);

timeStep = 1 / (nFreqs * freqStep);

scanTimes = linspace(0, nFreqs * timeStep, nFreqs);

end

