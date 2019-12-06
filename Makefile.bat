set CC=python
set TESTER=src/MiniCInterpreter.py
set TEST_OPT=test
set TEST_DIR=testfiles

echo %TEST_DIR%

if %1 == test (
for /f %%f in ('dir /b .\%TEST_DIR%\*.txt') do %CC% %TESTER% .\%TEST_DIR%\%%f %TEST_OPT% > .\%TEST_DIR%\results\%%f
)

if %1 ==clean (
	del .\%TEST_DIR%\results\*.txt
)

if %1 == test2 (
for /f %%f in ('dir /b .\%TEST_DIR%\*.txt') do echo %%f
)
