import pygame
import sys
import random
# Inicializar Pygame
pygame.init()


pygame.display.set_caption("BoxMan RPG Survival")

# Ruta de la imagen PNG
image_path = "Background.png"

# Cargar la imagen y obtener su rectángulo
background_image = pygame.image.load(image_path)
background_rect = background_image.get_rect()

# Definir constantes
CELL_SIZE = 16
GRASS_PERCENTAGE = 1

# Contadores globales para celdas y chunks
CELL_COUNTER = 1
CHUNK_COUNTER = 1


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
SCREEN_SIZE = (512, 512)  # 32x32 chunks * 16x16 cells per chunk

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()
FPS = 60

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_cell = f"C{x}_{y}"
        self.current_chunk = 1

    def move(self, dx, dy):
        if self.current_cell == (16, 16):  # primer movimiento
            self.current_cell = f"C{self.current_cell[0] + dx}_{self.current_cell[1] + dy}"
        else:  # el resto de los movimientos
            self.current_cell = f"C{int(self.current_cell[1:].split('_')[0]) + dx}_{int(self.current_cell[1:].split('_')[1]) + dy}" 
            print("player cell ", player.current_cell)      
            for chunk in chunks:
                for cell_id, cell_info in chunk.cells.items():
                    if cell_id == player.current_cell:
                        print("la celda en la que está el jugador es ", cell_id)
                        print("El chunk_id correspondiente es ", cell_info.get("chunk_id", "No chunk_id"))






            update_explored_area(dx, dy)


class Chunk:
    def __init__(self, start_x, start_y, width, height):
        global CHUNK_COUNTER
        self.id = CHUNK_COUNTER
        CHUNK_COUNTER += 1
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.cells = {}



# Posición inicial del jugador en celdas (más hacia el centro)
player = Player(16, 16)

# Configuración de la pantalla
screen = pygame.display.set_mode(SCREEN_SIZE)


# Función para obtener el chunk actual basado en las coordenadas del jugador
def get_current_chunk(player_x, player_y):
    for chunk in chunks:
        if chunk.start_x <= player_x < chunk.start_x + chunk.width and \
                chunk.start_y <= player_y < chunk.start_y + chunk.height:
            return chunk

    # Si el jugador no está en ningún chunk existente, puedes manejarlo de la manera que desees
    return None

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

def generate_cell(x, y,chunk_id):
    # Generar información sobre una nueva celda
    cell_id = f"C{x}_{y}"

    # Verificar si la celda ya existe antes de generarla nuevamente
    if cell_id not in cell_data:
        cell_data[cell_id] = {terrain: False for terrain in TERRAIN_TYPES}

        # Determinar el tipo de terreno
        if random.random() < GRASS_PERCENTAGE:
            cell_data[cell_id]["Grass"] = True
        # Agregar el chunk_id a la información de la celda
        cell_data[cell_id]["chunk_id"] = chunk_id

def generate_chunk(start_x, start_y, width, height):
    # Generar un nuevo chunk
    chunk = Chunk(start_x, start_y, width, height)

    for x in range(start_x, start_x + width):
        for y in range(start_y, start_y + height):
            generate_cell(x, y, chunk.id)

            # Verificar si la celda ya existe en el chunk antes de agregarla
            cell_id = f"C{x}_{y}"
            if cell_id not in chunk.cells:
                chunk.cells[cell_id] = cell_data[cell_id]

    return chunk




def spawn_chunks(center_x, center_y):
    # Instanciar los 8 chunks relativos al chunk actual
    spawn_relative_chunk(center_x - 8, center_y - 8)  # Noroeste
    spawn_relative_chunk(center_x, center_y - 8)      # Norte
    spawn_relative_chunk(center_x + 8, center_y - 8)  # Noreste
    spawn_relative_chunk(center_x - 8, center_y)      # Oeste
    spawn_relative_chunk(center_x + 8, center_y)      # Este
    spawn_relative_chunk(center_x - 8, center_y + 8)  # Suroeste
    spawn_relative_chunk(center_x, center_y + 8)      # Sur
    spawn_relative_chunk(center_x + 8, center_y + 8)  # Sureste

def spawn_relative_chunk(center_x, center_y):
    new_chunk = generate_chunk(center_x, center_y, CHUNK_WIDTH, CHUNK_HEIGHT)
    chunks.append(new_chunk)


def generar_anillo_externo(center_x, center_y):
    return
    # Generar un anillo externo de 5x5 de nuevos chunks alrededor de las coordenadas proporcionadas
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if abs(dx) <= 1 and abs(dy) <= 1:
                continue  # Salta los 9 chunks del medio

            nuevo_x = center_x + dx * CHUNK_WIDTH
            nuevo_y = center_y + dy * CHUNK_HEIGHT

            # Verificar si el nuevo chunk ya existe antes de generarlo nuevamente
            chunk_existente = next((chunk for chunk in chunks if chunk.start_x == nuevo_x and chunk.start_y == nuevo_y), None)

            if chunk_existente is None:
                nuevo_chunk = generate_chunk(nuevo_x, nuevo_y, CHUNK_WIDTH, CHUNK_HEIGHT)
                chunks.append(nuevo_chunk)

def generar_anillo_n_2(center_x, center_y):
    return
    # Generar un anillo N+2 de 7x7 de nuevos chunks alrededor de las coordenadas proporcionadas
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if abs(dx) <= 2 and abs(dy) <= 2:
                continue  # Salta los 25 chunks del anillo N de 5x5

            nuevo_x = center_x + dx * CHUNK_WIDTH
            nuevo_y = center_y + dy * CHUNK_HEIGHT

            # Verificar si el nuevo chunk ya existe antes de generarlo nuevamente
            chunk_existente = next((chunk for chunk in chunks if chunk.start_x == nuevo_x and chunk.start_y == nuevo_y), None)

            if chunk_existente is None:
                nuevo_chunk = generate_chunk(nuevo_x, nuevo_y, CHUNK_WIDTH, CHUNK_HEIGHT)
                chunks.append(nuevo_chunk)


def bucle_principal(player, current_chunk):
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
        pygame.draw.rect(screen, WHITE, ((player.x - 0.5) * CELL_SIZE, (player.y - 0.5) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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
                    iniciar_juego_desde_pantalla_inicio(player)
                elif event.key == pygame.K_ESCAPE:  # Tecla Escape
                    pygame.quit()
                    sys.exit()

        if mostrando_pantalla_inicio:
            mostrar_pantalla_inicio(screen)
        elif generando_mundo:
            bucle_principal(player, screen)

def iniciar_juego_desde_pantalla_inicio(player):
    # Generar el primer chunk inicial
    initial_chunk = generate_chunk(INITIAL_CHUNK_X, INITIAL_CHUNK_Y, CHUNK_WIDTH, CHUNK_HEIGHT)
    chunks.append(initial_chunk)

    # Definir el chunk actual al primer chunk generado
    current_chunk = initial_chunk

    # Spawn de los chunks relativos al chunk actual
    spawn_chunks(INITIAL_CHUNK_X, INITIAL_CHUNK_Y)


    # Llamada para generar el anillo externo alrededor del chunk inicial
    generar_anillo_externo(INITIAL_CHUNK_X, INITIAL_CHUNK_Y)

    # Llamada para generar el anillo N+2 alrededor del chunk inicial
    generar_anillo_n_2(INITIAL_CHUNK_X, INITIAL_CHUNK_Y)

    # Iniciar el bucle principal
    bucle_principal(player, current_chunk)










if __name__ == "__main__":
    main()
