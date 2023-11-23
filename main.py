import pygame
import sys
import random

class Player:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size

    def move(self, dx, dy, terrain_data):
        new_x = self.x + dx
        new_y = self.y + dy
        new_cell_id = f"C{new_x}_{new_y}"
        
        if (terrain_data[new_cell_id]["Forest"] or terrain_data[new_cell_id]["Mountain"] or terrain_data[new_cell_id]["Lake"]):
            print("terraind colsion")
        else:
            update_explored_area(dx, dy)

def generate_initial_view():
    # Generar la vista inicial del mapa alrededor del jugador
    for x in range(player.x - 4, player.x + 5):
        for y in range(player.y - 4, player.y + 5):
            cell_id = f"C{x}_{y}"
            if cell_id not in cell_data:
                generate_cell(x, y)


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
        terrain = "Grass"
    else:
        terrain = random.choice([t for t in terrain_types if t != "Grass"])

    cell_data[cell_id][terrain] = True
    cell_data[cell_id]["Explored"] = True  # Agregar la propiedad "Explored"


# Inicializar Pygame
pygame.init()

# Tamaño de la pantalla y la celda
screen_size = (496, 512)
cell_size = 16

# Posición inicial del jugador en celdas (más hacia el centro)
player = Player(screen_size[0] // (2 * cell_size), screen_size[1] // (2 * cell_size), cell_size)

# Configuración de la pantalla
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Juego de Celdas")

# Colores
green = (0, 255, 0)
dark_green = (0, 100, 0)
white = (255, 255, 255)
black = (0, 0, 0)
brown = (139, 69, 19)
blue = (0, 0, 255)

# Diccionario para almacenar información sobre cada tipo de terreno
terrain_types = ["Mountain", "Lake", "Forest", "Grass"]

# Porcentaje de terreno Grass deseado
grass_percentage = 0.9

# Diccionario para almacenar información sobre cada celda
cell_data = {}

# Generar la vista inicial del mapa
generate_initial_view()

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()
FPS = 60

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

    # Rellenar la pantalla con el color negro
    screen.fill(black)

    # Generar la vista inicial y dibujar celdas exploradas
    generate_initial_view()

    for cell_id, cell_info in cell_data.items():
        x = int(cell_id[1:].split('_')[0])
        y = int(cell_id[1:].split('_')[1])

        if cell_info.get("Explored", False):
            if cell_info["Mountain"]:
                pygame.draw.rect(screen, brown, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif cell_info["Lake"]:
                pygame.draw.rect(screen, blue, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif cell_info["Forest"]:
                pygame.draw.rect(screen, dark_green, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif cell_info["Grass"]:
                pygame.draw.rect(screen, green, (x * cell_size, y * cell_size, cell_size, cell_size))

    # Dibujar jugador blanco en su posición actual
    pygame.draw.rect(screen, white, ((screen_size[0] // (2 * cell_size)) * cell_size, (screen_size[1] // (2 * cell_size)) * cell_size, cell_size, cell_size))

    pygame.display.flip()
