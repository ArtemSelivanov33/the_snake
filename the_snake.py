from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет яблока
APPLE_COLOR = (255, 0, 0)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')
# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, bg_color=None) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = bg_color

    def draw(self):
        """
        Абстрактный метод.
        Который предназначен для переопределения в дочерних классах.
        """
        raise NotImplementedError(f'Определите Draw {type(self).__name__}')


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject, описывающий яблоко.
    Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def __init__(self, bg_color=APPLE_COLOR) -> None:
        super().__init__(bg_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, screen):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс Snake, наследуется от GameObject.
    Атрибуты и методы класса обеспечивают логику движения, отрисовку,
    обработку событий (нажата клавиша)
    и другие аспекты поведения змейки в игре.
    """

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def draw(self, screen):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head = self.get_head_position()
        head_rect = pygame.Rect(head, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction

    def reset(self):
        """Сбрасывает игру в исходное состояние."""
        self.__init__()

    def get_head_position(self):
        """
        Возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        # Множители для координат
        multiplier_width, multiplier_hight = self.direction
        coord_width, coord_higth = self.get_head_position()

        # Координаты новой головы
        new_position_x = (coord_width + (GRID_SIZE * multiplier_width))
        new_position_y = (coord_higth + (GRID_SIZE * multiplier_hight))
        new_position = (
            new_position_x % SCREEN_WIDTH,
            new_position_y % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Здесь находится основной цикл игры."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        pygame.display.update()
        handle_keys(snake)
        snake.update_direction()
        apple.draw(screen)
        snake.draw(screen)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.last)
            apple = Apple()
        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()


if __name__ == '__main__':
    main()
