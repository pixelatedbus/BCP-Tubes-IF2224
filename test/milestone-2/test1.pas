program BigTest;

konstanta
    pi = 314;                
    hello = 'hi';

tipe
    age = integer;            
    realArray = array[1..10] of real;
    point = record            
        x: integer;
        y: integer;
    end;

variabel
    a, b: integer;            
    p: point;                 
    arr: realArray;           
    c: char;
    s: string;
    flag: boolean;
    idx: integer;

procedure PrintPoint(pt: point);
begin
    write(pt.x);
    write(' ');
    write(pt.y);
end;

function AddThree(x, y: integer; z: real): real;
var
    temp: real;
begin
    temp := x + y + z;
    AddThree := temp;
end;

procedure Outer(u: integer);

    var
        localA: integer;

    procedure Inner(v: integer);
    begin
        localA := u + v;
        write(localA);
    end;

begin
    localA := u * 2;
    Inner(localA);
end;

begin
    a := 5;
    b := 10;
    c := 'Z';
    s := 'test';
    flag := tidak (a > 3);             
    arr[1] := 3.14;

    p.x := a;
    p.y := b;

    if a < b then
        write(a)
    else
        write(b);

    idx := 0;
    while idx < 3 do
    begin
        idx := idx + 1;
        write(idx);
    end;


    for idx := 1 to 3 do
        write(idx);

    arr[2] := AddThree(1, 2, 3.5);

    PrintPoint(p);

    Outer(7);

    a := (b * 3 + 1) mod 4 - (2 * (3 + a));

    flag := (a < b) dan tidak (b = 10) atau (a = 5);

end.
