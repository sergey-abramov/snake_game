#!/usr/bin/env python3
"""
Тестовый скрипт для проверки всех компонентов игры "Змейка"
"""

import sys
import os

def test_python_version():
    """Проверка версии Python"""
    print("🐍 Проверка Python...")
    version = sys.version_info
    print(f"   Версия Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("   ❌ Требуется Python 3.7 или выше")
        return False
    else:
        print("   ✅ Версия Python подходит")
        return True

def test_pygame():
    """Проверка pygame"""
    print("\n🎮 Проверка pygame...")
    try:
        import pygame
        print(f"   Версия pygame: {pygame.version.ver}")
        
        # Тест инициализации
        pygame.init()
        print("   ✅ pygame успешно инициализирован")
        
        # Тест создания поверхности
        test_surface = pygame.Surface((100, 100))
        print("   ✅ Создание поверхностей работает")
        
        pygame.quit()
        return True
        
    except ImportError:
        print("   ❌ pygame не установлен")
        print("   Установите: pip install pygame")
        return False
    except Exception as e:
        print(f"   ❌ Ошибка pygame: {e}")
        return False

def test_game_import():
    """Проверка импорта игры"""
    print("\n🕹️ Проверка импорта игры...")
    try:
        from snake_game import SnakeGame, Direction, GameState
        print("   ✅ Основные классы импортированы")
        
        # Проверка enum'ов
        assert Direction.UP.value == (0, -1)
        assert Direction.RIGHT.value == (1, 0)
        print("   ✅ Enum Direction работает корректно")
        
        assert GameState.MENU.value == 1
        assert GameState.PLAYING.value == 2
        print("   ✅ Enum GameState работает корректно")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def test_files():
    """Проверка файлов проекта"""
    print("\n📁 Проверка файлов проекта...")
    
    files_to_check = [
        ('snake_game.py', 'Основной файл игры'),
        ('requirements.txt', 'Файл зависимостей'),
        ('README.md', 'Документация'),
        ('run_game.bat', 'Скрипт запуска')
    ]
    
    all_good = True
    for filename, description in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   ✅ {filename} ({description}) - {size} байт")
        else:
            print(f"   ❌ {filename} ({description}) - не найден")
            all_good = False
    
    return all_good

def test_game_logic():
    """Базовая проверка игровой логики"""
    print("\n🧮 Проверка игровой логики...")
    try:
        import pygame
        pygame.init()
        
        # Создаем минимальную поверхность для теста
        screen = pygame.Surface((800, 600))
        
        from snake_game import SnakeGame
        
        # Создаем объект игры (без реального окна)
        game = SnakeGame.__new__(SnakeGame)
        game.screen = screen
        game.clock = pygame.time.Clock()
        
        # Инициализируем шрифты
        game.font_large = pygame.font.Font(None, 48)
        game.font_medium = pygame.font.Font(None, 36)
        game.font_small = pygame.font.Font(None, 24)
        
        # Тестируем сброс игры
        game.reset_game()
        print("   ✅ Сброс игры работает")
        
        # Проверяем начальное состояние
        assert len(game.snake) == 1
        assert game.score == 0
        assert game.speed == 10
        print("   ✅ Начальное состояние корректно")
        
        # Тестируем генерацию еды
        food = game.generate_food()
        assert isinstance(food, tuple)
        assert len(food) == 2
        print("   ✅ Генерация еды работает")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка логики игры: {e}")
        pygame.quit()
        return False

def main():
    """Основная функция тестирования"""
    print("🔍 ТЕСТИРОВАНИЕ ИГРЫ 'ЗМЕЙКА'")
    print("=" * 40)
    
    tests = [
        test_python_version,
        test_pygame,
        test_files,
        test_game_import,
        test_game_logic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   💥 Неожиданная ошибка в тесте: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Игра готова к запуску!")
        print("\n🚀 Для запуска игры выполните:")
        print("   python snake_game.py")
        print("   или")
        print("   run_game.bat")
        return True
    else:
        print("❌ Некоторые тесты не пройдены. Проверьте ошибки выше.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Тестирование прервано пользователем.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        sys.exit(1)
