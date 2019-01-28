Fs = 1000;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = 1500;             % Length of signal
t = (0:L-1)*T;        % Time vector

%S = 0.7*sin(2*pi*50*t) + sin(2*pi*120*t);
%S = 1 + zeros(size(t));
%S(10) = 1000;
%S = t.^3.2;
S = (2000-t).^1.2;
X = S + 2*randn(size(t));

figure()
plot(1000*t(1:50),X(1:50))
title('Signal Corrupted with Zero-Mean Random Noise')
xlabel('t (milliseconds)')
ylabel('X(t)')

Y = fft(X);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

figure()
f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of X(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')

Y = fft(S);
P2s = abs(Y/L);
P1s = P2s(1:L/2+1);
P1s(2:end-1) = 2*P1s(2:end-1);

figure()
plot(f,P1s) 
title('Single-Sided Amplitude Spectrum of S(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')