import tkinter as tk
import time

# --- Configuration & Physics Constants ---
FPS = 60
FRAME_TIME = 1 / FPS

# Colors (Hex)
SKY_DEEP = "#4A90E2"
SKY_LIGHT = "#87CEEB"
RED = "#E60000"
BLUE = "#0055AA"
SKIN = "#FFCC99"
BROWN = "#8B4513"
DARK_BROWN = "#5D2E0A"
GRASS = "#228B22"
DARK_GRASS = "#006400"
GOLD = "#FFD700"
LIGHT_GOLD = "#FFFACD"
GREEN = "#00FF00"
DARK_GREEN = "#008000"
WHITE = "#FFFFFF"
BLACK = "#000000"
PINK = "#FF69B4"
YELLOW = "#FFFF00"
GRAY = "#808080"

GRAVITY = 0.8
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_JUMP = -14

def create_pixel_image(pixel_data, scale=3):
    height = len(pixel_data)
    width = len(pixel_data[0])
    img = tk.PhotoImage(width=width * scale, height=height * scale)
    for r in range(height):
        row_colors = []
        for c in range(width):
            color = pixel_data[r][c]
            row_colors.append(color if color else "") 
        pixel_block = "{" + " ".join(row_colors) + "}"
        for s in range(scale):
            img.put(pixel_block, to=(0, r * scale + s, width * scale, r * scale + s + 1))
    return img

# --- Pixel Data Grids ---
_ = None
MARIO_PIXELS = [
    [_, _, RED, RED, RED, RED, RED, _],
    [_, RED, RED, RED, RED, RED, RED, RED],
    [_, BROWN, BROWN, BROWN, SKIN, SKIN, BLACK, _],
    [BROWN, SKIN, BROWN, SKIN, SKIN, SKIN, BLACK, _],
    [BROWN, SKIN, BROWN, BROWN, SKIN, SKIN, SKIN, _],
    [_, _, SKIN, SKIN, SKIN, SKIN, _, _],
    [_, _, BLUE, RED, BLUE, BLUE, _, _],
    [_, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, _],
    [BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE],
    [SKIN, SKIN, BLUE, BLUE, BLUE, BLUE, SKIN, SKIN],
    [_, _, BROWN, BROWN, _, BROWN, BROWN, _]
]

TURTLE_PIXELS = [
    [_, _, DARK_GREEN, DARK_GREEN, DARK_GREEN, _, _, _],
    [_, DARK_GREEN, GREEN, GREEN, GREEN, DARK_GREEN, _, _],
    [DARK_GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, YELLOW, _],
    [DARK_GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, YELLOW, YELLOW],
    [_, DARK_GREEN, GREEN, GREEN, GREEN, DARK_GREEN, BLACK, _],
    [_, _, DARK_GREEN, DARK_GREEN, DARK_GREEN, _, _, _],
    [_, _, YELLOW, _, _, YELLOW, _, _],
    [_, BROWN, _, _, _, _, BROWN, _]
]

PLANT_PIXELS = [
    [_, _, RED, RED, RED, RED, _, _],
    [_, RED, RED, WHITE, RED, RED, RED, _],
    [RED, RED, RED, RED, RED, WHITE, RED, RED],
    [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE],
    [RED, RED, WHITE, RED, RED, RED, RED, RED],
    [_, RED, RED, RED, WHITE, RED, RED, _],
    [_, _, RED, RED, RED, RED, _, _]
]

PRINCESS_PIXELS = [
    [_, _, _, YELLOW, YELLOW, _, _, _],
    [_, _, YELLOW, YELLOW, YELLOW, YELLOW, _, _],
    [_, _, SKIN, SKIN, SKIN, SKIN, _, _],
    [_, _, SKIN, SKIN, BLACK, SKIN, _, _],
    [_, _, SKIN, SKIN, SKIN, SKIN, _, _],
    [_, _, PINK, PINK, PINK, PINK, _, _],
    [_, PINK, PINK, PINK, PINK, PINK, PINK, _],
    [_, PINK, PINK, PINK, PINK, PINK, PINK, _],
    [PINK, PINK, PINK, PINK, PINK, PINK, PINK, PINK],
    [PINK, PINK, PINK, PINK, PINK, PINK, PINK, PINK],
    [PINK, PINK, PINK, PINK, PINK, PINK, PINK, PINK],
    [_, _, BROWN, _, _, BROWN, _, _]
]

DIRT_PIXELS = [
    [GRASS, GRASS, GRASS, GRASS, DARK_GRASS, GRASS, GRASS, GRASS],
    [GRASS, DARK_GRASS, GRASS, GRASS, GRASS, GRASS, DARK_GRASS, GRASS],
    [DARK_GRASS, GRASS, GRASS, GRASS, DARK_GRASS, GRASS, GRASS, DARK_GRASS],
    [BROWN, BROWN, BROWN, DARK_BROWN, BROWN, BROWN, BROWN, BROWN],
    [BROWN, DARK_BROWN, BROWN, BROWN, BROWN, DARK_BROWN, BROWN, BROWN],
    [BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN],
    [BROWN, BROWN, DARK_BROWN, BROWN, BROWN, BROWN, DARK_BROWN, BROWN],
    [BROWN, BROWN, BROWN, BROWN, DARK_BROWN, BROWN, BROWN, BROWN]
]

COIN_PIXELS = [
    [_, _, GOLD, GOLD, GOLD, GOLD, _, _],
    [_, GOLD, GOLD, LIGHT_GOLD, GOLD, GOLD, GOLD, _],
    [GOLD, GOLD, LIGHT_GOLD, GOLD, GOLD, GOLD, GOLD, GOLD],
    [GOLD, GOLD, LIGHT_GOLD, GOLD, GOLD, GOLD, GOLD, GOLD],
    [GOLD, GOLD, LIGHT_GOLD, GOLD, GOLD, GOLD, GOLD, GOLD],
    [GOLD, GOLD, GOLD, GOLD, GOLD, GOLD, GOLD, GOLD],
    [_, GOLD, GOLD, GOLD, GOLD, GOLD, GOLD, _],
    [_, _, GOLD, GOLD, GOLD, GOLD, _, _]
]

CLOUD_PIXELS = [
    [_, _, _, WHITE, WHITE, WHITE, _, _, _],
    [_, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, _],
    [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE]
]

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

class Player:
    def __init__(self, x, y):
        self.width = 24
        self.height = 33
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.on_ground = False
        self.jump_count = 0
        self.health = 1
        self.score = 0

    def jump(self):
        if self.on_ground:
            self.vel.y = PLAYER_JUMP
            self.on_ground = False
            self.jump_count = 1
        elif self.jump_count < 2:
            self.vel.y = PLAYER_JUMP
            self.jump_count = 2

    def update(self, platforms, keys, screen_height):
        self.acc = Vector2(0, GRAVITY)
        if keys.get("Left") or keys.get("left"): self.acc.x = -PLAYER_ACC
        elif keys.get("Right") or keys.get("right"): self.acc.x = PLAYER_ACC
        else: self.acc.x = 0
            
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel.x += self.acc.x
        self.vel.y += self.acc.y
        
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        for p in platforms:
            if self.collides_with(p):
                if self.vel.x > 0: self.pos.x = p.x - self.width
                elif self.vel.x < 0: self.pos.x = p.x + p.width
                self.vel.x = 0

        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.on_ground = False
        for p in platforms:
            if self.collides_with(p):
                if self.vel.y > 0:
                    self.pos.y = p.y - self.height
                    self.vel.y = 0
                    self.on_ground = True
                    self.jump_count = 0
                elif self.vel.y < 0:
                    self.pos.y = p.y + p.height
                    self.vel.y = 0
        if self.pos.y > screen_height: self.health = 0

    def collides_with(self, other):
        return (self.pos.x < other.x + other.width and
                self.pos.x + self.width > other.x and
                self.pos.y < other.y + other.height and
                self.pos.y + self.height > other.y)

class Platform:
    def __init__(self, x, y, width, height, color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 24
        self.vel_y = 0
        self.direction = 1
        self.speed = 2
        self.alive = True
        self.on_ground = False

    def update(self, platforms):
        if not self.alive: return
        self.vel_y += GRAVITY
        self.y += self.vel_y
        self.on_ground = False
        for p in platforms:
            if (self.x < p.x + p.width and self.x + self.width > p.x and
                self.y < p.y + p.height and self.y + self.height > p.y):
                if self.vel_y > 0:
                    self.y = p.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.y = p.y + p.height
                    self.vel_y = 0
        self.x += self.speed * self.direction
        for p in platforms:
            if (self.x < p.x + p.width and self.x + self.width > p.x and
                self.y < p.y + p.height and self.y + self.height > p.y):
                self.direction *= -1
                self.x += self.speed * self.direction
                break
        if self.on_ground:
            look_ahead_x = self.x + (self.width if self.direction > 0 else 0)
            has_ground = False
            for p in platforms:
                if p.x <= look_ahead_x <= p.x + p.width and p.y <= self.y + self.height + 5 <= p.y + p.height:
                    has_ground = True
                    break
            if not has_ground:
                self.direction *= -1
                self.x += self.speed * self.direction

class PiranhaPlant:
    def __init__(self, x, y):
        self.x = x + 12
        self.y = y
        self.width = 40
        self.height = 32
        self.offset = 0
        self.timer = 0
        self.state = "HIDDEN"

    def update(self):
        self.timer += 1
        if self.state == "HIDDEN":
            if self.timer > 100:
                self.state = "RISING"
                self.timer = 0
        elif self.state == "RISING":
            self.offset += 1
            if self.offset >= 45:
                self.state = "EXPOSED"
                self.timer = 0
        elif self.state == "EXPOSED":
            if self.timer > 100:
                self.state = "LOWERING"
                self.timer = 0
        elif self.state == "LOWERING":
            self.offset -= 1
            if self.offset <= 0:
                self.state = "HIDDEN"
                self.timer = 0

    def collides_with(self, player):
        if self.offset < 5: return False
        head_y = self.y - self.offset
        return (player.pos.x < self.x + self.width and
                player.pos.x + player.width > self.x and
                player.pos.y < head_y + self.height and
                player.pos.y + player.height > head_y)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.collected = False

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Mario: Rescue the Queen")
        
        # Initialize Full Screen
        self.root.attributes("-fullscreen", True)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height, bg=SKY_LIGHT, highlightthickness=0)
        self.canvas.pack()
        
        # Load Assets
        self.mario_img = create_pixel_image(MARIO_PIXELS, scale=3)
        self.turtle_img = create_pixel_image(TURTLE_PIXELS, scale=4)
        self.plant_img = create_pixel_image(PLANT_PIXELS, scale=5)
        self.princess_img = create_pixel_image(PRINCESS_PIXELS, scale=4)
        self.dirt_img = create_pixel_image(DIRT_PIXELS, scale=4)
        self.coin_img = create_pixel_image(COIN_PIXELS, scale=3)
        self.cloud_img = create_pixel_image(CLOUD_PIXELS, scale=10)
        
        self.camera_x = 0
        self.keys = {}
        self.state = "PLAYING"
        self.frame_count = 0
        self.cage_opened = False
        
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy()) # Exit game
        
        self.setup_level()
        self.game_loop()

    def setup_level(self):
        # Level segments with gaps (pits)
        h = self.screen_height
        self.platforms = [
            Platform(0, h - 64, 800, 64),
            Platform(950, h - 64, 1000, 64),
            Platform(2100, h - 64, 1800, 64),
            # Pipes
            Platform(400, h - 128, 64, 64, DARK_GREEN),
            Platform(1200, h - 160, 64, 96, DARK_GREEN),
            Platform(1800, h - 128, 64, 64, DARK_GREEN),
            Platform(2600, h - 192, 64, 128, DARK_GREEN),
            Platform(3200, h - 160, 64, 96, DARK_GREEN),
            # Bricks
            Platform(600, h - 200, 128, 32),
            Platform(1400, h - 300, 192, 32),
            Platform(2200, h - 200, 128, 32),
            Platform(2800, h - 300, 128, 32),
        ]
        
        self.plants = [
            PiranhaPlant(400, h - 128),
            PiranhaPlant(1800, h - 128),
            PiranhaPlant(3200, h - 160)
        ]
        
        self.queen_x = 3700
        self.queen_y = h - 64 - 48
        self.cage_rect = (self.queen_x - 10, self.queen_y - 10, 52, 60)

        self.player = Player(100, h - 150)
        self.enemies = [
            Enemy(700, h - 94),
            Enemy(1100, h - 94),
            Enemy(1500, h - 94),
            Enemy(2300, h - 94),
            Enemy(2900, h - 94)
        ]
        self.coins = [
            Coin(350, h - 250), Coin(650, h - 350), Coin(1250, h - 300), 
            Coin(2250, h - 300), Coin(2850, h - 400)
        ]
        self.clouds = [(i*500 + 100, 100 - (i%2)*50) for i in range(8)]
        self.cage_opened = False

    def key_press(self, event):
        key = event.keysym
        if key in ("space", "Up", "up"):
            if self.state == "PLAYING": self.player.jump()
            elif self.state in ("GAMEOVER", "VICTORY"): self.restart()
        if key in ("r", "R"): self.restart()
        self.keys[key] = True

    def key_release(self, event):
        self.keys[event.keysym] = False

    def restart(self):
        self.state = "PLAYING"
        self.camera_x = 0
        self.setup_level()

    def update(self):
        if self.state != "PLAYING": return
        
        self.player.update(self.platforms, self.keys, self.screen_height)
        for e in self.enemies: e.update(self.platforms)
        for p in self.plants: 
            p.update()
            if p.collides_with(self.player): self.player.health = 0
        
        target_camera_x = max(0, self.player.pos.x - self.screen_width / 2)
        if target_camera_x > self.camera_x: self.camera_x = target_camera_x
            
        for c in self.coins:
            if not c.collected and self.player.collides_with(c):
                c.collected = True
                self.player.score += 10
        for e in self.enemies:
            if e.alive and self.player.collides_with(e):
                if self.player.vel.y > 0 and self.player.pos.y + self.player.height < e.y + 15:
                    e.alive = False
                    self.player.vel.y = PLAYER_JUMP / 2
                    self.player.score += 50
                else: self.player.health = 0
        
        # Victory check
        if self.player.pos.x > self.queen_x - 100:
            if not self.cage_opened:
                self.cage_opened = True
                self.state = "VICTORY"
                self.keys = {}
            
        if self.player.health <= 0: self.state = "GAMEOVER"

    def draw(self):
        self.canvas.delete("all")
        self.frame_count += 1
        
        # Sky Gradient
        segments = 15
        seg_h = self.screen_height // segments
        for i in range(segments):
            color = self.interpolate_color(SKY_DEEP, SKY_LIGHT, i/segments)
            self.canvas.create_rectangle(0, i*seg_h, self.screen_width, (i+1)*seg_h, fill=color, outline="")
            
        for cx, cy in self.clouds:
            self.canvas.create_image(cx - self.camera_x * 0.5, cy, image=self.cloud_img, anchor="nw")
        
        for p in self.plants:
            self.canvas.create_image(p.x - self.camera_x, p.y - p.offset, image=self.plant_img, anchor="nw")

        for p in self.platforms:
            draw_x = p.x - self.camera_x
            if draw_x + p.width < 0 or draw_x > self.screen_width: continue
            if p.color:
                self.canvas.create_rectangle(draw_x, p.y, draw_x + p.width, p.y + p.height, fill=p.color, outline=BLACK, width=2)
                if p.height > 32:
                    self.canvas.create_rectangle(draw_x - 4, p.y, draw_x + p.width + 4, p.y + 20, fill=p.color, outline=BLACK, width=2)
            else:
                for tx in range(0, p.width, 32):
                    for ty in range(0, p.height, 32):
                        tile_x = draw_x + tx
                        if -32 <= tile_x <= self.screen_width:
                            self.canvas.create_image(tile_x, p.y + ty, image=self.dirt_img, anchor="nw")
        
        self.canvas.create_image(self.queen_x - self.camera_x, self.queen_y, image=self.princess_img, anchor="nw")
        if not self.cage_opened:
            x1, y1, w, h = self.cage_rect
            for bx in range(0, w + 1, 10):
                self.canvas.create_line(x1 + bx - self.camera_x, y1, x1 + bx - self.camera_x, y1 + h, fill=GRAY, width=3)
            self.canvas.create_rectangle(x1 - self.camera_x, y1, x1 + w - self.camera_x, y1 + h, outline=BLACK, width=2)

        for c in self.coins:
            if not c.collected:
                draw_x = c.x - self.camera_x
                if -24 <= draw_x <= self.screen_width:
                    self.canvas.create_image(draw_x, c.y + abs((self.frame_count // 10) % 4 - 2), image=self.coin_img, anchor="nw")
        for e in self.enemies:
            if e.alive:
                draw_x = e.x - self.camera_x
                if -32 <= draw_x <= self.screen_width:
                    self.canvas.create_image(draw_x, e.y, image=self.turtle_img, anchor="nw")
        
        self.canvas.create_image(self.player.pos.x - self.camera_x, self.player.pos.y, image=self.mario_img, anchor="nw")
        self.canvas.create_text(20, 20, anchor="nw", text=f"Score: {self.player.score}", font=("Courier", 24, "bold"), fill=WHITE)
        
        if self.state == "GAMEOVER":
            self.canvas.create_text(self.screen_width/2, self.screen_height/2, text="GAME OVER\nPress R to Restart\nEsc to Quit", font=("Courier", 40, "bold"), fill=RED, justify="center")
        elif self.state == "VICTORY":
            self.canvas.create_text(self.screen_width/2, self.screen_height/2, text=f"VICTORY!\nTHE QUEEN HAS BEEN RESCUED!\nScore: {self.player.score}\nPress R to Play Again\nEsc to Quit", font=("Courier", 30, "bold"), fill=YELLOW, justify="center")

    def interpolate_color(self, c1, c2, t):
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def game_loop(self):
        start = time.time()
        self.update(); self.draw()
        elapsed = time.time() - start
        self.root.after(max(1, int((FRAME_TIME - elapsed) * 1000)), self.game_loop)

if __name__ == "__main__":
    root = tk.Tk(); game = Game(root); root.mainloop()
