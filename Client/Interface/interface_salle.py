import pygame

# Initialisation de Pygame
pygame.init()

# Constantes de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 1900, 1080
ROOM_WIDTH, ROOM_HEIGHT = 3000, 1080  # Dimensions de la salle plus grandes que l'écran
FPS = 60

# Thèmes
THEME = [
    "GUERRE",
    "PAIX",
    "SANTE MENTALE",
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
    "PAIX": (0, 255, 0),
    "SANTE MENTALE": (128, 0, 128),
    "EMOTIONS": (255, 165, 0),
    "NATURE": (34, 139, 34),
    "ABSTRAIT": (75, 0, 130),
    "NOTRE COLLECTION PERSONEL": (255, 215, 0),
    "STREET ART": (169, 169, 169),
    "DIVERS": (255, 255, 255)
}

# Dictionnaire pour les images de fond des thèmes
THEME_IMAGES = {
    "GUERRE": "thème_nature.png",
    "PAIX": "thème_paix.png",
    "SANTE MENTALE": "thème_sante_mentale.png",
    "EMOTIONS": "thème_emotions.png",
    "NATURE": "thème_nature.png",
    "ABSTRAIT": "thème_abstrait.png",
    "NOTRE COLLECTION PERSONEL": "thème_collection_personel.png",
    "STREET ART": "thème_street_art.png",
    "DIVERS": "thème_divers.png"
}

# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Police pour afficher le thème
font = pygame.font.Font(None, 74)

# Classe Joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprite.png").convert_alpha()  # Charge l'image du joueur
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

# Fonction pour exécuter une salle
def run_room(theme_index):
    running = True
    clock = pygame.time.Clock()

    # Définir le thème et la couleur de la salle
    theme = THEME[theme_index]
    theme_color = THEME_STYLES[theme]

    # Charger l'image de fond associée au thème et la redimensionner à la taille de l'écran
    background_image = pygame.image.load(THEME_IMAGES[theme]).convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Mettre à jour le titre de la fenêtre
    pygame.display.set_caption(f"Salle du {theme}")

    # Initialisation des sprites
    all_sprites = pygame.sprite.Group()
    player = Player()
    door_right = Door("right")
    door_left = Door("left")
    all_sprites.add(player, door_right, door_left)

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

        # Vérification de collision avec les portes
        if pygame.sprite.collide_rect(player, door_right):
            print(f"Porte droite atteinte! Transition vers le thème suivant: {THEME[theme_index + 1] if theme_index + 1 < len(THEME) else 'Fin' }")
            return theme_index + 1
        if pygame.sprite.collide_rect(player, door_left):
            print(f"Porte gauche atteinte! Retour au thème précédent: {THEME[theme_index - 1] if theme_index - 1 >= 0 else 'Début' }")
            return max(theme_index - 1, 0)

        # Affichage
        screen.blit(background_image, (0, 0))  # Afficher l'image de fond redimensionnée

        # Affichage des sprites
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

        # Affichage du thème
        theme_text = font.render(theme, True, (0, 0, 0))
        text_rect = theme_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(theme_text, text_rect)

        pygame.display.flip()

# Boucle pour les salles
theme_index = 0
while theme_index < len(THEME):
    theme_index = run_room(theme_index)

print("Toutes les salles ont été terminées!")
pygame.quit()
