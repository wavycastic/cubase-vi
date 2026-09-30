@echo off
REM Tim vcvars64.bat cua Visual Studio Build Tools va chay no trong shell hien tai.
REM Bien dich hook can MSVC; may nay co BuildTools 2022 nhung PATH chua co san.
REM
REM   find_vcvars.bat <duong dan mac dinh>

set "V=vcvars64.bat"
if not "%~1"=="" set "V=%~1"

if exist "%~dp0..\..\..\" rem giup cho nhan ra dang chay tu hook\

if exist "%V%" (
    call "%V%" >nul 2>&1
    if errorlevel 1 (
        echo LOI: goi "%V%" that bai
        exit /b 1
    )
    exit /b 0
)

echo LOI: khong tim thay "%V%".
echo Cai Visual Studio 2022 Build Tools, hoac truyen duong dan:
echo   find_vcvars.bat "C:\...\VC\Auxiliary\Build\vcvars64.bat"
exit /b 1
