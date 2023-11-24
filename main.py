import pygame
import sys
import random



# Porcentaje de terreno Grass deseado
grass_percentage = 1

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()
FPS = 60


# Colores
green = (0, 255, 0)
white = (255, 255, 255)

# Diccionario para almacenar información sobre cada tipo de terreno
terrain_types = ["Grass"]

# Lista para almacenar chunks
chunks = []

# Diccionario para almacenar información sobre cada celda
cell_data = {}

# Coordenadas del chunk inicial
chunk_width = 32  
chunk_height = 32
initial_chunk_x = 0  # Por ejemplo, en el centro del mapa
initial_chunk_y = 0  # Por ejemplo, en el centro del mapa

# Tamaño de la pantalla y la celda
screen_size = (16 * 32, 16 * 32)  # 32x32 chunks * 16x16 cells per chunk
cell_size = 16

class Player:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.current_chunk = None  # Mantén un registro del chunk actual del jugador

    def move(self, dx, dy, terrain_data):
        new_x = self.x + dx
        new_y = self.y + dy
        new_cell_id = f"C{new_x}_{new_y}"

        # Verificar si ha cambiado de chunk
        new_chunk_x = new_x // chunk_width
        new_chunk_y = new_y // chunk_height
        if self.current_chunk is None or (new_chunk_x, new_chunk_y) != (self.current_chunk.start_x // chunk_width, self.current_chunk.start_y // chunk_height):
            self.current_chunk = find_chunk_at(new_x, new_y)

        update_explored_area(dx, dy)

class Chunk:
    def __init__(self, start_x, start_y, width, height):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.cells = {}

def update_explored_area(dx, dy):
    # Actualizar el área explorada alrededor del jugador
    for x in range(player.x - 4, player.x + 5):
        for y in range(player.y - 4, player.y + 5):
            cell_id = f"C{x}_{y}"
            if cell_id not in cell_data:
                generate_cell(x, y)

    # Mover el mapa en la dirección opuesta al movimiento del jugador
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
    cell_data[cell_id] = {terrain: False for terrain in terrain_types}

    # Determinar el tipo de terreno
    if random.random() < grass_percentage:
        cell_data[cell_id]["Grass"] = True

def generate_chunk(start_x, start_y, width, height):
    # Generar un nuevo chunk
    chunk = Chunk(start_x, start_y, width, height)

    for x in range(start_x, start_x + width):
        for y in range(start_y, start_y + height):
            generate_cell(x, y)
            chunk.cells[f"C{x}_{y}"] = cell_data[f"C{x}_{y}"]

    return chunk

def find_chunk_at(x, y):
    # Buscar el chunk que contiene la posición (x, y)
    for chunk in chunks:
        if chunk.start_x <= x < chunk.start_x + chunk.width * cell_size and chunk.start_y <= y < chunk.start_y + chunk.height * cell_size:
            return chunk
    return None


# Función para generar chunks al norte, sur, este, oeste y diagonales del chunk inicial
def generate_surrounding_chunks(initial_chunk):
    chunks = []
    
    # Coordenadas de los chunks adyacentes y diagonales
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for dx, dy in directions:
        start_x = initial_chunk.start_x + dx * initial_chunk.width
        start_y = initial_chunk.start_y + dy * initial_chunk.height
        chunk = generate_chunk(start_x, start_y, initial_chunk.width, initial_chunk.height)
        chunks.append(chunk)

    return chunks

# Inicializar Pygame
pygame.init()



# Posición inicial del jugador en celdas (más hacia el centro)
player = Player(16, 16, cell_size)  # Start at the center of the initial chunk

# Configuración de la pantalla
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Juego de Celdas")


# Generar el primer chunk inicial
initial_chunk = generate_chunk(initial_chunk_x, initial_chunk_y, chunk_width, chunk_height)
chunks.append(initial_chunk)

# Generar chunks alrededor del chunk inicial
surrounding_chunks = generate_surrounding_chunks(initial_chunk)
chunks.extend(surrounding_chunks)



while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.move(0, -1, cell_data)
            elif event.key == pygame.K_s:
                player.move(0, 1, cell_data)
            elif event.key == pygame.K_a:
                player.move(-1, 0, cell_data)
            elif event.key == pygame.K_d:
                player.move(1, 0, cell_data)
    # Mostrar en qué chunk se encuentra el jugador
    if player.current_chunk:
        print(f"Player is in chunk ({player.current_chunk.start_x // chunk_width}, {player.current_chunk.start_y // chunk_height})")

    # Rellenar la pantalla con el color negro
    screen.fill((0, 0, 0))

    # Dibujar celdas exploradas
    for cell_id, cell_info in cell_data.items():
        x = int(cell_id[1:].split('_')[0])
        y = int(cell_id[1:].split('_')[1])

        if cell_info["Grass"]:
            pygame.draw.rect(screen, green, (x * cell_size, y * cell_size, cell_size, cell_size))

    # Dibujar jugador blanco en su posición actual
    pygame.draw.rect(screen, white, (player.x * cell_size, player.y * cell_size, cell_size, cell_size))

    pygame.display.flip()
