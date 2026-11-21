# A library in a folder

For a library in a folder, write `package.mo` plus one file per class. Load it with
`loadFile("MyLib/package.mo")`: OpenModelica loads the whole folder from there.
`run_tests.py` takes any file of the library and finds the top-level `package.mo` itself. Each
file starts with `within PackageName;`, and a `package.order` file lists the classes in order.

Every folder is a package and needs its own file named exactly `package.mo`:

    MyLib/package.mo                 within ;                package MyLib end MyLib;
    MyLib/package.order              Sub
    MyLib/Sub/package.mo             within MyLib;           package Sub end Sub;
    MyLib/Sub/package.order          Model1 and Tests, one name per line
    MyLib/Sub/Model1.mo              within MyLib.Sub;       model Model1 ... end Model1;
    MyLib/Sub/Tests/package.mo       within MyLib.Sub;       package Tests end Tests;
    MyLib/Sub/Tests/Test1.mo         within MyLib.Sub.Tests; model Test1 ... end Test1;

A `package.mo` holds only the package line, its `end` and optionally constants or imports; the
classes in their own files are not declared in it (no `model Model1;` lines).

A file named like its folder (`Sub/Sub.mo`) is not loaded, and nothing below it either;
`loadFile` still returns true with no message. The `within` line is the folder path with dots,
without the class itself. "Error: Class MyLib.Sub.X not found in scope <top>." means exactly
this: a `package.mo` is missing or misnamed, or a `within` line does not match the folder. Check
with `find MyLib -name '*.mo'` and `head -2` of each file.
