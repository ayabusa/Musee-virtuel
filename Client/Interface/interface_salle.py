import pygame
import os  # Pour la gestion des chemins compatibles avec tous les systèmes
import api
from api import *
# Initialisation de Pygame
pygame.init()

# Constantes de la fenêtre
pygame.init()

# Constantes de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 1900, 1080
FPS = 60

# Dimensions des carrés et espacement
CARRE_WIDTH = 200
CARRE_HEIGH = 400
CARRE_SPACING = 100
NUM_CARRES = 10
ROOM_WIDTH = NUM_CARRES * (CARRE_WIDTH + CARRE_SPACING) - CARRE_SPACING
ROOM_HEIGHT = SCREEN_HEIGHT

# Thèmes
THEME = [
    "GUERRE",
    "EMOTIONS",
    "NATURE",
    "ABSTRAIT",
    "NOTRE COLLECTION PERSONEL",
    "STREET ART",
    "DIVERS"
]

# Couleurs associées aux thèmes
THEME_STYLES = {
    "GUERRE": (255, 0, 0),
    "EMOTIONS": (255, 165, 0),
    "NATURE": (34, 139, 34),
    "ABSTRAIT": (75, 0, 130),
    "NOTRE COLLECTION PERSONEL": (255, 215, 0),
    "STREET ART": (169, 169, 169),
    "DIVERS": (255, 255, 255)
}

# Dictionnaire pour les images de fond des thèmes
THEME_IMAGES = {
    "GUERRE": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_guerre.png"),
    "EMOTIONS": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_emotion.png"),
    "NATURE": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_nature.png"),
    "ABSTRAIT": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_abstrait.png"),
    "NOTRE COLLECTION PERSONEL": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_art_pla.png"),
    "STREET ART": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_street_art.png"),
    "DIVERS": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_art_pla.png")
}

# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Police pour afficher le thème
font = pygame.font.Font(None, 74)

# Classe Joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Musee-virtuel", "Client", "Interface", "sprite.png")).convert_alpha()  # Charge l'image du joueur
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 300)  # Position plus haute
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x

        # Limiter le déplacement aux bords de la salle
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ROOM_WIDTH:
            self.rect.right = ROOM_WIDTH

# Classe Porte
class Door(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((50, SCREEN_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        if position == "right":
            self.rect.right = ROOM_WIDTH
        elif position == "left":
            self.rect.left = 0

# Classe Camera
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        else:
            return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - SCREEN_WIDTH), x)  # right
        y = max(-(self.height - SCREEN_HEIGHT), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Fonction pour exécuter une salle
def run_room(theme_index):
    running = True
    clock = pygame.time.Clock()

    # Définir le thème et la couleur de la salle
    theme = THEME[theme_index]
    theme_color = THEME_STYLES[theme]

    # Charger l'image de fond associée au thème et la redimensionner à la taille de l'écran
    background_image = pygame.image.load(api.get_tableau_image[2]).convert()
    background_image = pygame.transform.scale(background_image, (ROOM_WIDTH, SCREEN_HEIGHT))

    # Mettre à jour le titre de la fenêtre
    pygame.display.set_caption(f"Salle du {theme}")

    # Initialisation des sprites
    all_sprites = pygame.sprite.Group()
    player = Player()
    door_right = Door("right")
    door_left = Door("left")
    all_sprites.add(player, door_right, door_left)

    # Initialisation de la caméra
    camera = Camera(ROOM_WIDTH, ROOM_HEIGHT)

    # Coordonnées des carrés violets pour les tableaux
    tableau_positions = [
        (x * (CARRE_WIDTH + CARRE_SPACING), SCREEN_HEIGHT // 2 - CARRE_WIDTH // 2)
        for x in range(NUM_CARRES)
    ]

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Gestion des touches
        keys = pygame.key.get_pressed()
        # Vitesse de mouvement à droite et à gauche
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        player.speed_x = dx * 10

        # Mise à jour des sprites
        all_sprites.update()

        # Mise à jour de la caméra
        camera.update(player)

        # Vérification de collision avec les portes
        if pygame.sprite.collide_rect(player, door_right):
            return theme_index + 1
        if pygame.sprite.collide_rect(player, door_left):
            return max(theme_index - 1, 0)

        # Affichage
        screen.blit(background_image, camera.apply(pygame.Rect(0, 0, ROOM_WIDTH, SCREEN_HEIGHT)))  # Afficher l'image de fond décalée par la position de la caméra

        # Affichage des sprites avec la caméra
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        # Affichage des carrés violets
        for pos in tableau_positions:
            pygame.draw.rect(screen, (128, 0, 128), camera.apply(pygame.Rect(pos[0], pos[1], CARRE_WIDTH, CARRE_HEIGH)))

        # Affichage du thème
        theme_text = font.render(theme, True, (0, 0, 0))
        text_rect = theme_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(theme_text, text_rect)

        # le carré s'agrandit quand on passe la souris dessus
        # m_pos = pygame.mouse.get_pos()
        # for pos in tableau_positions:
        #     rect = pygame.Rect(pos[0] - camera_x, pos[1], CARRE_WIDTH, CARRE_WIDTH)
        #     if rect.collidepoint(m_pos):
        #         CARRE_WIDTH = 250

        pygame.display.flip()

# Boucle pour les salles
theme_index = 0
while theme_index < len(THEME):
    theme_index = run_room(theme_index)
    
pygame.quit()