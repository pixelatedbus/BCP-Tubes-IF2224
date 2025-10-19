program test4;
begin
    i := 0;
    j := 10;
    k := Max(i, j);

    x := 1.5;
    y := x * 2.0 + 3.14 / (x + 1.0);
    message := 'Hello, Lexer!';
    done := (x > y) or (not (x < y));
end.
