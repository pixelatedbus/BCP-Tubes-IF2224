program Test5;

fungsi AddOne(x: integer): integer;
mulai
    AddOne := x + 1;
selesai;

prosedur PrintTwice(v: integer);
mulai
    write(v);
    write(v);
selesai;

variabel
    a: integer;
    ok: boolean;

mulai
    a := AddOne(7);
    ok := (a > 5) dan tidak (a = 10);

    jika ok maka
        PrintTwice(a)
    selain_itu
        write(0);

selesai.
