import pygame
import os  # Pour la gestion des chemins compatibles avec tous les systèmes
import api

# Initialisation de Pygame
pygame.init()

# Constantes de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080  # Dimensions de l'écran
ROOM_WIDTH, ROOM_HEIGHT = 3800, SCREEN_HEIGHT  # Dimensions de la salle plus grandes que l'écran
FPS = 60
CARRE_WIDTH = 300
CARRE_HEIGH = 300
NUM_CARRES = 10
CARRE_SPACING = 200
ROOM_WIDTH = NUM_CARRES * (200 + 100) - 100

# Thèmes
THEME = [
    "GUERRE",
    "ABSTRAIT",
    "ARTS PLASTIQUES",
    "EMOTIONS",
    "NATURE",
    "STREET ART"
]

# Couleurs associées aux thèmes
THEME_STYLES = {
    "GUERRE": (255, 0, 0),
    "EMOTIONS": (255, 165, 0),
    "NATURE": (34, 139, 34),
    "ABSTRAIT": (75, 0, 130),
    "NOTRE COLLECTION PERSONEL": (255, 215, 0),
    "STREET ART": (169, 169, 169),
    "ARTS PLASTIQUES": (255, 255, 255)
}

# Dictionnaire pour les images de fond des thèmes
THEME_IMAGES = {
    "GUERRE": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_guerre.png"),
    "ABSTRAIT": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_abstrait.png"),
    "ARTS PLASTIQUES": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_art_plastique.png"),
    "EMOTIONS": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_emotion.png"),
    "NATURE": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_nature.png"),
    "STREET ART": os.path.join("Musee-virtuel", "Client", "Interface", "Thème_street_art.png"),
}

# Dictionnaire pour les tableaux
TABLEAUX = [
    {"titre": "Tableau 1", "auteur": "Auteur 1", "bio": "Biographie 1", "image": None, "image_no_frame": None},
    {"titre": "Tableau 2", "auteur": "Auteur 2", "bio": "Biographie 2", "image": None, "image_no_frame": None},
    {"titre": "Tableau 3", "auteur": "Auteur 3", "bio": "Biographie 3", "image": None, "image_no_frame": None},
    {"titre": "Tableau 4", "auteur": "Auteur 4", "bio": "Biographie 4", "image": None, "image_no_frame": None},
    {"titre": "Tableau 5", "auteur": "Auteur 5", "bio": "Biographie 5", "image": None, "image_no_frame": None},
]

couloir_liste = api.get_couloir_liste()

# Initialisation de l'écran en mode plein écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

# Police pour afficher le thème
font = pygame.font.Font(None, 74)
text_font = pygame.font.Font(None, 36)

# Charger les images des cadres
frame_image_carre = pygame.image.load(os.path.join("Musee-virtuel", "Client", "Interface", "cadre_carre.png")).convert_alpha()
frame_image_portrait = pygame.image.load(os.path.join("Musee-virtuel", "Client", "Interface", "cadre_portrait.png")).convert_alpha()
frame_image_paysage = pygame.image.load(os.path.join("Musee-virtuel", "Client", "Interface", "cadre_paysage.png")).convert_alpha()

def draw_frame(image, frame_image):
    """Dessine un cadre autour de l'image en utilisant une image de cadre."""
    frame = pygame.Surface((frame_image.get_width(), frame_image.get_height()), pygame.SRCALPHA)
    frame.blit(image, ((frame_image.get_width() - image.get_width()) // 2, (frame_image.get_height() - image.get_height()) // 2))
    frame.blit(frame_image, (0, 0))
    return frame

def get_frame_image(image):
    """Retourne l'image de cadre appropriée en fonction de l'orientation de l'image."""
    width, height = image.get_size()
    if width == height:
        return frame_image_carre
    elif width > height:
        return frame_image_paysage
    else:
        return frame_image_portrait

def load_tableaux(salle_id: int) -> None:
    """Charge les tableaux dans la nouvelle salle, concrètement on update TABLEAUX et NUM_CARRES"""
    global TABLEAUX, NUM_CARRES
    salle_id += 1
    TABLEAUX = [{"titre": "NE DOIT PAS APPARAITRE", "auteur": "NE DOIT PAS APPARAITRE", "bio": "NE DOIT PAS APPARAITRE", "image": None, "image_no_frame": None}]
    api_tab_liste = api.get_tableaux_from_couloir_id(salle_id)
    for k, v in api_tab_liste.items():
        original_image = api.get_tableau_image(int(k)).convert_alpha()

        # Obtenir les dimensions d'origine
        orig_width, orig_height = original_image.get_size()

        # Calcul du facteur d'échelle pour s'assurer que l'image tient dans 300x300 sans être déformée
        scale_factor = min(300 / orig_width, 300 / orig_height)
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)

        # Redimensionner l'image en gardant les proportions
        image = pygame.transform.scale(original_image, (new_width, new_height))
        frame_image = get_frame_image(image)
        image_with_frame = draw_frame(image, frame_image)

        # Calcul du facteur d'échelle pour s'assurer que l'image tient dans 600x600 sans être déformée
        scale_factor = min(600 / orig_width, 600 / orig_height)
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)

        # Redimensionner l'image en gardant les proportions
        big_image = pygame.transform.scale(original_image, (new_width, new_height))
        big_frame_image = get_frame_image(big_image)
        big_image_with_frame = draw_frame(big_image, big_frame_image)

        TABLEAUX.append({"titre": v["nom"], "auteur": v["auteur"], "bio": v["description"], "image": image_with_frame, "image_no_frame": big_image, "big_image": big_image_with_frame})
    NUM_CARRES = len(TABLEAUX) + 1
    print("loaded tableaux:", TABLEAUX)

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
            pygame.draw.rect(screen, (255, 255, 255, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

            # Afficher le tableau sélectionné agrandi sans cadre
            screen.blit(TABLEAUX[selected_tableau]["image_no_frame"], ((SCREEN_WIDTH - TABLEAUX[selected_tableau]["image_no_frame"].get_width()) // 10, (SCREEN_HEIGHT - TABLEAUX[selected_tableau]["image_no_frame"].get_height()) // 2, TABLEAUX[selected_tableau]["image_no_frame"].get_width(), TABLEAUX[selected_tableau]["image_no_frame"].get_height()))

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
                if i == 0 or i == len(tableau_positions) - 1:
                    continue  # Ignorer le premier et le dernier tableau
                screen.blit(TABLEAUX[i]["image"], camera.apply(pygame.Rect(pos[0], pos[1], TABLEAUX[i]["image"].get_width(), TABLEAUX[i]["image"].get_height())))

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
    load_tableaux(theme_index)
    theme_index = run_room(theme_index)

print("Toutes les salles ont été terminées!")
pygame.quit()
    