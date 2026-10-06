@echo off
REM Bien dich hook\wheelprobe.dll - ban CHI QUAN SAT, dung khuong mau.
REM
REM   cd hook && build_probe.bat
REM
REM Tach rieng build.bat vi build.bat lien ket wavehook.asm va kiem tra
REM danh sach export cua wavehook. Ban nay chi co mot file C, khong co ASM,
REM va kiem tra export cua rieng no - dung chung mot khoi lenh MSVC se
REM phai sua ca hai ben.
REM
REM Khuong mau phai dung khi can xem chuoi: ban chan do thi mat ngay thong
REM tin, nhung no khong can khi chay trong Cubase.
REM
REM `enabledelayedexpansion` bat buoc: moi khoi if/else la MOT khoi duy nhat,
REM nen `%ARCH%` trong khoi do se mo rong khi DOC (luc bien do chua duoc gan)
REM va ra rong. Chi `!ARCH!` moi dung. xem wavehook/build.bat.
setlocal enabledelayedexpansion
set "ARCH=x64"
if /i "%PROCESSOR_ARCHITECTURE%"=="ARM64" set "ARCH=arm64"

set "TOOLSROOT=%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC"
if not exist "%TOOLSROOT%" (
    echo LOI: khong thay MSVC tai "%TOOLSROOT%"
    exit /b 1
)
for /f "delims=" %%V in ('dir /b /ad "%TOOLSROOT%" 2^>nul') do set "VCDIR=%TOOLSROOT%\%%V"
if not defined VCDIR (
    echo LOI: khong tim thay phien ban MSVC nao
    exit /b 1
)
set "BIN=%VCDIR%\bin\Hostx64\%ARCH%"
set "LIB=%VCDIR%\lib\%ARCH%"
set "INC=%VCDIR%\include"

set "WK=%ProgramFiles(x86)%\Windows Kits\10"
set "SDKT=%WK%\Include"
if not exist "%SDKT%" (
    echo LOI: khong thay Windows SDK tai "%SDKT%"
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

echo === moi truong ===
echo   MSVC   !VCDIR!
echo   SDK    !SDKDIR!
echo   arch   %ARCH%

set "PATH=%BIN%;%VCDIR%\bin\Hostx64\x86;%PATH%"
if not exist "%BIN%\cl.exe" (
    echo LOI: khong thay cl.exe tai "%BIN%"
    dir /b "%VCDIR%\bin"
    exit /b 1
)

if /i "%~1"=="debug" (
    set "CFLAGS=/nologo /c /O1 /Zi /MTd /DDEBUG /W4 /I"!INC!" /I"!SDKUM!" /I"!SDKSH!""
    set "LFLAGS=/nologo /DLL /DEBUG /LIBPATH:"!LIB!" /LIBPATH:"!SDKLIBROOT!\ucrt\!ARCH!" /LIBPATH:"!SDKLIBROOT!\um\!ARCH!" /MACHINE:!ARCH!"
) else (
    set "CFLAGS=/nologo /c /O2 /MT /W4 /I"!INC!" /I"!SDKUM!" /I"!SDKSH!""
    set "LFLAGS=/nologo /DLL /LIBPATH:"!LIB!" /LIBPATH:"!SDKLIBROOT!\ucrt\!ARCH!" /LIBPATH:"!SDKLIBROOT!\um\!ARCH!" /MACHINE:!ARCH!"
)

REM Xoa file .exp/.lib cu. Phai tach bien rieng: `:.dll=.exp` la phep bien
REM cua cmd, va `set "BASE=%OUT:.dll=%"` se ra rong -> link bao thieu thuvien.
set "BASE=wheelprobe"
if exist "%BASE%.exp" del "%BASE%.exp"
if exist "%BASE%.lib" del "%BASE%.lib"

echo === bien dich ===
cl %CFLAGS% wheelprobe.c /Fo%BASE%.obj
if errorlevel 1 (echo LOI: cl that bai & exit /b 1)

REM user32.lib: bat buoc. DLL nay chi goi ham cua user32 (SetWindowLongPtrA,
REM EnumWindows, GetKeyState, CallWindowProcA...), ma khong khai bao gi khac
REM nen linker khong tu doan. Thieu no -> 11 loi LNK2019, tat ca deu la
REM "__imp_" - dau hieu "co goi nhung quen noi thu vien".
link %LFLAGS% /OUT:%BASE%.dll %BASE%.obj user32.lib
if errorlevel 1 (echo LOI: link that bai & exit /b 1)

if not exist %BASE%.dll (
    echo LOI: khong tao duoc %BASE%.dll
    exit /b 1
)

REM Kiem tra export thuc su co truoc khi dua vao may cua nguoi dung.
REM Thieu export thi injector load duoc nhung goi that bai.
for %%E in (WheelProbe_Install WheelProbe_Remove WheelProbe_IsInstalled WheelProbe_Enable) do (
    dumpbin /exports %BASE%.dll | find "%%E" >nul
    if errorlevel 1 (
        echo LOI: thieu export %%E
        exit /b 1
    )
)
echo   exports: Install, Remove, IsInstalled, Enable

for %%F in (%BASE%.dll) do echo === xong: %%~zF byte  %%F ===
endlocal