from random import randint

import pygame as pg

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (83, 83, 83)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10

screen = pg.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    0,
    32
)
screen.fill(BOARD_BACKGROUND_COLOR)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, bg_color=None) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = bg_color

    def draw(self):
        """Абстрактный метод.

        Который предназначен для переопределения в дочерних классах.
        """
        raise NotImplementedError(f'Определите Draw {type(self).__name__}')

    def draw_cell(self, position, color=None):
        """Отрисовывает одну ячейку."""
        if color is None:
            color = self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, унаследованный от GameObject, описывающий яблоко.

    Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def __init__(self, occupied_positions=[0], bg_color=APPLE_COLOR) -> None:
        super().__init__(bg_color)
        self.position = self.randomize_position(occupied_positions)

    def randomize_position(self, forbidden_positions):
        """Устанавливает случайное положение яблока на игровом поле.

        Избегает позиции, которые уже заняты.
        """
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in forbidden_positions:
                return position

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс Snake, наследуется от GameObject.

    Атрибуты и методы класса обеспечивают логику движения,
    отрисовку, обработку событий (нажата клавиша) и другие
    аспекты поведения змейки в игре.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(bg_color=body_color)
        self.reset()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        self.draw_cell(self.get_head_position(), self.body_color)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        # Проверяем, что новое направление не обратное текущему
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def reset(self):
        """Сбрасывает игру в исходное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки.

        Первый элемент в списке positions.
        """
        return self.positions[0]

    def move(self, apple):
        """Обновляет позицию змейки.

        Координаты каждой секции, добавляя новую голову в начало
        списка positions и удаляя последний элемент, если длина
        змейки не увеличилась.
        """
        self.positions.insert(
            0,
            (
                (
                    self.positions[0][0] + (GRID_SIZE * self.direction[0])
                ) % SCREEN_WIDTH,
                (
                    self.positions[0][1] + (GRID_SIZE * self.direction[1])
                ) % SCREEN_HEIGHT)
        )
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            # Если длина змейки не увеличилась, очищаем значение
            self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT:
                game_object.update_direction(RIGHT)


def main():
    """Здесь находится основной цикл игры."""
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction(snake.direction)
        snake.move(apple)
        pg.display.update()
        apple.draw()
        snake.draw()

        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.last)
            apple.position = apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()


if __name__ == '__main__':
    main()
