function asserting(predicate, string)
% ASSERTING Raise an error if the predicate is not true.
if nargin<2, string = ''; end

if ~predicate
  s = sprintf('assertion violated: %s', string);
  error(s);
end
