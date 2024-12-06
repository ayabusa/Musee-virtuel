import pygame, sys, math, random

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 600
RES = WIDTH, HEIGHT = 1020, 600
HALF_W, HALF_H = WIDTH / 2, HEIGHT / 2
SIZE_TEXTE = 50
BLACK = (0,0,0)
WHITE = (255,255,255)
SIZE = 400
GREEN = (0,255,0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Musée GLANF")
clock = pygame.time.Clock()
# running = True

# while running:
while True:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # déplacé depuis le bas du code vers ici.
            sys.exit()
            # running = False # remplacé par le while True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            for btn in buttons:
                btn_rect = buttons[btn]
                if btn_rect.collidepoint(m_pos) and pygame.mouse.get_pressed()[0]:
                    print('HELLO WORLD!')

    offset_y = 80
    enter_button = pygame.Rect(
        HALF_W-100,
        HALF_H-25+offset_y
    , 200, 50)
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 40)
    buttons = { 
    "ENTRER": enter_button,
    }
    def draw_buttons(screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 115, 230), enter_button,0,25)
        font = pygame.font.SysFont(None, 36)
        enter = font.render("ENTRER", True, WHITE)
        enter_rect = enter.get_rect()
        # screen.blit(enter,(SCREEN_WIDTH/2 - SIZE /3+40,(SCREEN_HEIGHT/2+SIZE/4+17.5)))
        screen.blit(enter, (

            enter_button.x + enter_button.width / 2 - enter_rect.width / 2,
            enter_button.y + enter_button.height / 2 - enter_rect.height / 2

        ))

    screen.fill("white")

    font = pygame.font.Font(None,SIZE_TEXTE)
    textes = [
        "BIENVENUE",
        "AU",
        "MUSEE GLANF"
    ]
    total_height = 0
    for texte in textes:
        txt = font.render(texte, True, BLACK)
        txt_rect = txt.get_rect()
        total_height += txt_rect.height * 1.5

    for y, texte in enumerate(textes):
        txt = font.render(texte, True, BLACK)
        txt_rect = txt.get_rect()
        y += 1

        screen.blit(
            txt,
            (
                SCREEN_WIDTH / 2 - txt_rect.width / 2, # centrer sur Ox
                SCREEN_HEIGHT / 2 - total_height + (1 + 2*y) * txt_rect.height / 2 
            )
        )

    draw_buttons(screen)
    pygame.display.flip()

    clock.tick(60)  
