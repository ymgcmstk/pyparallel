mat_data_server = MatDataServer('MatDataServerTest')
while true
    data = mat_data_server.get();
    data_sum = sum(data);
    data = mat_data_server.send(num2str(data_sum));
    pause(1);
end
