import pygame
import os  # Pour la gestion des chemins compatibles avec tous les systèmes

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
    "GUERRE": os.path.join("Client", "Interface", "Thème_nature.png"),
    "PAIX": os.path.join("Client", "Interface", "Thème_paix.png"),
    "SANTE MENTALE": os.path.join("Client", "Interface", "Thème_sante_mentale.png"),
    "EMOTIONS": os.path.join("Client", "Interface", "Thème_emotions.png"),
    "NATURE": os.path.join("Client", "Interface", "Thème_nature.png"),
    "ABSTRAIT": os.path.join("Client", "Interface", "Thème_abstrait.png"),
    "NOTRE COLLECTION PERSONEL": os.path.join("Client", "Interface", "Thème_collection_personel.png"),
    "STREET ART": os.path.join("Client", "Interface", "Thème_street_art.png"),
    "DIVERS": os.path.join("Client", "Interface", "Thème_divers.png")
}

# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Police pour afficher le thème
font = pygame.font.Font(None, 74)

# Classe Porte
class Door(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((50, SCREEN_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        if position == "right":
            self.rect.right = SCREEN_WIDTH  # Ajustement pour correspondre à l'écran
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
    try:
        background_image = pygame.image.load(THEME_IMAGES[theme]).convert()
        background_image = pygame.transform.scale(background_image, (ROOM_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        print(f"Erreur : L'image pour le thème '{theme}' est introuvable.")
        background_image = pygame.Surface((ROOM_WIDTH, SCREEN_HEIGHT))
        background_image.fill(theme_color)

    # Mettre à jour le titre de la fenêtre
    pygame.display.set_caption(f"Salle du {theme}")

    # Initialisation de la caméra (position de la vue dans la salle)
    camera_x = 0

    # Initialisation des portes
    door_right = Door("right")
    door_left = Door("left")

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Gestion des touches
        keys = pygame.key.get_pressed()
        
        # Déplacement de la caméra (simuler un mouvement à la première personne)
        if keys[pygame.K_RIGHT]:
            camera_x += 10  # Déplacement à droite
        if keys[pygame.K_LEFT]:
            camera_x -= 10  # Déplacement à gauche

        # Limiter le mouvement de la caméra aux bords de la salle
        camera_x = max(0, min(camera_x, ROOM_WIDTH - SCREEN_WIDTH))

        # Vérification de collision avec les portes
        if camera_x + SCREEN_WIDTH >= ROOM_WIDTH:  # Arrivée à la porte droite
            print(f"Porte droite atteinte! Transition vers le thème suivant : {THEME[theme_index + 1] if theme_index + 1 < len(THEME) else 'Fin'}")
            return theme_index + 1
        if camera_x <= 0:  # Arrivée à la porte gauche
            print(f"Porte gauche atteinte! Retour au thème précédent : {THEME[theme_index - 1] if theme_index - 1 >= 0 else 'Début'}")
            return max(theme_index - 1, 0)

        # Affichage
        screen.blit(background_image, (-camera_x, 0))  # Afficher l'image de fond décalée par la position de la caméra

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
