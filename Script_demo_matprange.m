n_last = int32(5);
mp = matprange('temp', n_last);
while ~mp.isover
    fprintf('%d / %d\n', mp.next(), n_last);
    pause(1);
end
assert(mp.isover)
