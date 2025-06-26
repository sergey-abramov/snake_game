#!/usr/bin/env python3
"""
Игра "Змейка" с графическим интерфейсом
Создано с использованием pygame для плавной игровой механики
"""

import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple

# Константы игры
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Змейка - Snake Game")
        self.clock = pygame.time.Clock()
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Игровые переменные
        self.reset_game()
        self.state = GameState.MENU
        self.high_score = self.load_high_score()
        
    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.speed = 10  # Начальная скорость
        
    def generate_food(self) -> Tuple[int, int]:
        """Генерация еды в случайном месте"""
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), 
                   random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food
    
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                        
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                    elif event.key == pygame.K_SPACE:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
        
        return True
    
    def update_game(self):
        """Обновление логики игры"""
        if self.state != GameState.PLAYING:
            return
            
        # Движение змейки
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Проверка столкновения со стенами
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over()
            return
        
        # Проверка столкновения с собой
        if new_head in self.snake:
            self.game_over()
            return
        
        self.snake.insert(0, new_head)
        
        # Проверка поедания еды
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            # Увеличение скорости каждые 50 очков
            if self.score % 50 == 0:
                self.speed = min(self.speed + 1, 20)
        else:
            self.snake.pop()  # Убираем хвост если еда не съедена
    
    def game_over(self):
        """Обработка окончания игры"""
        self.state = GameState.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def load_high_score(self) -> int:
        """Загрузка рекорда из файла"""
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        """Сохранение рекорда в файл"""
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except IOError:
            pass  # Игнорируем ошибки записи
    
    def draw_snake(self):
        """Отрисовка змейки"""
        for i, segment in enumerate(self.snake):
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Голова змейки отличается от тела
            if i == 0:
                pygame.draw.rect(self.screen, DARK_GREEN, rect)
                pygame.draw.rect(self.screen, GREEN, rect, 2)
                # Глаза
                eye_size = 3
                eye_offset = 5
                if self.direction == Direction.UP:
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + eye_offset, y * GRID_SIZE + eye_offset), eye_size)
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + eye_offset), eye_size)
                elif self.direction == Direction.DOWN:
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset), eye_size)
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset), eye_size)
                elif self.direction == Direction.LEFT:
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + eye_offset, y * GRID_SIZE + eye_offset), eye_size)
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset), eye_size)
                else:  # RIGHT
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + eye_offset), eye_size)
                    pygame.draw.circle(self.screen, WHITE, 
                                     (x * GRID_SIZE + GRID_SIZE - eye_offset, y * GRID_SIZE + GRID_SIZE - eye_offset), eye_size)
            else:
                pygame.draw.rect(self.screen, GREEN, rect)
                pygame.draw.rect(self.screen, DARK_GREEN, rect, 1)
    
    def draw_food(self):
        """Отрисовка еды"""
        x, y = self.food
        center = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2)
        pygame.draw.circle(self.screen, RED, center, GRID_SIZE // 2 - 2)
        pygame.draw.circle(self.screen, WHITE, center, GRID_SIZE // 2 - 2, 2)
    
    def draw_grid(self):
        """Отрисовка сетки"""
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
    
    def draw_hud(self):
        """Отрисовка интерфейса (счет, скорость)"""
        score_text = self.font_medium.render(f"Счет: {self.score}", True, WHITE)
        speed_text = self.font_small.render(f"Скорость: {self.speed}", True, WHITE)
        high_score_text = self.font_small.render(f"Рекорд: {self.high_score}", True, YELLOW)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(speed_text, (10, 50))
        self.screen.blit(high_score_text, (10, 75))
    
    def draw_menu(self):
        """Отрисовка главного меню"""
        self.screen.fill(BLACK)
        
        title = self.font_large.render("ЗМЕЙКА", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_medium.render("Snake Game", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(subtitle, subtitle_rect)
        
        instructions = [
            "ПРОБЕЛ - Начать игру",
            "Стрелки - Управление",
            "ПРОБЕЛ (в игре) - Пауза",
            "ESC - Выход/Меню",
            "",
            f"Лучший результат: {self.high_score}"
        ]
        
        for i, instruction in enumerate(instructions):
            color = YELLOW if "результат" in instruction else WHITE
            text = self.font_small.render(instruction, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 30))
            self.screen.blit(text, text_rect)
    
    def draw_pause(self):
        """Отрисовка экрана паузы"""
        # Полупрозрачный overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render("ПАУЗА", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        continue_text = self.font_medium.render("ПРОБЕЛ - Продолжить", True, WHITE)
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        # Полупрозрачный overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("ИГРА ОКОНЧЕНА", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_medium.render(f"Ваш счет: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        if self.score == self.high_score and self.score > 0:
            new_record = self.font_medium.render("НОВЫЙ РЕКОРД!", True, YELLOW)
            new_record_rect = new_record.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(new_record, new_record_rect)
        
        restart_text = self.font_small.render("ПРОБЕЛ - Играть снова", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_small.render("ESC - Главное меню", True, WHITE)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 95))
        self.screen.blit(menu_text, menu_rect)
    
    def draw(self):
        """Основная функция отрисовки"""
        if self.state == GameState.MENU:
            self.draw_menu()
            
        elif self.state == GameState.PLAYING:
            self.screen.fill(BLACK)
            # self.draw_grid()  # Можно включить для отладки
            self.draw_food()
            self.draw_snake()
            self.draw_hud()
            
        elif self.state == GameState.PAUSED:
            self.screen.fill(BLACK)
            self.draw_food()
            self.draw_snake()
            self.draw_hud()
            self.draw_pause()
            
        elif self.state == GameState.GAME_OVER:
            self.screen.fill(BLACK)
            self.draw_food()
            self.draw_snake()
            self.draw_hud()
            self.draw_game_over()
    
    def run(self):
        """Главный игровой цикл"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update_game()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(self.speed)
        
        pygame.quit()
        sys.exit()

def main():
    """Точка входа в программу"""
    try:
        game = SnakeGame()
        game.run()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
