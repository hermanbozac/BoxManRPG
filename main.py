import pygame
import sys

pygame.init()
pygame.display.set_caption("BoxMan RPG Survival")
clock = pygame.time.Clock()
FPS = 60
SCREEN_SIZE = (528, 528)
CHUNK_WIDTH = 128
CHUNK_HEIGHT = 128
CHUNK_COUTNER = 1
CELL_SIZE = 16
PLAYER_SIZE = 16
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
chunks = []
exist_chunks = [(0, 0), (-128, -128), (-128, 0), (-128, 128), (0, -128), (0, 128), (128, -128), (128, 0), (128, 128)]
neighbor_chunks = []
no_neighbor_chunks = []
missing_chunks =[]
# ...CLASES...
class Player:
    def __init__(self, x, y):#solucionado
        self.x = x
        self.y = y
        self.relative_position_x = x
        self.relative_position_y = y
        self.current_chunk = (self.x,self.y)
    def get_current_chunk(self):
        print("xxxxxxxxxxxxxxx funcion get current chunk leng chunks",len(chunks))
        for chunk in chunks:
            if chunk.is_inside_chunk(self.relative_position_x, self.relative_position_y):
                print("en los chunks encontre las posiciones relativas del jugador")
                print("chunk id",chunk.id)
                self.current_chunk = chunk
                break
            else:
                pass




        
    def get_neighbor_chunks(self):
        global neighbor_chunks
        global exist_chunks
        global no_neighbor_chunks
        neighbor_chunks.clear()  # Limpiar la lista antes de agregar nuevos elementos
        # Obtener los IDs de los chunks adyacentes al chunk actual
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue  # Saltar el propio chunk
                neighbor_x = self.current_chunk.start_x + dx * CHUNK_WIDTH
                neighbor_y = self.current_chunk.start_y + dy * CHUNK_HEIGHT
                neighbor_chunks.append((neighbor_x, neighbor_y))
        for neighbor in neighbor_chunks:
            if neighbor in exist_chunks:
                pass
            else:
                exist_chunks.append(neighbor)
    def get_non_neighbor_chunks(self):
        global neighbor_chunks
        global no_neighbor_chunks
        global exist_chunks

        # Encontrar los chunks que no son vecinos
        current_chunk_coord = (self.current_chunk.position[0], self.current_chunk.position[1])
        no_neighbor_chunks.clear()
        
        for chunk in exist_chunks:
            if chunk in neighbor_chunks:
                pass
            else:
                if chunk == current_chunk_coord:
                    pass
                else:
                    no_neighbor_chunks.append(chunk)
    def remove_non_neighbor_chunks(self,direction):
        global chunks
        global exist_chunks
        global no_neighbor_chunks
        global neighbor_chunks
        chunks_to_remove = []
        player_chunk_position = (self.current_chunk.position[0], self.current_chunk.position[1])
        for chunk_position in no_neighbor_chunks:
            if chunk_position not in neighbor_chunks:
                if chunk_position == player_chunk_position:
                    pass
                else:
                    # Buscar el fragmento correspondiente en la lista de chunks
                    #encontrar valores relativos para adicionar en cada  direcion
                    compensation_x = 0
                    compensation_y = 0
                    if direction == (0, 16):
                        compensation_y = -0
                    elif direction == (0, -16):
                        compensation_y = 0
                    elif direction == (16, 0):
                        compensation_x = -0
                    elif direction == (-16, 0):
                        compensation_x = 0

                    chunk_to_remove = next((chunk for chunk in chunks if (chunk.start_x +  compensation_x, chunk.start_y + compensation_y) == chunk_position), None)
                    if chunk_to_remove:
                        chunks_to_remove.append(chunk_to_remove)
                    else:
                        pass
        for chunk in chunks_to_remove:
            print("chunk id ",chunk.id)
            chunk_position = (chunk.start_x, chunk.start_y)
            chunks.remove(chunk)
            exist_chunks.remove(chunk_position)

    def get_missing_chunks(self):
        global neighbor_chunks
        global missing_chunks
        global exist_chunks
        global no_neighbor_chunks

        
        player_chunk_position = (self.current_chunk.position[0], self.current_chunk.position[1])
        aux_nueve_chunks = neighbor_chunks
        aux_nueve_chunks.append(player_chunk_position)
        exist_chunks = []
        for chunk in chunks:
            chunk_position = (chunk.start_x,chunk.start_y)
            exist_chunks.append(chunk_position)
        for chunk in aux_nueve_chunks:
            for exist in exist_chunks:
                if exist in aux_nueve_chunks:
                    pass
                else:
                    missing_chunks.append(exist)

                    
            break
    def spawn_missing_chunks(self,direction):
        global missing_chunks
        compensation_x = 0
        compensation_y = 0
        if direction == (0, 16):
            compensation_x = self.relative_position_x
            compensation_y -= 0
            self.calculating(compensation_x,compensation_y)
        elif direction == (0, -16):
            compensation_x = self.relative_position_x
            compensation_y += 112
            self.calculating(compensation_x,compensation_y)
        elif direction == (16, 0):
            compensation_x = 0
            compensation_y += self.relative_position_y
            self.calculating(compensation_x,compensation_y)
        elif direction == (-16, 0):
            compensation_x = 112
            compensation_y += self.relative_position_y
            self.calculating(compensation_x,compensation_y)
    def calculating(self,compensation_x,compensation_y):
        global CHUNK_COUTNER
        for positions in missing_chunks:
            width = CHUNK_WIDTH
            height = CHUNK_HEIGHT
            chunk = generate_chunk(positions[0]+compensation_x, positions[1] + compensation_y, width, height,CHUNK_COUTNER)
            chunks.append(chunk)
            CHUNK_COUTNER += 1    
    def move(self, direction):
        if direction == (0, 16):
            
            for chunk in chunks:
                chunk.mobile_y += CELL_SIZE
            self.relative_position_y += CELL_SIZE
            self.aux(direction)
        elif direction == (0, -16):
            
            for chunk in chunks:
                chunk.mobile_y -= CELL_SIZE
            self.relative_position_y -= CELL_SIZE
            self.aux(direction)
        elif direction == (16, 0):
            for chunk in chunks:
                chunk.mobile_x += CELL_SIZE
            self.relative_position_x += CELL_SIZE
            self.aux(direction)
        elif direction == (-16, 0):
            
            for chunk in chunks:
                chunk.mobile_x -= CELL_SIZE
            self.relative_position_x -= CELL_SIZE
            self.aux(direction)
        else:
            return        

    def aux(self, direction):
        global no_neighbor_chunks
        global missing_chunks
        global exist_chunks
        global no_neighbor_chunks
        global neighbor_chunks
        aux_chunk = self.current_chunk
        
        self.get_current_chunk()
        for chunk in chunks:
            if chunk.id == self.current_chunk.id:
                print("chunk object id = self current chunk id",chunk.id)
                chunk = self.current_chunk

    
                print("CAMBIE AL CHUNK ID:", self.current_chunk.id)
                no_neighbor_chunks = []
                missing_chunks = []
                exist_chunks = []
                neighbor_chunks = []
                for chunk in chunks:
                    chunk_position = (chunk.start_x, chunk.start_y)
                    exist_chunks.append(chunk_position)

                self.get_neighbor_chunks()
                self.get_non_neighbor_chunks()
                self.remove_non_neighbor_chunks(direction)
                self.get_missing_chunks()
                self.spawn_missing_chunks(direction)
            else:
                pass




    def get_draw_position(self, screen_width, screen_height): #esto esta ok
        # Calcular la posición de dibujo alineada con la cuadrícula del chunk y centrada en la pantalla
        draw_x = (screen_width // 2 - PLAYER_SIZE // 2 + self.x * CELL_SIZE - CHUNK_WIDTH // 2) % CHUNK_WIDTH
        draw_y = (screen_height // 2 - PLAYER_SIZE // 2 + self.y * CELL_SIZE - CHUNK_HEIGHT // 2) % CHUNK_HEIGHT
        return draw_x, draw_y
    def is_inside_current_chunk(self, chunk): #funciona ok
        """
        Verifica si la posición actual del jugador está dentro del chunk proporcionado.
        """
        if chunk is not None:
            return chunk.is_inside_chunk(self.relative_position_x, self.relative_position_y)
        else:
            return False

class Chunk:
    def __init__(self, start_x, start_y, width, height,id):
        self.start_x = start_x
        self.start_y = start_y
        self.mobile_x = start_x  # Variable para rastrear la posición móvil x
        self.mobile_y = start_y  # Variable para rastrear la posición móvil y
        self.width = width
        self.height = height
        self.position = (self.start_x,self.start_y)
        self.id = id

    def is_inside_chunk(self, x, y):
        """
        Verifica si las coordenadas (x, y) están dentro de los límites del chunk.
        """

        inside_limits_x = self.start_x <= x < self.start_x + self.width
        inside_limits_y = self.start_y <= y < self.start_y + self.height

  

        return inside_limits_x and inside_limits_y



# ...GENERADORES COMUNES...
def generate_chunk(start_x, start_y, width, height,id):
    
    return Chunk(start_x, start_y, width, height,id)

# ...GENERACION PRIMARIA DEL MUNDO...
def spawn_first_chunk(player):
    global CHUNK_COUTNER
    start_x = player.x
    start_y = player.y
    width = CHUNK_WIDTH
    height = CHUNK_HEIGHT

    chunk = generate_chunk(start_x, start_y, width, height,CHUNK_COUTNER)
    chunks.append(chunk)
    CHUNK_COUTNER += 1

def spawn_first_neighboring_chunks(player,faltant_chunks):
    global CHUNK_COUTNER
    global chunks
    width = CHUNK_WIDTH
    height = CHUNK_HEIGHT

    # Generar los chunks faltantes
    for chunk_coords in faltant_chunks:
        start_x = chunk_coords[0]
        start_y = chunk_coords[1]
        chunk = generate_chunk(start_x, start_y, width, height,CHUNK_COUTNER)
        chunks.append(chunk)
        CHUNK_COUTNER += 1
     
######START GAME#####

def main():
    player = Player(0, 0)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    spawn_first_chunk(player)
    player.get_current_chunk()
    player.get_neighbor_chunks()
    spawn_first_neighboring_chunks(player,neighbor_chunks)



    bucle_principal(player, screen)

def bucle_principal(player, screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    direction= (0,+16)
                    player.move(direction)
                elif event.key == pygame.K_s:
                    direction= (0,-16)
                    player.move(direction)
                elif event.key == pygame.K_a:
                    direction= (+16,0)
                    player.move(direction)
                elif event.key == pygame.K_d:
                    direction= (-16,0)
                    player.move(direction)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        # Dibujar los chunks con las coordenadas ajustadas por el movimiento del mapa
        for chunk in chunks:
            pygame.draw.rect(screen, GREEN, (chunk.mobile_x+160, chunk.mobile_y+160, chunk.width, chunk.height), 8)

        # Dibujar jugador blanco en su posición actual alineada con la cuadrícula del chunk y centrada en la pantalla
        draw_x, draw_y = player.get_draw_position(SCREEN_SIZE[0], SCREEN_SIZE[1])
        pygame.draw.rect(screen, WHITE, (draw_x+208, draw_y+208, PLAYER_SIZE, PLAYER_SIZE))

        pygame.display.flip()        

if __name__ == "__main__":
    main()

