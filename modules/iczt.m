function [tdData] = iczt(fdData, iniT, finT, nTimePts, iniF, finF)
% Compute the ICZT of frequency-domain data, transform to time domain
%
% Parameters
% ----------
% fdData : array
%   The frequency-domain array to be transformed via the ICZT to the
%   time domain
% iniT : float
%   Starting time-of-response used when computing the ICZT, in seconds
% finT : float
%   Final time-of-response used when computing the ICZT, in seconds
% nTimePts : int
%   The number of points in the time-domain at which the transform will
%   be evaluated at
% iniF : float
%   The initial frequency of the fdData, in Hz
% finF : float
%   The final frequency of the fdData, in Hz
%
% Returns
% -------
% tdData : array
%   The time-domain data obtained via the ICZT
%
%%

% Assert that fdData is 1D or 2D
assert(length(size(fdData)) == 1 | length(size(fdData)) == 2, ...
            'Error: fdData must be 1D or 2D array');

nFreqs = size(fdData, 1);  % Find number of frequencies

% Get the conversion factor to convert from time-of-response to angle
% around the unit circle
timeToAng = (2 * pi) / max(scanTimes(iniF, finF, nFreqs));

% Find the parameters for computing the ICZT over the specified 
% time window
thetaNaught = iniT * timeToAng;
phiNaught = (finT - iniT) * timeToAng / (nTimePts - 1);

% Compute the exponential values only once, outside loops
expThetaNaught = exp(-1j * thetaNaught);
expPhiNaught = exp(-1j * phiNaught);

% Create dummy var to faciliate vectorized computation
dummyVec = -1 * (0 : nFreqs - 1);

if length(size(fdData)) > 1  % If the fdData is 2D 
    
   % Init arr to return
   tdData = complex(zeros([nTimePts, size(fdData, 2)]));
   
   for ii = 1 : size(fdData, 2)  % For each antenna position
      
       for jj = 1 : nTimePts  % For each time point
           
          % Compute the ICZT by determining the z-value ...
          zHere = expThetaNaught * expPhiNaught.^(ii - 1);
          
          % ... and then sum over all the zs for this time point
          zSum = sum(fdData .* zHere.^dummyVec);
          
          tdData(ii, jj) = zSum / nFreqs;  % Store the obtained value
          
       end  % End loop over time points
   end  % End loop over antenna position
   
else  % If the fdData is 1D
    
    tdData = complex(zeros([nTimePts, ]));  % Init arr to return
    
    for ii = 1 : nTimePts  % Loop over time points
        
        % Compute the ICZT by determining the z-value...
        zHere = expThetaNaught * expPhiNaught.^(ii - 1);
        
        % ...and then sum over all the zs for this time point
        zSum = sum(fdData .* zHere.^dummyVec);
        
        tdData(ii) = zSum / nFreqs;  % Store the obtained value
        
    end  % End loop over time points
    
end  % End if statement for 1D or 2D fdData


end  % End function definition
