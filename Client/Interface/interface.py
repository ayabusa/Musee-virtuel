import pygame, sys, math, random

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 600
SIZE_TEXTE = 50
BLACK = (0,0,0)
WHITE = (255,255,255)
SIZE = 400

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

    enter_button = pygame.Rect(SCREEN_WIDTH/2 - SIZE /3,SCREEN_HEIGHT/2+SIZE/4, 200, 50)
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 40)
    buttons = { 
    "ENTRER": enter_button,
    }
    def draw_buttons(screen):
        pygame.draw.rect(screen, (0, 115, 230), enter_button,0,25)
        font = pygame.font.SysFont(None, 36)
        enter = font.render("ENTRER", True, WHITE)
        screen.blit(enter,(SCREEN_WIDTH/2 - SIZE /3+40,(SCREEN_HEIGHT/2+SIZE/4+17.5)))
    


    screen.fill("white")
    font = pygame.font.Font(None,SIZE_TEXTE)
    text   = font.render("BIENVENUE", True, BLACK)
    text_2   = font.render("AU", True, BLACK)
    text_3   = font.render("MUSEE GLANF", True, BLACK)
    screen.blit(text,(SCREEN_WIDTH/2 - SIZE_TEXTE*2.5,SCREEN_HEIGHT/2-100))
    screen.blit(text_2,(SCREEN_WIDTH/2 - SIZE_TEXTE*1.2,SCREEN_HEIGHT/2-50))
    screen.blit(text_3,(SCREEN_WIDTH/2 - SIZE_TEXTE*3,SCREEN_HEIGHT/2))
    draw_buttons(screen)
    pygame.display.flip()

    clock.tick(60)  
