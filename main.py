import pygame
import sys
import random
# Ruta de la imagen PNG
image_path = "Background.png"
# Cargar la imagen y obtener su rectángulo
background_image = pygame.image.load(image_path)
background_rect = background_image.get_rect()

# Definir constantes
CELL_SIZE = 16
GRASS_PERCENTAGE = 1

# Colores
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Colores adicionales
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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
        if self.start_cell == (16, 16):  # primer movimiento
            self.current_cell = (self.start_cell[0] + dx, self.start_cell[1] + dy)
            self.start_cell = None
        else:  # el resto de los movimientos
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

def inicializar_juego():
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

    return player, screen

def bucle_principal(player, screen):
    # Bucle principal del juego
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
                elif event.key == pygame.K_RETURN:  # Tecla Enter
                    return
                elif event.key == pygame.K_ESCAPE:  # Tecla Escape
                    pygame.quit()
                    sys.exit()

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

def mostrar_pantalla_inicio(screen):
        # Dibujar la imagen de fondo
    screen.blit(background_image, background_rect)
    font = pygame.font.Font(None, 48)

    start_text = font.render("Start", True, RED)
    enter_text = font.render("ENTER", True, WHITE)  # Nuevo texto para la tecla Enter
    esc_text = font.render("ESC", True, WHITE)  # Nuevo texto para el layer de la tecla ESC

    start_rect = start_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 50))
    enter_rect = enter_text.get_rect(center=start_rect.center)  # Centra el texto "Enter" sobre el botón "Start"
    quit_rect = esc_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 50))
    esc_rect = esc_text.get_rect(center=quit_rect.center)  # Centra el texto "ESC" sobre el botón "Quit"

    # Agranda el botón "Start"
    start_rect.inflate_ip(48, 16)
    # Agranda el botón "Quit"
    quit_rect.inflate_ip(48, 16)

    pygame.draw.rect(screen, RED, start_rect)
    pygame.draw.rect(screen, RED, quit_rect)

 

    # Dibujar la capa de texto "Enter"
    screen.blit(enter_text, enter_rect)

    # Dibujar la capa de texto "ESC"
    screen.blit(esc_text, esc_rect)

    pygame.display.flip()




def main():
    player, screen = inicializar_juego()

    mostrando_pantalla_inicio = True
    generando_mundo = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and mostrando_pantalla_inicio:
                if event.key == pygame.K_RETURN:  # Tecla Enter
                    mostrando_pantalla_inicio = False
                    generando_mundo = True
                elif event.key == pygame.K_ESCAPE:  # Tecla Escape
                    pygame.quit()
                    sys.exit()

        if mostrando_pantalla_inicio:
            mostrar_pantalla_inicio(screen)
        elif generando_mundo:
            bucle_principal(player, screen)

if __name__ == "__main__":
    main()
