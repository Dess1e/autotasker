@echo off
where >nul 2>nul pip
IF %ERRORLEVEL% NEQ 0 (
 GOTO no_pip 
 ) ELSE (
 GOTO pip_okay
 )
:pip_checked
where >nul 2>nul python
IF %ERRORLEVEL% NEQ 0 (GOTO no_py) ELSE (GOTO py_okay)
:py_checked
GOTO end

:pip_okay
echo Pip is present in path, performing libs installation...
timeout /T 3
echo:
echo:
pip install PyQt5
pip install opencv-python
pip install numpy
GOTO pip_checked

:py_okay
echo:
echo:
echo Done!
echo Generating start.bat...
echo python main.py > start.bat
echo Launch the executable by executing start.bat
echo:
GOTO py_checked

:no_pip
echo Pip executable is not found in path
echo Attempting to find one...
FOR /F "delims=" %%i IN ('where /r %systemdrive% pip.exe') DO set pippath=%%i
IF [%pippath%] == [] (
echo Pip is not found! Aborting...
GOTO end
) ELSE (
echo Pip executable found at:
echo %pippath%
echo Performing libs installation...
timeout /T 3
echo:
echo:
%pippath% install PyQt5
%pippath% install opencv-python
%pippath% install numpy
GOTO pip_checked
)

:no_py
echo:
echo Python executable is not found in path
echo Please make sure your Python 3.5.2 executable is added to PATH variable
echo ^(This can be simply done by reinstalling Python and checking the checkbox during the installation process^)
echo:
echo Attempting to find the Python executable...
FOR /F "delims=" %%i IN ('where /r %systemdrive% python.exe') DO set pypath=%%i
echo:
echo:
IF [%pypath%] == [] (
echo Python is not found! Aborting...
GOTO end
) ELSE ( 
echo
echo Python executable found at:
echo    %pypath%
echo Generating start.bat...
echo %pypath% main.py > start.bat
echo Launch the executable by executing start.bat
echo:
GOTO py_checked
)

:end
pause
