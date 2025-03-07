import pygame
import os  # Pour la gestion des chemins compatibles avec tous les systèmes
 
# Initialisation de Pygame
pygame.init()
 
# Constantes de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 1900, 1080
ROOM_WIDTH, ROOM_HEIGHT = 3800, 1080  # Dimensions de la salle plus grandes que l'écran
FPS = 60
CARRE_WIDTH = 200
CARRE_HEIGH = 400
NUM_CARRES = 10
CARRE_SPACING = 100
ROOM_WIDTH = NUM_CARRES * (CARRE_WIDTH + CARRE_SPACING) - CARRE_SPACING
ROOM_HEIGH = SCREEN_HEIGHT
 
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
    "NOTRE COLLECTION PERSONEL": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_art_plastique.png"),
    "STREET ART": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_street_art.png"),
    "DIVERS": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_art_plastique.png")
}
 
# Dictionnaire pour les tableaux
TABLEAUX = [
    {"titre": "Tableau 1", "auteur": "Auteur 1", "bio": "Biographie 1"},
    {"titre": "Tableau 2", "auteur": "Auteur 2", "bio": "Biographie 2"},
    {"titre": "Tableau 3", "auteur": "Auteur 3", "bio": "Biographie 3"},
    {"titre": "Tableau 4", "auteur": "Auteur 4", "bio": "Biographie 4"},
    {"titre": "Tableau 5", "auteur": "Auteur 5", "bio": "Biographie 5"},
    {"titre": "Tableau 6", "auteur": "Auteur 6", "bio": "Biographie 6"},
    {"titre": "Tableau 7", "auteur": "Auteur 7", "bio": "Biographie 7"},
    {"titre": "Tableau 8", "auteur": "Auteur 8", "bio": "Biographie 8"},
    {"titre": "Tableau 9", "auteur": "Auteur 9", "bio": "Biographie 9"},
    {"titre": "Tableau 10", "auteur": "Auteur 10", "bio": "Biographie 10"}
]
 
# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
 
# Police pour afficher le thème
font = pygame.font.Font(None, 74)
text_font = pygame.font.Font(None, 36)
 
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
    background_image = pygame.image.load(THEME_IMAGES[theme]).convert()
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
 
    selected_tableau = None
 
    while running:
        clock.tick(FPS)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Ajuster les coordonnées de la souris en fonction de la position de la caméra
                adjusted_mouse_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
                if selected_tableau is not None:
                    # Vérifier si la croix noire est cliquée
                    if 1750 <= mouse_pos[0] <= 1800 and 0 <= mouse_pos[1] <= 50:
                        selected_tableau = None
                else:
                    for i, pos in enumerate(tableau_positions):
                        rect = pygame.Rect(pos[0], pos[1], CARRE_WIDTH, CARRE_HEIGH)
                        if rect.collidepoint(adjusted_mouse_pos):
                            selected_tableau = i
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    selected_tableau = None
 
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
 
        if selected_tableau is not None:
            # Afficher le fond blanc
            pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
 
            # Afficher le tableau sélectionné agrandi
            new_pos = (SCREEN_WIDTH // 4 - CARRE_WIDTH // 2, SCREEN_HEIGHT // 2 - CARRE_HEIGH // 2)
            pygame.draw.rect(screen, (128, 0, 128), pygame.Rect(new_pos[0], new_pos[1], CARRE_WIDTH * 1.5, CARRE_HEIGH * 1.5))
 
            # Afficher le texte associé au tableau sélectionné
            tableau = TABLEAUX[selected_tableau]
            text_lines = [
                f"Titre: {tableau['titre']}",
                f"Auteur: {tableau['auteur']}",
                f"Biographie: {tableau['bio']}"
            ]
            for j, line in enumerate(text_lines):
                text_surface = text_font.render(line, True, (0, 0, 0))
                screen.blit(text_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + j * 40))
 
            # Afficher la croix noire en haut à droite
            pygame.draw.line(screen, (0, 0, 0), (1750, 0), (1800, 50), 5)
            pygame.draw.line(screen, (0, 0, 0), (1800, 0), (1750, 50), 5)
        else:
            # Affichage des carrés violets
            for i, pos in enumerate(tableau_positions):
                pygame.draw.rect(screen, (128, 0, 128), camera.apply(pygame.Rect(pos[0], pos[1], CARRE_WIDTH, CARRE_HEIGH)))
 
            # Affichage des sprites avec la caméra
            for sprite in all_sprites:
                screen.blit(sprite.image, camera.apply(sprite))
 
            # Affichage du thème
            theme_text = font.render(theme, True, (0, 0, 0))
            text_rect = theme_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(theme_text, text_rect)
 
        pygame.display.flip()
 
# Boucle pour les salles
theme_index = 0
while theme_index < len(THEME):
    theme_index = run_room(theme_index)
    
pygame.quit()