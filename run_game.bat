@echo off
echo Запуск игры "Змейка"...
echo ========================

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден! Установите Python с python.org
    pause
    exit /b 1
)

REM Проверка pygame
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Установка pygame...
    pip install pygame
    if errorlevel 1 (
        echo ОШИБКА: Не удалось установить pygame
        pause
        exit /b 1
    )
)

REM Запуск игры
echo Запуск игры...
python snake_game.py

REM Пауза перед закрытием (если есть ошибки)
if errorlevel 1 (
    echo.
    echo Произошла ошибка при запуске игры.
    pause
)
