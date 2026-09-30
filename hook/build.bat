@echo off
REM Bien dich hook\wavehook.dll bang MSVC 2022 BuildTools.
REM
REM   build.bat            x64, /MD
REM   build.bat debug      x64, /MTd (de debug voi Visual Studio)
REM
REM Ket qua: hook\wavehook.dll
REM
REM Vao sao de trong 'hook' roi chay. Sai thu muc se khong tim thay file.

setlocal enabledelayedexpansion

set "ARCH=x64"
if /i "%PROCESSOR_ARCHITECTURE%"=="ARM64" set "ARCH=arm64"
if /i "%~1"=="debug" (set CFG=debug) else (set CFG=release)

REM Ten file ra co the doi. DLL da nap vao Cubase se giu file cu cho toi
REM khi Cubase chay, nen `link` bao LNK1104 "cannot open file". Khi do, build
REM sang ten moi thay vi bat buoc dong Cubase.
set OUT=%~2
if "%OUT%"=="" set OUT=wavehook.dll

REM --- tim MSVC -------------------------------------------------------
REM Thu vien MSVC cua Build Tools nam o: ...\VC\Tools\MSVC\<ver>\
set "TOOLSROOT=%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC"
if not exist "%TOOLSROOT%" (
    echo LOI: khong thay MSVC tai "%TOOLSROOT%"
    echo Cai Visual Studio 2022 Build Tools truoc.
    exit /b 1
)
for /f "delims=" %%V in ('dir /b /ad "%TOOLSROOT%" 2^>nul') do set "VCDIR=%TOOLSROOT%\%%V"

if not defined VCDIR (
    echo LOI: khong tim thay phien ban MSVC nao trong "%TOOLSROOT%"
    exit /b 1
)

REM Tool host luon la Hostx64, va moi host co thu muc con theo target:
REM Hostx64\x64 (64 bit), Hostx64\x86 (32 bit). Khong co Hostx64\ml64.exe.
set "BIN=%VCDIR%\bin\Hostx64\%ARCH%"
set "LIB=%VCDIR%\lib\%ARCH%"
set "INC=%VCDIR%\include"

REM Windows SDK: lay ban moi nhat
set "SDKT=%ProgramFiles(x86)%\Windows Kits\10\Include"
if not exist "%SDKT%" (
    echo LOI: khong thay Windows SDK tai "%SDKT%"
    exit /b 1
)
REM CHI lay TEN phien ban ("10.0.26100.0"), khong lay ca duong dan. Sau do
REM noi lai. Lan truoc gan ca duong dan vao bien, roi noi them lan nua, ra
REM "...\Lib\C:\Program Files\...\Include\10.0.26100.0" - link bao
REM LNK1104 khong tim thay uuid.lib.
set "WK=%ProgramFiles(x86)%\Windows Kits\10"
set "SDKT=%WK%\Include"
if not exist "%SDKT%" (
    echo LOI: khong thay Windows SDK tai "%SDKT%"
    echo Cai Windows 10 SDK cung voi Visual Studio Build Tools.
    exit /b 1
)
set "SDKDIR="
for /f "delims=" %%S in ('dir /b /ad "%SDKT%" 2^>nul') do set "SDKDIR=%%S"
if not defined SDKDIR (
    echo LOI: khong co ban Windows SDK nao trong "%SDKT%"
    exit /b 1
)
set "SDKLIBROOT=%WK%\Lib\%SDKDIR%"
set "SDKUM=%WK%\Include\%SDKDIR%\um"
set "SDKSH=%WK%\Include\%SDKDIR%\shared"

REM Bo .lib cua SDK: KHONG phai ...\Lib\<ver>\<arch>\um\ ma la
REM ...\Lib\<ver>\um\<arch>\. Sai duong dan nay thi link bao
REM LNK1104 "cannot open file 'uuid.lib'".

echo === moi truong ===
echo   MSVC   !VCDIR!
echo   SDK    !SDKDIR!
echo   arch   %ARCH%   cfg %CFG%

set "PATH=%BIN%;%VCDIR%\bin\Hostx64\x86;%PATH%"
if not exist "%BIN%\cl.exe" (
    echo LOI: khong thay cl.exe tai "%BIN%"
    echo Ban MSVC nay co the chi ho tro host 32 bit. Kiem lai thu muc:
    dir /b "%VCDIR%\bin"
    exit /b 1
)

REM dung ! bien mo rong chu khong phai % bien, vi khoi if/else la MOT khoi
REM duy nhat va % se duoc mo rong o luc DOC khoi - luc do cac bien duoi
REM chua duoc gan. Dung % se ra rong nen link khong tim thay thu vien.
if /i "!CFG!"=="debug" (
    set "CFLAGS=/nologo /c /O1 /Zi /MTd /DDEBUG /W4 /I"!INC!" /I"!SDKUM!" /I"!SDKSH!""
    set "LFLAGS=/nologo /DLL /DEBUG /LIBPATH:"!LIB!" /LIBPATH:"!SDKLIBROOT!\ucrt\!ARCH!" /LIBPATH:"!SDKLIBROOT!\um\!ARCH!" /MACHINE:!ARCH!"
) else (
    set "CFLAGS=/nologo /c /O2 /MT /W4 /I"!INC!" /I"!SDKUM!" /I"!SDKSH!""
    set "LFLAGS=/nologo /DLL /LIBPATH:"!LIB!" /LIBPATH:"!SDKLIBROOT!\ucrt\!ARCH!" /LIBPATH:"!SDKLIBROOT!\um\!ARCH!" /MACHINE:!ARCH!"
)
echo   LFLAGS=!LFLAGS!
REM /Safer khong ton tai o ml64 (chi co o MASM32 doi voi assembler cu). Bo
REM no khoi MFLAGS; /Safer la thuoc tinh cua cua so rieng cho MASM32.
set MFLAGS=/nologo /c /I"%INC%"

echo === bien dich %CFG% -> %OUT% ===
ml64 %MFLAGS% wavehook.asm
if errorlevel 1 (echo LOI: ml64 that bai & exit /b 1)

REM Phai bien dich ca wavecolour.c: ham cong thuc mau nam o file rieng, nen
REM khong duoc quen no o khi link.
cl %CFLAGS% wavehook.c /Fohook.obj
if errorlevel 1 (echo LOI: cl wavehook.c that bai & exit /b 1)

cl %CFLAGS% wavecolour.c /Fowavecolour.obj
if errorlevel 1 (echo LOI: cl wavecolour.c that bai & exit /b 1)

cl %CFLAGS% waveprobe.c /Fowaveprobe.obj
if errorlevel 1 (echo LOI: cl waveprobe.c that bai & exit /b 1)

REM Xoa file .exp/.lib cu. `%OUT:.dll=.exp` KHONG phai phép bien thi cua
REM cmd - `%OUT%` la bien thuong, nên cmd hieu `:.dll=.exp` la phan cua ten
REM tep roi va tim file ten "OUT:.dll". Phai tach bang bien rieng.
set "BASE=%OUT:.dll=%"
if exist "%BASE%.exp" del "%BASE%.exp"
if exist "%BASE%.lib" del "%BASE%.lib"

link %LFLAGS% /DEF:wavehook.def /OUT:%OUT% hook.obj wavehook.obj wavecolour.obj waveprobe.obj
if errorlevel 1 (echo LOI: link that bai & exit /b 1)

if not exist %OUT% (
    echo LOI: khong tao duoc %OUT%
    exit /b 1
)

REM Kiem tra DLL co that su co cac ham can dung truoc khi tay vao may cua
REM nguoi dung. Thieu export thi injector se load duoc nhung goi that bai.
for %%E in (WaveHook_Install WaveHook_InstallAt WaveHook_Remove WaveDrawHook WaveDrawTrampoline WaveDrawTrampolineVA WaveDrawResumeVA WaveProbe_InstallAll WaveProbe_RemoveAll WaveProbe_Count WaveProbeCommon WaveProbeTrampVA g_probeCount g_probeArg0) do (
    dumpbin /exports %OUT% | find "%%E" >nul
    if errorlevel 1 (
        echo LOI: thieu export %%E
        exit /b 1
    )
)
echo   exports: Install, InstallAt, Remove, IsInstalled, hook, trampoline, VA

for %%F in (%OUT%) do echo === xong: %%~zF byte  %%F ===
endlocal
