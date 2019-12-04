set CC=python
set TESTER=LexParTester.py
set TEST_OPT=par
set TEST_DIR=testfiles

echo %TEST_DIR%

if %1 == test (
for /f %%f in ('dir /b .\%TEST_DIR%\*.txt') do %CC% %TESTER% %TEST_OPT% .\%TEST_DIR%\%%f .\%TEST_DIR%\results\%%f
)

if %1 ==clean (
	del .\%TEST_DIR%\results\*.txt
)

if %1 == test2 (
for /f %%f in ('dir /b .\%TEST_DIR%\*.txt') do echo %%f
)

if %1 == testinterp (
for /f %%f in ('dir /b .\%TEST_DIR%\*.txt') do %CC% Interpreter.py .\%TEST_DIR%\%%f > .\%TEST_DIR%\results\%%f

)