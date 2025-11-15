program BigTest;

konstanta
    pi = 314;                
    hello = 'hi';

tipe
    age = integer;

variabel
    a, b: integer;
    c: char;
    flag: boolean;
    idx: integer;

fungsi AddThree(x, y: integer; z: real): real;
variabel
    temp: real;
mulai
    temp := x + y + z;
    AddThree := temp;
selesai;

prosedur Outer(u: integer);

    variabel
        localA: integer;

    prosedur Inner(v: integer);
    mulai
        localA := u + v;
        write(localA);
    selesai;

mulai
    localA := u * 2;
    Inner(localA);
selesai;

mulai
    a := 5;
    b := 10;
    c := 'Z';
    flag := tidak (a > 3);

    jika a < b maka
        write(a)
    selain_itu
        write(b);

    idx := 0;
    selama idx < 3 lakukan
    mulai
        idx := idx + 1;
        write(idx);
    selesai;


    untuk idx := 1 ke 3 lakukan
        write(idx);

    Outer(7);

    a := (b * 3 + 1) mod 4 - (2 * (3 + a));

    flag := (a < b) dan tidak (b = 10) atau (a = 5);

selesai.
