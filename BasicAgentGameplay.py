import sys
import time

import BasicAgent
import Environment
import pygame

HEIGHT = 50
WIDTH = 50
MINES = 100

# Colors
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Create game
pygame.init()
size = width, height = 1050, 700
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/VrindaHasFlag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/AzimIsTheMine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent
game = Environment.Environment(height=HEIGHT, width=WIDTH, mines=MINES)
ai = BasicAgent.BasicAgent(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

# Show instructions initially
instructions = True

# Keep track of triggered mines
triggered_mines = []

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(MAGENTA)

    # Show game instructions
    if instructions:

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:  # and ai_trigger == (i,j):
                screen.blit(mine, rect)
            elif (i, j) in flags:
                # display triggered mine
                if (i, j) in triggered_mines:
                    screen.blit(mine, rect)
                else:
                    screen.blit(flag, rect)
            elif (i, j) in revealed:
                neighbors = smallFont.render(
                    str(game.mineNeighbor((i, j))),
                    True, BLACK
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    #TYPE OF AGENT
    AgentType = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 200,
        (width / 3) - BOARD_PADDING * 2, 50)
    buttonText = mediumFont.render("Basic Agent", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = AgentType.center
    pygame.draw.rect(screen, MAGENTA, AgentType)
    screen.blit(buttonText, buttonRect)

    #TOTAL MINES
    AgentType = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 150,
        (width / 3) - BOARD_PADDING * 2, 50)
    buttonText = mediumFont.render("Total Mines: " + str(MINES), True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = AgentType.center
    pygame.draw.rect(screen, MAGENTA, AgentType)
    screen.blit(buttonText, buttonRect)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    # Display text
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # If AI button clicked, make an AI move
        if aiButton.collidepoint(mouse) and not lost:
            move = ai.move_safely()
            if move is None:
                move = ai.move_randomly()
                if move is None:
                    flags = ai.mineSet.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            # Added Code to Update Flags in RealTime
            for ai_mine in ai.FlagCells():
                flags.add(ai_mine)
            time.sleep(0.2)

            # for game.mines in ai.movesmade():
            #     mines.add(game.mines)
            # time.sleep(0.2)

        # Reset game state
        elif resetButton.collidepoint(mouse):
            game = Environment.Environment(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = BasicAgent.BasicAgent(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            continue

        # User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # Make move and update AI knowledge
    if move:
        if game.is_mine(move):
            # lost = True
            ai.MarkMine(move)
            triggered_mines.append(move)
            # revealed.add(move)
            print(move)
            print("Mine Triggered")


        else:
            nearby = game.mineNeighbor(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()