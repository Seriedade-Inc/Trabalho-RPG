import pygame
import sys

def transition_bars(screen, width, height, color=(255, 255, 255), speed=15):
    """
    Cria uma transição de barras horizontais estilo Pokémon.
    """
    bar_height = height // 10  # Divide a tela em 10 barras
    bars = []
    
    # Inicializa as barras fora da tela (à esquerda ou direita alternadamente)
    for i in range(10):
        if i % 2 == 0:
            # Barras pares vêm da esquerda
            bars.append(pygame.Rect(-width, i * bar_height, width, bar_height))
        else:
            # Barras ímpares vêm da direita
            bars.append(pygame.Rect(width, i * bar_height, width, bar_height))

    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Preenche o fundo com o que já estava na tela antes (opcional)
        # Se quiser que o fundo fique preto atrás das barras, descomente:
        # screen.fill((0, 0, 0)) 

        all_done = True
        for i, bar in enumerate(bars):
            if i % 2 == 0:
                if bar.x < 0:
                    bar.x += speed
                    all_done = False
                else:
                    bar.x = 0
            else:
                if bar.x > 0:
                    bar.x -= speed
                    all_done = False
                else:
                    bar.x = 0
            
            pygame.draw.rect(screen, color, bar)

        pygame.display.flip()
        clock.tick(60)

        if all_done:
            running = False
            
    # Pequena pausa no final para impacto visual
    pygame.time.delay(200)