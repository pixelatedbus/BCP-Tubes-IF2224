program test5;

var 
    ifx, theny, z123, _hidden : integer;
    a, b : real;
    s : string;

begin
    a := 0.00123E+4;
    s := 'hello ''world''';
    ifx := 10;
    theny := ifx + 5;
    _hidden := theny - 3*2/4;

    if (a >= b) and not (ifx = 0) then
        writeln('a >= b')
    else
        writeln('a < b');
end.

