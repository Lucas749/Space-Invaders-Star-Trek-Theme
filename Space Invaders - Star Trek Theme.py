# Import packages
import pygame
import random

# Define screen parameters
WIDTH, HEIGHT = 1080, 1000

# Initialize pygame
pygame.font.init()
pygame.init()

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load game assets
ICON = pygame.image.load('assets/Logo.png')
BACKGROUND = pygame.transform.scale(pygame.image.load('assets/Nasa_background.jpg'), (WIDTH, HEIGHT))
START_SCREEN = pygame.transform.scale(pygame.image.load('assets/Nasa_startscreen.jpg'), (WIDTH, HEIGHT))
INTRO_SCREEN = pygame.transform.scale(pygame.image.load('assets/Nasa_introscreen.jpg'), (WIDTH, HEIGHT))
SPACE_SHUTTLE = pygame.transform.scale(pygame.image.load('assets/Space_shuttle.png'), (int(233 * 1.5), int(150 * 1.5)))
SPACE_SHUTTLE_SMALL = pygame.transform.scale(pygame.image.load('assets/Space_shuttle.png'), (int(233), int(150)))
PLAYER_ICON = pygame.transform.scale(pygame.image.load('assets/Player_ship.png'), (30, 30))
BULLET_IMG = pygame.transform.scale(pygame.image.load('assets/Bullet.png'), (10, 10))
KLINGON_SHIP = pygame.transform.scale(pygame.image.load('assets/Klingon_Ship.png'), (32, 32))
KLINGON_BOMB = pygame.transform.scale(pygame.image.load('assets/Klingon_Bomb.png'), (15, 15))
BORG_SHIP = pygame.transform.scale(pygame.image.load('assets/Borg_Ship.png'), (32, 32))
BORG_BOMB = pygame.transform.scale(pygame.image.load('assets/Borg_Bomb.png'), (15, 15))
ROMULAN_SHIP = pygame.transform.scale(pygame.image.load('assets/Romulan_Ship.png'), (32, 32))
ROMULAN_BOMB = pygame.transform.scale(pygame.image.load('assets/Romulan_Bomb.png'), (15, 15))
BLACKHOLE = pygame.transform.scale(pygame.image.load('assets/Black_Hole.png'), (40, 40))
BLACKHOLE_BIG = pygame.transform.scale(pygame.image.load('assets/Black_Hole.png'), (100, 100))
HEART = pygame.transform.scale(pygame.image.load('assets/Heart.png'), (20, 20))

# Set title and icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(ICON)


# Class laser
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)


# Class Healthpackage
class Healthpackage(Laser):
    def __init__(self, x, y, img):
        super().__init__(x, y, img)
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def off_screen(self, height):
        return (self.y >= height)


# Function checks if objects collide
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# Ship superclass
class Ships:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = PLAYER_ICON
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, screen):
        screen.blit(self.ship_img, (self.x, self.y))

        for laser in self.lasers:
            laser.draw(screen)

        # pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50), 0)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


# Player subclass
class Player(Ships):
    BLACKHOLE_COOLDOWN = 300

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_ICON
        self.laser_img = BULLET_IMG
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.blackhole_cooldown_counter = 1
        self.blackhole_shot = 0
        self.blackhole_available = False

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def healthbar(self):
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(screen, (0, 255, 0), (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width() * (self.health / self.max_health),
            10))

    def blackhole_cooldown(self):
        if self.blackhole_cooldown_counter >= self.BLACKHOLE_COOLDOWN:
            self.blackhole_cooldown_counter = 0
        elif self.blackhole_cooldown_counter > 0:
            self.blackhole_cooldown_counter += 1

    def blackhole_status(self):
        if (self.health == self.max_health and self.blackhole_cooldown_counter == 0):
            self.blackhole_available = True
        return (self.health == self.max_health and self.blackhole_cooldown_counter == 0) or (
                self.blackhole_available == True)

    def draw(self, screen):
        super().draw(screen)
        self.healthbar()
        self.blackhole_cooldown()
        if self.blackhole_status():
            screen.blit(BLACKHOLE, (10, HEIGHT - 50))
        if self.blackhole_shot == 1:
            self.blackhole_shot = 0
            screen.blit(BLACKHOLE_BIG,
                        (WIDTH / 2 - BLACKHOLE_BIG.get_width() / 2, HEIGHT / 2 - BLACKHOLE_BIG.get_height() / 2))

    def shoot_blackhole(self):
        if self.blackhole_status():
            self.blackhole_shot = 1
            self.blackhole_available = False
            self.blackhole_cooldown_counter = 1


# Enemy ship subclass
class Enemy(Ships):
    ENEMY_TYPE = {
        "Klingon": (KLINGON_SHIP, KLINGON_BOMB),
        "Borg": (BORG_SHIP, BORG_BOMB),
        "Romulan": (ROMULAN_SHIP, ROMULAN_BOMB),
    }

    def __init__(self, x, y, type, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.ENEMY_TYPE[type]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


# Game loop
def main():
    # Set general parameters
    running = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("Arial", 50)
    lost = False
    lost_count = 0
    clock = pygame.time.Clock()

    # Set enemy parameters
    enemies = []
    wave_length = 5
    enemy_vel = 3
    laser_vel = 7

    # Set player parameters
    player_vel = 10
    player = Player(int(WIDTH / 2 - BLACKHOLE_BIG.get_width() / 2), 800)

    # Set healthpackage parameters
    healthpackage = []
    health_vel = 7

    # Draw window function
    def redraw_window():
        screen.blit(BACKGROUND, (0, 0))

        # Draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        # Draw ships
        player.draw(screen)

        for h in healthpackage:
            h.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        if lost:
            lost_label = main_font.render("Federation Lost!", 1, (255, 255, 255))
            screen.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, HEIGHT / 2))

        if len(enemies) == 0 and not lost:
            wave_label = main_font.render(f"Wave {level} incoming", 1, (255, 255, 255))
            screen.blit(wave_label, (WIDTH / 2 - wave_label.get_width() / 2, HEIGHT / 2))

        # Update lives and levels
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        pygame.display.update()

    # "Play Game" loop
    while running:
        clock.tick(FPS)
        redraw_window()

        # Event loop to close program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        # Restart game if player loses
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                running = False
            else:
                continue

        # Add enemies if wave complete
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            redraw_window()
            pygame.time.wait(1200)

            # Randomly spawn enemies
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["Klingon", "Borg", "Romulan"]))
                enemies.append(enemy)

        # Enemies logic
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # Randomly spawn healthpackages
        if (random.randint(0, 100 * FPS) < 10):
            h = Healthpackage(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), HEART)
            healthpackage.append(h)

        for h in healthpackage[:]:
            h.move(health_vel)
            if collide(h, player):
                player.health = player.max_health
                healthpackage.remove(h)

            if h.off_screen(HEIGHT):
                healthpackage.remove(h)

        # Player controls
        player.move_lasers(-laser_vel, enemies)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # left
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # left
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # left
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_f]:
            if player.blackhole_status():
                enemies = []
            player.shoot_blackhole()


# Get mouse location to click on buttons
def button_click(button_coor, img_size):
    x_range = pygame.mouse.get_pos()[0] >= button_coor[0] and pygame.mouse.get_pos()[0] <= button_coor[0] + img_size[0]
    y_range = pygame.mouse.get_pos()[1] >= button_coor[1] and pygame.mouse.get_pos()[1] <= button_coor[1] + img_size[1]
    return (x_range and y_range)


# Game menu mission section
def rules():
    text_font = pygame.font.SysFont("Arial", 40)
    title_font = pygame.font.SysFont("Arial", 30)
    running = True

    while running:
        screen.blit(INTRO_SCREEN, (0, 0))

        # Add mission text to screen
        text = ["The Earth's moon outpost detected an armada of enemy ships",
                "close to the Federation's orbit. You were selected to lead ",
                "the interception mission. Destroy all enemy ships", "before they reach the earth.",
                "Your ship is equipped with the  latest technology.",
                "Phaser torpedos (Space-key) and black holes (F-key) are your main",
                "weapons and give you an advantage.", "Make the Federation proud!"]
        for i, t in enumerate(text):
            text_label = text_font.render(t, 1, (255, 255, 255))
            screen.blit(text_label, (WIDTH / 2 - text_label.get_width() / 2, 75 * (1 + i)))

        # Add back button
        back_label = title_font.render("BACK", 1, (0, 0, 0))
        button_img = (SPACE_SHUTTLE_SMALL.get_width(), SPACE_SHUTTLE_SMALL.get_height())
        back_button_coor = (20, HEIGHT - 200)
        screen.blit(SPACE_SHUTTLE_SMALL, back_button_coor)
        screen.blit(back_label, (back_button_coor[0] + button_img[0] / 2 - back_label.get_width() / 2,
                                 back_button_coor[1] + button_img[1] / 2 - back_label.get_height() / 2))

        pygame.display.update()

        # Event loop to go back to main menu and close program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and button_click(back_button_coor, button_img):
                main_menu()


# Main menu logic
def main_menu():
    # Set general parameters
    header_font = pygame.font.SysFont("Arial", 100)
    title_font = pygame.font.SysFont("Arial", 30)
    running = True

    while running:
        # Add labels and background
        screen.blit(START_SCREEN, (0, 0))
        game_label = header_font.render("Space Invaders by Luke749", 1, (255, 255, 255))
        play_label = title_font.render("PLAY GAME", 1, (0, 0, 0))
        instruct_label = title_font.render("MISSION", 1, (0, 0, 0))
        screen.blit(game_label, (WIDTH / 2 - game_label.get_width() / 2, 40))
        play_button_coor = (WIDTH / 2 - SPACE_SHUTTLE.get_width() / 2, HEIGHT / 2 - 150)
        screen.blit(SPACE_SHUTTLE, play_button_coor)
        screen.blit(play_label, (WIDTH / 2 - play_label.get_width() / 2,
                                 HEIGHT / 2 - 150 + SPACE_SHUTTLE.get_height() / 2 - play_label.get_height() / 2))
        button_img = (SPACE_SHUTTLE.get_width(), SPACE_SHUTTLE.get_height())
        instruct_coor = (WIDTH / 2 - SPACE_SHUTTLE.get_width() / 2, HEIGHT / 2 + 150)
        screen.blit(SPACE_SHUTTLE, instruct_coor)
        screen.blit(instruct_label, (WIDTH / 2 - instruct_label.get_width() / 2,
                                     HEIGHT / 2 + 150 + SPACE_SHUTTLE.get_height() / 2 - instruct_label.get_height() / 2))
        pygame.display.update()

        # Event loop to run game and close program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and button_click(play_button_coor, button_img):
                main()
            if event.type == pygame.MOUSEBUTTONDOWN and button_click(instruct_coor, button_img):
                rules()
    pygame.quit()


main_menu()
