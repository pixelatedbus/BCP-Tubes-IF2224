program RecordTypes;

tipe
    Point = rekaman
        x: integer;
        y: integer;
    selesai;
    
    Person = rekaman
        name: char;
        age: integer;
        height: real;
        active: boolean;
    selesai;

variabel
    p1, p2: Point;
    student: Person;
    teacher: Person;
    counter: integer;

mulai
    counter := 0
selesai.
