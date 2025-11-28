program ComplexProgram;

konstanta
    MAX = 100;
    PI = 3.14159;

tipe
    Status = boolean;
    Age = integer;
    Score = real;
    
    StudentRecord = rekaman
        id: integer;
        grade: char;
        gpa: real;
    selesai;
    
    NumberList = larik[1..50] dari integer;

variabel
    isActive: Status;
    studentAge: Age;
    testScore: Score;
    student1: StudentRecord;
    numbers: NumberList;
    total: integer;

prosedur initialize;
mulai
    total := 0
selesai;

fungsi calculate(x: integer; y: integer): integer;
variabel
    temp: integer;
mulai
    temp := x + y
selesai;

fungsi average(count: integer; sum: real): real;
variabel
    result: real;
mulai
    result := sum
selesai;

mulai
    studentAge := 20;
    testScore := 95.5;
    total := 0
selesai.
