classdef MatDataServer < handle
    properties (Access = private)
        matserver
    end
    methods
        % constructor
        function obj = MatDataServer(varargin)
            assert(nargin < 2);
            assert(nargin < 5);
            id = 'test';
            if nargin == 1
                id = varargin{1};
            end
            obj.matserver = py.mat_server.MatServer(id);
        end
        function val = get(obj)
            data = matserver.get();
            data = load(data);
            val = data.data;
        end
        function val = send(obj, message)
            val = matserver.send(message);
        end
    end
end