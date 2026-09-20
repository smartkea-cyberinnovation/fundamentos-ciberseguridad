@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Ejemplo BAT acotado a contar nombres del dataset. No calcula hashes.
if "%~1"=="" exit /b 2
if not "%~2"=="" exit /b 2
if not exist "%~1\.oslab" exit /b 2
if not exist "%~1\datos\" exit /b 2
findstr /L /X /C:"OSLAB-SYNTHETIC-1" "%~1\.oslab" >nul
if errorlevel 1 exit /b 2
set "count=0"
for /f "delims=" %%F in ('dir /b /a:-d-l "%~1\datos" 2^>nul') do set /a count+=1 >nul
echo {"count":%count%}
exit /b 0
