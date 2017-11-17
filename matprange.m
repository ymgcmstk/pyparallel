classdef matprange < handle
    properties (Access = public)
        % public (arguments)
        first
        last
        id
        % public (to be checked by users)
        isover
        % private
    end
    properties (Access = private)
        parobj
        next_val
    end
    methods
        % constructor
        function obj = matprange(varargin)
            assert(nargin > 1);
            assert(nargin < 5);
            if nargin == 2
                obj.first = int64(1);
                obj.last  = int64(varargin{2});
                obj.id    = sprintf('%sF%dL%d', varargin{1}, obj.first, obj.last);
            elseif nargin == 3
                obj.first = int64(varargin{2});
                obj.last  = int64(varargin{3});
                obj.id    = sprintf('%sF%dL%d', varargin{1}, obj.first, obj.last);
            end
            fprintf('[matprange] id: "%s"\n', obj.id);
            obj.parobj = py.parallel_toolbox.prange_matlab(obj.id, obj.first, obj.last + 1);
            obj.isover = false;
            obj.prepare_next();
        end
        function val = next(obj)
            val = obj.next_val;
            obj.prepare_next();
        end
        function prepare_next(obj)
            try
                obj.next_val = obj.parobj.next();
            catch ME
                if strcmp(ME.identifier,'MATLAB:Python:PyException') && strcmp(ME.message,'Python Error: StopIteration')
                    obj.isover = true;
                    obj.next_val = [];
                else
                    rethrow(ME)
                end
            end
        end
    end
end
