@echo off

:: environment activation
echo :: Activation of the virtual environment...
call venv\Scripts\activate

:: running the program
echo Running program...
python main.py
