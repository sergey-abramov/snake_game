#!/usr/bin/env python3
"""
Финальная проверка готовности игры к запуску
"""

import sys
import os

def final_check():
    """Финальная проверка всех компонентов"""
    print("🎮 ФИНАЛЬНАЯ ПРОВЕРКА ИГРЫ 'ЗМЕЙКА'")
    print("=" * 50)
    
    # Проверка Python
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Проверка pygame
    try:
        import pygame
        print(f"✅ pygame {pygame.version.ver}")
    except ImportError:
        print("❌ pygame не установлен!")
        return False
    
    # Проверка файлов
    required_files = ['snake_game.py', 'README.md', 'requirements.txt']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} отсутствует!")
            return False
    
    # Проверка импорта игры
    try:
        from snake_game import SnakeGame
        print("✅ Игра корректно импортируется")
    except Exception as e:
        print(f"❌ Ошибка импорта игры: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ВСЕ ГОТОВО! ИГРА ПОЛНОСТЬЮ НАСТРОЕНА!")
    print("\n📝 ИНСТРУКЦИЯ ДЛЯ ЗАПУСКА:")
    print("1. Откройте терминал/командную строку")
    print("2. Перейдите в папку с игрой:")
    print(f"   cd {os.getcwd()}")
    print("3. Запустите игру одним из способов:")
    print("   • python snake_game.py")
    print("   • run_game.bat (двойной клик)")
    
    print("\n🎮 УПРАВЛЕНИЕ В ИГРЕ:")
    print("• ПРОБЕЛ - Начать игру/Пауза")
    print("• Стрелки - Управление змейкой")
    print("• ESC - Выход/Меню")
    
    print("\n🏆 ОСОБЕННОСТИ:")
    print("• Красивая графика с анимированной змейкой")
    print("• Система счета и сохранение рекордов")
    print("• Увеличение скорости по мере прогресса")
    print("• Полнофункциональное меню и пауза")
    
    return True

if __name__ == "__main__":
    try:
        if final_check():
            print("\n🚀 Готово к игре! Удачи!")
        else:
            print("\n❌ Есть проблемы, которые нужно исправить.")
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        sys.exit(1)
