import pygame
import os
import api 

# Initialisation de Pygame
pygame.init()

# Constantes de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080  # Dimensions de l'écran
ROOM_WIDTH, ROOM_HEIGHT = 3800, SCREEN_HEIGHT  # Dimensions de la salle plus grandes que l'écran
FPS = 60
CARRE_WIDTH = 200
CARRE_HEIGH = 400
CARRE_SPACING = 100
THEME = api.get_couloir_liste()

THEME_IMAGES = {
    "guerre": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_guerre.png"),
    "abstrait": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_abstrait.png"),
    "arts plastiques": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_art_plastique.png"),
    "emotion": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_emotion.png"),
    "nature": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_nature.png"),
    "street art": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_street_art.png"),
}

# Obtenir la liste des couloirs
couloirs = api.get_couloir_liste()
if couloirs is None:
    print("Erreur lors de la récupération des couloirs")
    exit()

# Choisir un couloir (par exemple, le premier couloir)
couloir_id = list(couloirs.keys())[0]

# Obtenir les tableaux du couloir choisi
tableaux = api.get_tableaux_from_couloir_id(couloir_id)
if tableaux is None:
    print("Erreur lors de la récupération des tableaux")
    exit()

# Calculer la largeur de la salle en fonction du nombre de tableaux
NUM_CARRES = len(tableaux)
ROOM_WIDTH = NUM_CARRES * (CARRE_WIDTH + CARRE_SPACING) - CARRE_SPACING

# Initialisation de l'écran en mode plein écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

# Police pour afficher le thème
font = pygame.font.Font(None, 74)
text_font = pygame.font.Font(None, 36)

# Charger les images des tableaux
tableau_images = {}
for tableau_id in tableaux:
    tableau_images[tableau_id] = api.get_tableau_image(tableau_id)

# Classe Joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
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

    # Coordonnées des tableaux
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
                        if i == 0 or i == len(tableau_positions) - 1:
                            continue  # Ignorer le premier et le dernier tableau
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
            tableau = tableaux[selected_tableau]
            text_lines = [
                f"Titre: {tableau['nom']}",
                f"Auteur: {tableau['auteur']}",
                f"Description: {tableau['description']}"
            ]
            for j, line in enumerate(text_lines):
                text_surface = text_font.render(line, True, (0, 0, 0))
                screen.blit(text_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + j * 40))

            # Afficher la croix noire en haut à droite
            pygame.draw.line(screen, (0, 0, 0), (1750, 0), (1800, 50), 5)
            pygame.draw.line(screen, (0, 0, 0), (1800, 0), (1750, 50), 5)
        else:
            # Affichage des images des tableaux
            for i, pos in enumerate(tableau_positions):
                if i == 0 or i == len(tableau_positions) - 1:
                    continue  # Ignorer le premier et le dernier tableau
                screen.blit(tableau_images[i + 1], camera.apply(pygame.Rect(pos[0], pos[1], CARRE_WIDTH, CARRE_HEIGH)))

            # Affichage des sprites avec la caméra
            for sprite in all_sprites:
                screen.blit(sprite.image, camera.apply(sprite))

            # Affichage du thème
            theme_text = font.render(theme, True, (0, 0, 0))
            text_rect = theme_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(theme_text, text_rect)

        pygame.display.flip()

# Boucle pour les salles
theme_index = 1
while True:
    theme_index = run_room(theme_index)
    if theme_index >= len(THEME):
        theme_index = 1

print("Toutes les salles ont été terminées!")
pygame.quit()