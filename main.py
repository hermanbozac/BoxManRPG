import pygame
import sys
import random
pygame.init()
pygame.display.set_caption("BoxMan RPG Survival")
clock = pygame.time.Clock()
FPS = 60
SCREEN_SIZE = (528, 528)  
CHUNK_WIDTH = 8
CHUNK_HEIGHT = 8
INITIAL_CHUNK_X = 0  
INITIAL_CHUNK_Y = 0
CELL_SIZE = 16
GRASS_PERCENTAGE = 1
CELL_COUNTER = 1
CHUNK_COUNTER = 1
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TERRAIN_TYPES = ["Grass"]
chunks = []
cell_data = {}
#......CLASES.....
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_cell = f"C{x+3}_{y+3}"
        self.current_chunk = 1
    def move(self, dx, dy):
        if self.current_cell == (0, 0):  # primer movimiento
            self.current_cell = f"C{self.current_cell[0] + dx}_{self.current_cell[1] + dy}"
        else:  # el resto de los movimientos
            self.current_cell = f"C{int(self.current_cell[1:].split('_')[0]) + dx}_{int(self.current_cell[1:].split('_')[1]) + dy}" 
            #print("player cell ", player.current_cell,self.current_chunk)      
            for chunk in chunks:
                for cell_id, cell_info in chunk.cells.items():
                    #si salgo del chunk principal solo llega hasta
                    if cell_id == player.current_cell:
                        #ENCUENTRA CELDA DEL PERSONAJE EN DICCIONARIO DE CHUNKS
                        if self.current_chunk == cell_info.get("chunk_id"):
                            #print("MISMO CHUNK")
                            pass
                        else:
                            print
                            self.current_chunk = cell_info.get("chunk_id")
                            print("CAMBIO DE CHUNK: ",self.current_chunk)
                            # Obtener chunks adyacentes al chunk actual del jugador
            update_explored_area(dx, dy,self.current_chunk)

class Chunk:
    def __init__(self, start_x, start_y, width, height,id):
        global CHUNK_COUNTER
        self.id = id
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.cells = {}
    def get_adjacent_chunks(self):
        existing_chunk_coords = [(chunk.start_x, chunk.start_y) for chunk in chunks]
        for chunk in chunks:
            if chunk.id == player.current_chunk:
                adjacent_chunks = []
                # Obtener las coordenadas del chunk actual del jugador
                player_chunk_x, player_chunk_y = chunk.start_x, chunk.start_y
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue  # Saltar el propio chunk
                        neighbor_x = player_chunk_x + dx * CHUNK_WIDTH
                        neighbor_y = player_chunk_y + dy * CHUNK_HEIGHT
                        adjacent_chunks.append((neighbor_x, neighbor_y))
                print("Chunks adyacentes:", adjacent_chunks)

                # Llamar a get_missing_chunks para manejar los chunks faltantes
                missing_chunks = get_missing_chunks(adjacent_chunks, existing_chunk_coords)
                
                # Llamar a spawn_missing_chunks para generar los chunks faltantes
                self.spawn_missing_chunks(missing_chunks)

#.....GENERACION PRIMARIA DEL MUNDO.....
def spawn_first_chunk():
    global chunks
    global cell_data
    global CHUNK_COUNTER

    start_x = INITIAL_CHUNK_X
    start_y = INITIAL_CHUNK_Y
    width = CHUNK_WIDTH
    height = CHUNK_HEIGHT

    # Verificar si el chunk ya existe antes de generarlo nuevamente
    for existing_chunk in chunks:
        if existing_chunk.start_x == start_x and existing_chunk.start_y == start_y:
            return existing_chunk

    # Si no existe, crear un nuevo chunk
    chunk = generate_chunk(start_x, start_y, width, height)
    chunks.append(chunk)

def generate_chunk(start_x, start_y, width, height):
    global CHUNK_COUNTER
    # Generar un nuevo chunk
    print("spawn chunk n ",CHUNK_COUNTER)
    print("player current cell",player.current_cell)
    chunk = Chunk(start_x, start_y, width, height,CHUNK_COUNTER)
    CHUNK_COUNTER += 1
    print("nuevo chunk cordenadas",start_x," ",start_y)
    for x in range(start_x, start_x + width):
        for y in range(start_y, start_y + height):
            generate_cell(x , y , chunk.id)  # Usar coordenadas relativas al chunk
            # Verificar si la celda ya existe en el chunk antes de agregarla
            cell_id = f"C{x}_{y}"
            if cell_id not in chunk.cells:
                # Asegúrate de usar coordenadas relativas al inicio del chunk aquí también
                chunk.cells[cell_id] = cell_data[cell_id]
    return chunk

def generate_cell(x, y, chunk_id):
    global cell_data
    print("x,y que reccive generate cell",x,y)
    # Generar información sobre una nueva celda solo si no existe
    cell_id = f"C{x}_{y}"
    if cell_id not in cell_data:
        cell_data[cell_id] = {terrain: False for terrain in TERRAIN_TYPES}

        # Determinar el tipo de terreno
        if random.random() < GRASS_PERCENTAGE:
            cell_data[cell_id]["Grass"] = True

        # Agregar el chunk_id a la información de la celda
        cell_data[cell_id]["chunk_id"] = chunk_id

def search_neighbor_chunks(center_x, center_y):
    # Obtener el ID del chunk actual
    current_chunk = get_current_chunk(center_x, center_y)
    current_chunk_id = (current_chunk.start_x, current_chunk.start_y)
    print("current_chunk_id",current_chunk_id)

    # Obtener los IDs de los chunks adyacentes al chunk actual
    neighboring_chunk_ids = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue  # Saltar el propio chunk

            neighbor_x = current_chunk.start_x + dx * CHUNK_WIDTH
            neighbor_y = current_chunk.start_y + dy * CHUNK_HEIGHT

            neighboring_chunk_ids.append((neighbor_x, neighbor_y))

    # Filtrar los IDs de los chunks adyacentes para excluir el propio chunk actual
    neighboring_chunk_ids = [chunk_id for chunk_id in neighboring_chunk_ids if chunk_id != current_chunk_id]
    print("funcion search_neighbor_chunks",neighboring_chunk_ids)
    for neighbor_id in neighboring_chunk_ids:
        spawn_neighbors_chunks(neighbor_id[0], neighbor_id[1])

def spawn_neighbors_chunks(center_x, center_y):
    new_chunk = generate_chunk(center_x, center_y, CHUNK_WIDTH, CHUNK_HEIGHT)
    chunks.append(new_chunk)

#.....GETTERS PARA BUSCAR DATOS.........

def get_current_chunk(player_x, player_y):
    for chunk in chunks:
        if chunk.start_x <= player_x < chunk.start_x + chunk.width and \
                chunk.start_y <= player_y < chunk.start_y + chunk.height:
            return chunk
    return None

def get_missing_chunks(adjacent_chunks, existing_chunk_coords):
    missing_chunks = [chunk for chunk in adjacent_chunks if chunk not in existing_chunk_coords]
    print("missing chunks", missing_chunks)
    return missing_chunks

#.......UPDATE DEL MUNDO
def update_explored_area(dx, dy, current_chunk):
    # Llamar a la función move_terrain para actualizar el terreno en el mapa
    move_terrain(dx, dy, current_chunk)

def move_terrain(dx, dy, current_chunk):
    global cell_data

    # Crear un nuevo diccionario de datos de celdas
    new_cell_data = {}

    for cell_id, cell_info in cell_data.items():
        x = int(cell_id[1:].split('_')[0]) + dx  # Cambiado a resta para mover en la dirección opuesta
        y = int(cell_id[1:].split('_')[1]) + dy  # Cambiado a resta para mover en la dirección opuesta
        new_cell_id = f"C{x}_{y}"

        # Mover la información de la celda al nuevo diccionario
        new_cell_data[new_cell_id] = cell_info

    # Actualizar el diccionario de datos de celdas con el nuevo diccionario
    cell_data.clear()
    cell_data.update(new_cell_data)
        



#........INIT GAME.........        
player = Player(0, 0)
screen = pygame.display.set_mode(SCREEN_SIZE)

def bucle_principal(player):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.move(0, 1)
                elif event.key == pygame.K_s:
                    player.move(0, -1)
                elif event.key == pygame.K_a:
                    player.move(1, 0)
                elif event.key == pygame.K_d:
                    player.move(-1, 0)
                elif event.key == pygame.K_ESCAPE:  
                    pygame.quit()
                    sys.exit()

        clock.tick(FPS)
        screen.fill((0, 0, 0))
        # Dibujar celdas exploradas
        for chunk in chunks:
            
            for cell in chunk.cells.items():
                #print("chunk id",chunk.id, " ", cell)
                pass
            for cell_id, cell_info in cell_data.items():
                x = int(cell_id[1:].split('_')[0])
                y = int(cell_id[1:].split('_')[1])

                if cell_info["Grass"]:
                    pygame.draw.rect(screen, GREEN, ((x+12) * CELL_SIZE, (y+12) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Dibujar jugador blanco en su posición actual
        pygame.draw.rect(screen, WHITE, ((16 ) * CELL_SIZE, (16 ) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()

def main():
    spawn_first_chunk()
    search_neighbor_chunks(INITIAL_CHUNK_X, INITIAL_CHUNK_Y)
    bucle_principal(player)
    
if __name__ == "__main__":
    main()
