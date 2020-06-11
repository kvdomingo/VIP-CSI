path(path, "D:\Kenneth\Documents\4-2\VIP\Algo\l1magic")
%set(groot, "defaultAxesTickLabelInterpreter", "latex");
%set(groot, "defaultLegendInterpreter", "latex");
set(0, "defaultTextInterpreter", "latex");

[dat ,rate] = audioread("guitar-midA.wav");
data = mean(dat, 2);
N = length(data);
dur = N./rate;
t = linspace(0, dur, N);

figure()
plot(t, data, "b-");
xlabel("Time, $t$ [sec]")
ylabel("Amplitude")
title("original, guitar @ std mid A (440 Hz)");

figure()
c = fft(data);
plot(abs(c), "b-");
xlabel("Frequency");
ylabel("Density");
title("original, guitar @ std mid A (440 Hz)");

c(7500:end) = 0;
sig = real(ifft(c));

figure()
plot(t, sig, "b-");
xlabel("Frequency");
ylabel("Density");
title("original, guitar @ std mid A (440 Hz) with removed harmonics");

k = 0.75;
M = k*N;
ri = sort(randi(0, N, M));
b = sig(ri);