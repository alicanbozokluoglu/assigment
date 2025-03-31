# Import pygame and sys
import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agar.io Ultimate! 🟢")

# Colors
white = (255, 255, 255)
blue = (0, 100, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Map size (big arena)
arena_width, arena_height = 3000, 3000

# Font
font = pygame.font.SysFont(None, 35)

# Calculate distance between two points
def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Move bot towards player (aggressive)
def move_bot_towards_player(bot, player_pos):
    # Move the bot towards the player
    angle = math.atan2(player_pos[1] - bot["y"], player_pos[0] - bot["x"])
    bot["x"] += math.cos(angle) * bot["speed"]
    bot["y"] += math.sin(angle) * bot["speed"]

# Move bot away from player (fleeing)
def move_bot_away_from_player(bot, player_pos):
    # Move the bot away from the player
    angle = math.atan2(player_pos[1] - bot["y"], player_pos[0] - bot["x"]) + math.pi  # Reverse direction
    bot["x"] += math.cos(angle) * bot["speed"]
    bot["y"] += math.sin(angle) * bot["speed"]

# Move bot randomly (neutral)
def move_bot_randomly(bot):
    # Move the bot randomly
    bot["x"] += random.choice([-1, 1]) * bot["speed"]
    bot["y"] += random.choice([-1, 1]) * bot["speed"]

# Menu function
def menu():
    while True:
        screen.fill(white)
        
        # Draw menu title
        draw_text("Agar.io Ultimate!", font, black, screen, screen_width // 2, screen_height // 4)
        
        # Draw "Start Game" button
        draw_text("Start Game", font, black, screen, screen_width // 2, screen_height // 2 - 50)
        
        # Draw "Quit Game" button
        draw_text("Quit Game", font, black, screen, screen_width // 2, screen_height // 2 + 50)

        pygame.display.update()

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if "Start Game" button is clicked
                if screen_width // 2 - 100 < mouse_x < screen_width // 2 + 100:
                    if screen_height // 2 - 75 < mouse_y < screen_height // 2 - 25:
                        game_loop()

                # Check if "Quit Game" button is clicked
                if screen_width // 2 - 100 < mouse_x < screen_width // 2 + 100:
                    if screen_height // 2 + 25 < mouse_y < screen_height // 2 + 75:
                        pygame.quit()
                        sys.exit()


        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if "Start Game" button is clicked
                if screen_width // 2 - 100 < mouse_x < screen_width // 2 + 100:
                    if screen_height // 2 - 75 < mouse_y < screen_height // 2 - 25:
                        game_loop()

                # Check if "Quit Game" button is clicked
                elif screen_width // 2 - 100 < mouse_x < screen_width // 2 + 100:
                    if screen_height // 2 + 25 < mouse_y < screen_height // 2 + 75:
                        pygame.quit()
                        sys.exit()

# Main game loop
def game_loop():
    # Player properties
    player_pos = [arena_width // 2, arena_height // 2]
    player_radius = 20
    player_speed = 8

    # Food properties
    food_count = 200
    food_radius = 5
    food_list = []
    for i in range(food_count):
        x = random.randint(0, arena_width)
        y = random.randint(0, arena_height)
        food_list.append([x, y])

    # Bot properties
    bot_count = 15
    bots = []
    for i in range(bot_count):
        bot_x = random.randint(0, arena_width)
        bot_y = random.randint(0, arena_height)
        bot_radius = random.randint(10, 60)  # Some bots will be very large
        bot_speed = random.uniform(1.5, 4)  # Slower speeds to make movement smoother
        
        # Define bot behavior
        if bot_radius > 40:
            bot_behavior = "aggressive"  # Big bots are aggressive
        elif bot_radius < 20:
            bot_behavior = "fleeing"  # Small bots will flee
        else:
            bot_behavior = "neutral"  # Normal bots are neutral
            
        bots.append({
            "x": bot_x, 
            "y": bot_y, 
            "radius": bot_radius, 
            "speed": bot_speed,
            "behavior": bot_behavior
        })

    # Camera properties
    camera_x, camera_y = player_pos[0] - screen_width // 2, player_pos[1] - screen_height // 2

    # Main game loop
    while True:
        # Fill the screen with white
        screen.fill(white)

        # Check for events (like closing the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get keys pressed for player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= player_speed
        if keys[pygame.K_s]:
            dy += player_speed
        if keys[pygame.K_a]:
            dx -= player_speed
        if keys[pygame.K_d]:
            dx += player_speed

        # Update player position
        player_pos[0] += dx
        player_pos[1] += dy

        # Keep player within arena boundaries
        player_pos[0] = max(player_radius, min(arena_width - player_radius, player_pos[0]))
        player_pos[1] = max(player_radius, min(arena_height - player_radius, player_pos[1]))

        # Update camera to follow the player
        camera_x, camera_y = player_pos[0] - screen_width // 2, player_pos[1] - screen_height // 2

        # Draw food
        for food in food_list:
            pygame.draw.circle(screen, green, (food[0] - camera_x, food[1] - camera_y), food_radius)

        # Check for collisions with food
        new_food_list = []
        for food in food_list:
            if distance(player_pos, food) < player_radius + food_radius:
                player_radius += 1  # Eat food and grow
            else:
                new_food_list.append(food)
        food_list = new_food_list

        # Draw and move bots
        for bot in bots:
            pygame.draw.circle(screen, red, (bot["x"] - camera_x, bot["y"] - camera_y), bot["radius"])

            # Handle different bot behaviors
            if bot["behavior"] == "aggressive":
                move_bot_towards_player(bot, player_pos)
            elif bot["behavior"] == "fleeing":
                move_bot_away_from_player(bot, player_pos)
            else:
                move_bot_randomly(bot)

            # Keep bots within arena
            bot["x"] = max(bot["radius"], min(arena_width - bot["radius"], bot["x"]))
            bot["y"] = max(bot["radius"], min(arena_height - bot["radius"], bot["y"]))

            # Bot eats player if bigger
            if distance(player_pos, (bot["x"], bot["y"])) < player_radius + bot["radius"]:
                if player_radius > bot["radius"]:
                    player_radius += bot["radius"] // 2
                    bots.remove(bot)
                else:
                    print("💀 Game Over! Bot Yedi Seni!")
                    pygame.quit()
                    sys.exit()

        # Draw player
        pygame.draw.circle(screen, blue, (player_pos[0] - camera_x, player_pos[1] - camera_y), player_radius)

        # Update the display
        pygame.display.update()

        # Set the frame rate to 60 FPS
        pygame.time.Clock().tick(60)

# Start the game by showing the menu
menu()
