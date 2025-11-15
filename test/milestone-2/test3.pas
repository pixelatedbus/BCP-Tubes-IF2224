program Loop;

variabel
    x, i: integer;
    ok: boolean;

mulai
    x := 5;
    ok := tidak (x = 3);

    jika ok maka
        write(x)
    selain_itu
        write(0);

    i := 1;
    selama i < 4 lakukan
    mulai
        write(i);
        i := i + 1;
    selesai;

    untuk i := 1 ke 3 lakukan
        write(i);

selesai.
