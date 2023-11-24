
import pygame
import sys
import random

# Definir constantes
CELL_SIZE = 16
GRASS_PERCENTAGE = 1

# Colores
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Diccionario para almacenar información sobre cada tipo de terreno
TERRAIN_TYPES = ["Grass"]

# Lista para almacenar chunks
chunks = []

# Diccionario para almacenar información sobre cada celda
cell_data = {}

# Coordenadas del chunk inicial
CHUNK_WIDTH = 8
CHUNK_HEIGHT = 8
INITIAL_CHUNK_X = 12
INITIAL_CHUNK_Y = 12

# Tamaño de la pantalla y la celda
SCREEN_SIZE = (16 * 32, 16 * 32)  # 32x32 chunks * 16x16 cells per chunk


# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()
FPS = 60

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_cell = (16, 16)
        self.current_cell = None

    def move(self, dx, dy):
        if self.start_cell == (16, 16):
            print("La celda es la inicial")
            self.current_cell = (self.start_cell[0] + dx, self.start_cell[1] + dy)
            self.start_cell = None
            print(self.current_cell)
        else:
            self.current_cell = (self.current_cell[0] + dx, self.current_cell[1] + dy)
            print(self.current_cell)
        update_explored_area(dx, dy)


class Chunk:
    # Contador de chunks para asignar IDs únicos
    chunk_counter = 1

    def __init__(self, start_x, start_y, width, height):
        self.id = Chunk.chunk_counter
        Chunk.chunk_counter += 1
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.cells = {}


def update_explored_area(dx, dy):
    move_terrain(-dx, -dy)


def move_terrain(dx, dy):
    # Crear un nuevo diccionario de datos de celdas
    new_cell_data = {}

    for cell_id, cell_info in cell_data.items():
        x = int(cell_id[1:].split('_')[0]) + dx
        y = int(cell_id[1:].split('_')[1]) + dy
        new_cell_id = f"C{x}_{y}"

        # Mover la información de la celda al nuevo diccionario
        new_cell_data[new_cell_id] = cell_info

    # Actualizar el diccionario de datos de celdas con el nuevo diccionario
    cell_data.clear()
    cell_data.update(new_cell_data)


def generate_cell(x, y):
    # Generar información sobre una nueva celda
    cell_id = f"C{x}_{y}"
    cell_data[cell_id] = {terrain: False for terrain in TERRAIN_TYPES}

    # Determinar el tipo de terreno
    if random.random() < GRASS_PERCENTAGE:
        cell_data[cell_id]["Grass"] = True


def generate_chunk(start_x, start_y, width, height):
    # Generar un nuevo chunk
    chunk = Chunk(start_x, start_y, width, height)

    for x in range(start_x, start_x + width):
        for y in range(start_y, start_y + height):
            generate_cell(x, y)
            chunk.cells[f"C{x}_{y}"] = cell_data[f"C{x}_{y}"]

    return chunk


# Inicializar Pygame
pygame.init()

# Posición inicial del jugador en celdas (más hacia el centro)
player = Player(16, 16)

# Configuración de la pantalla
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Juego de Celdas")

# Generar el primer chunk inicial
initial_chunk = generate_chunk(INITIAL_CHUNK_X, INITIAL_CHUNK_Y, CHUNK_WIDTH, CHUNK_HEIGHT)
chunks.append(initial_chunk)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.move(0, -1)
            elif event.key == pygame.K_s:
                player.move(0, 1)
            elif event.key == pygame.K_a:
                player.move(-1, 0)
            elif event.key == pygame.K_d:
                player.move(1, 0)

    # Resto del código para dibujar y actualizar la pantalla
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    # Dibujar celdas exploradas
    for cell_id, cell_info in cell_data.items():
        x = int(cell_id[1:].split('_')[0])
        y = int(cell_id[1:].split('_')[1])

        if cell_info["Grass"]:
            pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Dibujar jugador blanco en su posición actual
    pygame.draw.rect(screen, WHITE, (player.x * CELL_SIZE, player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
