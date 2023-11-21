import sys
import math
import random
from scripts.utils import load_img, load_images, Animation, draw_text
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark

import  pygame

class Game:
    def __init__(self):
        pygame.init()

        self.font = pygame.font.Font('game_assets\\font\\samurai-blast-font\\SamuraiBlast-YznGj.ttf', 25)
        self.sfont = pygame.font.Font('game_assets\\font\\samurai-blast-font\\SamuraiBlast-YznGj.ttf', 20)

        pygame.display.set_caption('PyNinja Game')
        self.screen = pygame.display.set_mode((640,480))
        self.display = pygame.Surface((320,240))
        self.clock = pygame.time.Clock()
        self.movement = [False , False]

        self.assets = {
            'bg' : load_img('background/background.png'),
            'play': load_img('settings/start.png'),
            'options': load_img('settings/options.png'),
            'decor': load_images('deco'),
            'grass': load_images('dirt'),
            'stone': load_images('stone'),
            'util': load_images('util'),
            'clouds' : load_images('cloud'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'weapons': Animation(load_images('weapon'), img_dur=2),
            'projectile': load_img('projectile/01_arrow.png')
            
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('game_assets/audio/jump.wav'),
            'dash': pygame.mixer.Sound('game_assets/audio/dash.wav'),
            'hit': pygame.mixer.Sound('game_assets/audio/hit.wav'),
            'shoot': pygame.mixer.Sound('game_assets/audio/shoot.wav'),
            'ambience': pygame.mixer.Sound('game_assets/audio/ambience.wav'),
        }
        
        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)

        print(self.assets)

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8,15))

        self.tilemap = Tilemap(self, tile_size=16)

        self.screen_shake = 0

        self.level = 0


    def load_level(self, map_id):
            self.tilemap.load('maps/lvl' + str(map_id) + '.json')
                
            self.enemies = []
            for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
                if spawner['variant'] == 0:
                    self.player.pos = spawner['pos']
                else:
                    self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
                
            self.projectiles = []
            self.particles = []
            self.sparks = []
            
            self.scroll = [0, 0]
            self.dead = 0
            self.transition = -30

    click =False

    def run(self):
        pygame.mixer.music.load('game_assets/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        while True:
            self.display.fill((113, 7, 166))

            draw_text('Ninja Legends', self.font, (227, 119, 25), self.display, 70, 70)

            mx, my = pygame.mouse.get_pos()

            button1 = self.assets['play'].get_rect()
            button1.x = 140
            button1.y = 120
            self.display.blit(self.assets['play'], button1)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if  event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            if button1.collidepoint((mx / 2,my / 2)):
                if click:
                    print(1)
                    self.play()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

    def play(self):
        pygame.mixer.music.load('game_assets/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        running = True
        while running:
            self.display.fill((113, 7, 166))

            draw_text('LEVELS', self.font, (227, 119, 25), self.display, 115, 30)

            bttn1rect = draw_text('1', self.sfont, (240, 66, 50), self.display, 50, 80)

            bttn2rect = draw_text('2', self.sfont, (240, 66, 50), self.display, 160, 80)

            bttn3rect = draw_text('3', self.sfont, (240, 66, 50), self.display, 270, 80)
            
            mx, my = pygame.mouse.get_pos()

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if  event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            if bttn1rect.collidepoint((mx / 2,my / 2)):
                if click:
                    print(1)
                    self.lvl1(1)
            if bttn2rect.collidepoint((mx/2, my/2)):
                if click:
                    print(2)
                    self.lvl1(2)
            if bttn3rect.collidepoint((mx/2, my/2)):
                if click:
                    print(3)
                    self.lvl1(3)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

    def options(self):
        pygame.mixer.music.load('game_assets/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        running = True
        while running:
            self.display.fill((56, 193, 242))

            draw_text('SETTINGS', self.font, (240, 66, 50), self.display, 100, 30)

            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if  event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

    def lvl1(self, lvl):
        pygame.mixer.music.load('game_assets/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        running = True
        self.level = lvl
        self.load_level(self.level)
        while running:
            self.display.fill((56, 193, 242))
            self.display.blit(self.assets['bg'], (0, 0))

            self.screen_shake = max(0, self.screen_shake-1)

            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, 3)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead >= 10 :
                    self.transition = min(30, self.transition +1)
                if self.dead > 40:
                    self.load_level(self.level)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_width() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset= render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
                
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.sfx['hit'].play()
                        self.screen_shake = max(16, self.screen_shake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))

            #print(self.tilemap.physics_rects_around (self.player.pos ))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)
            
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jump():
                            self.sfx['jump'].play()
                    if event.key == pygame.K_x:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if  event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            screen_shake_offset = (random.random() * self.screen_shake - self.screen_shake / 2, random.random() * self.screen_shake - self.screen_shake / 2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screen_shake_offset)
            pygame.display.update()
            self.clock.tick(60)

Game().run()