matserver = py.mat_server.MatServer('test');
while true
    message = matserver.get();
    fprintf('%s\n', message);
    message = matserver.send([message ' has been received.']);
    pause(1);
end
