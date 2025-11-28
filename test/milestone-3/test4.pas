program ProceduresAndFunctions;

variabel
    a, b: integer;
    sum: integer;

prosedur swap(var x: integer; var y: integer);
variabel
    temp: integer;
mulai
    temp := x;
    x := y;
    y := temp
selesai;

fungsi add(p: integer; q: integer): integer;
variabel
    result: integer;
mulai
    result := p + q
selesai;

mulai
    a := 10;
    b := 20;
    sum := 0
selesai.
