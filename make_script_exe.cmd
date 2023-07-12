@echo off
cd "C:\Users\hp\Documents\My_Data\Python Projects\Qt\VoiceNote"
REM Check if "dist" directory exists and delete it if found
if exist dist (
    echo Deleting existing "dist" directory...
    rd /s /q dist
)

REM Check if "build" directory exists and delete it if found
if exist build (
    echo Deleting existing "build" directory...
    rd /s /q build
)

if exist main.spec (
    echo Deleting existing 'main.spec' file...
    del /f main.spec
)


REM Execute the PyInstaller command
pyinstaller --windowed --icon="C:\Users\hp\Documents\My_Data\Python Projects\Qt\VoiceNote\ui\data\icon.png" main.py

REM Copy "ui" folder to "dist/main"
echo Copying "ui" folder to "dist/main"...
xcopy /s /e /i "ui" "dist\main\ui\"

pause
