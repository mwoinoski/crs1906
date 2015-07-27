import pygame
from pygame.locals import *
import os, sys
from math import *
import random

if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

Screen = (800, 600)

pygame.display.set_caption("Asteroids - v.7.1.0 - Ian Mallett - 2008")
icon = pygame.Surface((1, 1));
icon.set_alpha(0);
pygame.display.set_icon(icon)
Surface = pygame.display.set_mode(Screen)

Explosions = []
Asteroids = []
PowerUps = []
Bullets = []
Bombs = []

Level = 0

Font = pygame.font.SysFont("Times New Roman", 8)
Font2 = pygame.font.SysFont("Times New Roman", 10)
Font3 = pygame.font.SysFont("Times New Roman", 16)

Clock = pygame.time.Clock()
TargetFPS = 50.0  # 200.0, 100.0, 50.0, 25.0, 13.0
IdealFPS = 200.0

import Images, Classes

Classes.init(Screen)

p1 = Classes.Player()


def Fire(direction):
    if direction == "Sides":
        Bullets.append(Classes.Bullet(p1, "Left Side", -p1.rotation))
        Bullets.append(Classes.Bullet(p1, "Right Side", -p1.rotation))
    elif direction == "Forwards":
        if p1.forward_fire_type == "Single Shot":
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation))
        elif p1.forward_fire_type == "Double Shot":
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation - 5))
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation + 5))
        elif p1.forward_fire_type == "Triple Shot":
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation))
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation - 10))
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation + 10))
        elif p1.forward_fire_type == "Quadruple Shot":
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation - 2))
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation + 2))
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation + 5))
            Bullets.append(Classes.Bullet(p1, direction, -p1.rotation - 5))
    elif direction == "Backwards":
        Bullets.append(Classes.Bullet(p1, direction, -p1.rotation))
    p1.weapon_reloading_time = p1.total_weapon_reload_time


def GetInput():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit();
            sys.exit()
    if key[K_SPACE]:
        if p1.weapon_reloading_time == 0 and p1.energy >= 2.5:
            Fire("Forwards")
            if p1.fire_direction == "Forwards, Backward":
                Fire("Backwards")
            elif p1.fire_direction == "Forwards, Sides":
                Fire("Sides")
            elif p1.fire_direction == "Forwards, Backwards, Sides":
                Fire("Sides")
                Fire("Backwards")
            p1.energy -= 2.5
    if key[K_b]:
        if p1.bomb_reload_time == 100 and p1.bomb_ammo >= 1:
            Bombs.append(Classes.Bomb(p1, Images.BombImage))
            p1.bomb_ammo -= 1
            p1.bomb_reload_time = 0
    if key[K_s] and p1.energy >= p1.shield_discharge_rate:
        p1.shielded = True
    else:
        p1.shielded = False
    if key[K_LEFT]:  p1.rotation += 1 * (IdealFPS / TargetFPS)
    if key[K_RIGHT]: p1.rotation -= 1 * (IdealFPS / TargetFPS)
    if key[K_UP]:
        p1.speed[0] -= p1.thrust * cos(radians(p1.rotation))
        p1.speed[1] -= p1.thrust * sin(radians(p1.rotation))
    if key[K_DOWN]:
        p1.speed[0] *= .99
        p1.speed[1] *= .99


def Move():
    # Self
    p1.position[0] += p1.speed[0]
    p1.position[1] += p1.speed[1]
    # Bullets
    for b in Bullets:
        b.position[0] += b.speed[0]
        b.position[1] += b.speed[1]
    # Bombs
    for b in Bombs:
        b.position[0] += b.speed[0]
        b.position[1] += b.speed[1]
    # Asteroids
    for a in Asteroids:
        a.position[0] += a.speed[0]
        a.position[1] += a.speed[1]
    # Power Ups
    for p in PowerUps:
        p.position[0] += 0.1 * cos(radians(p.rotate))
        p.position[1] += 0.1 * sin(radians(p.rotate))
        p.position[0] += p.speed[0]
        p.position[1] += p.speed[1]


def BreakAsteroid(a):
    Explosions.append(Classes.Explosion("Asteroid", a.size, a.position))
    if a.size == 1:
        add_object = random.choice(
            ["Powerup", False, False, False, False, False, False, False, False,
             False, False, False, False, False, False])
        if add_object == "Powerup":
            PowerUps.append(Classes.PowerUp(a.position))
    else:
        add_asteroid_size = a.size - 1
        if add_asteroid_size <= 0: add_asteroid_size = 1
        Asteroids.append(Classes.Asteroid(a.position[0], a.position[1],
                                          add_asteroid_size))
        Asteroids.append(Classes.Asteroid(a.position[0], a.position[1], 1))
        Asteroids.append(Classes.Asteroid(a.position[0], a.position[1], 1))
    Asteroids.remove(a)


def Die():
    global Level, Asteroids, Explosions, p1
    Explosions.append(Classes.Explosion("Self", 1, p1.position))
    p1.speed = [0.0, 0.0]
    for x in xrange(540):
        Move()
        Update()
        Draw()
    p1 = Classes.Player()
    Level = 0
    Asteroids = []
    Explosions = []


def NewLevel():
    global Level
    Level += 1
    for a in xrange(Level * 5):
        Asteroids.append(Classes.Asteroid())
    p1.energy = 100.0;
    p1.health = 100.0;
    p1.speed = [0.0, 0.0];
    PowerUps = []
    if p1.bomb_ammo < 5: p1.bomb_ammo += 1
    for a in Asteroids:
        asteroid_radius = a.get_radius()
        if sqrt(((a.position[0] - p1.position[0]) ** 2) + (
            (a.position[1] - p1.position[1]) ** 2)) <= asteroid_radius + 20 + 27:
            Asteroids.remove(a)


def CollisionDetect():
    # Start a new Level?
    if len(Asteroids) == 0:
        NewLevel()
    # Self
    if p1.position[0] > Screen[0]:
        p1.position[0] = p1.position[0] - Screen[0]
    elif p1.position[0] < 0:
        p1.position[0] = p1.position[0] + Screen[0]
    if p1.position[1] > Screen[1]:
        p1.position[1] = p1.position[1] - Screen[1]
    elif p1.position[1] < 0:
        p1.position[1] = p1.position[1] + Screen[1]
    if p1.energy < 0:  p1.energy = 0
    if p1.health < 0:  p1.health = 0; Die()
    # Bullets
    for b in Bullets:
        if b.position[0] > Screen[0]:
            b.position[0] = b.position[0] - Screen[0]
        elif b.position[0] < 0:
            b.position[0] = b.position[0] + Screen[0]
        if b.position[1] > Screen[1]:
            b.position[1] = b.position[1] - Screen[1]
        elif b.position[1] < 0:
            b.position[1] = b.position[1] + Screen[1]
    # Bombs
    for b in Bombs:
        if b.position[0] > Screen[0]:
            b.position[0] = b.position[0] - Screen[0]
        elif b.position[0] < 0:
            b.position[0] = b.position[0] + Screen[0]
        if b.position[1] > Screen[1]:
            b.position[1] = b.position[1] - Screen[1]
        elif b.position[1] < 0:
            b.position[1] = b.position[1] + Screen[1]
    # Asteroids
    for a in Asteroids:
        if a.position[0] > Screen[0]:
            a.position[0] = a.position[0] - Screen[0]
        elif a.position[0] < 0:
            a.position[0] = a.position[0] + Screen[0]
        if a.position[1] > Screen[1]:
            a.position[1] = a.position[1] - Screen[1]
        elif a.position[1] < 0:
            a.position[1] = a.position[1] + Screen[1]
        if a.stamina <= 0: BreakAsteroid(a)
    # Power Ups
    for p in PowerUps:
        if p.position[0] > Screen[0]:
            p.position[0] = p.position[0] - Screen[0]
        elif p.position[0] < 0:
            p.position[0] = p.position[0] + Screen[0]
        if p.position[1] > Screen[1]:
            p.position[1] = p.position[1] - Screen[1]
        elif p.position[1] < 0:
            p.position[1] = p.position[1] + Screen[1]
    # Asteroids/Self
    for a in Asteroids:
        AsteroidRadius = a.get_radius()
        XDiff = abs(a.position[0] - p1.position[0])
        if p1.shielded:
            if XDiff <= (AsteroidRadius / 2.0) + 37:
                YDiff = abs(a.position[1] - p1.position[1])
                if YDiff <= (AsteroidRadius / 2.0) + 37:
                    if (XDiff ** 2) + (YDiff ** 2) <= \
                            (((AsteroidRadius / 2.0) + 37) ** 2):
                        p1.energy -= 10
                        if p1.energy < 0:
                            p1.health += p1.energy
                        BreakAsteroid(a)
        else:
            if XDiff <= (AsteroidRadius / 2.0) + 27:
                YDiff = abs(a.position[1] - p1.position[1])
                if YDiff <= (AsteroidRadius / 2.0) + 27:
                    if (XDiff ** 2) + (YDiff ** 2) <= \
                            (((AsteroidRadius / 2.0) + 27) ** 2):
                        BreakAsteroid(a)
                        p1.being_hit = 7
                        p1.health -= a.size * 2
    # Asteroids/Bullets
    for a in Asteroids:
        AsteroidRadius = a.get_radius()
        for b in Bullets:
            XDiff = abs(a.position[0] - b.position[0])
            if XDiff <= (AsteroidRadius / 2.0) + 7:
                YDiff = abs(a.position[1] - b.position[1])
                if YDiff <= (AsteroidRadius / 2.0) + 7:
                    if (XDiff ** 2) + (YDiff ** 2) <= \
                            (((AsteroidRadius / 2.0) + 7) ** 2):  # 7 = bullet radius
                        a.stamina -= b.damage
                        a.being_hit = 7
                        Bullets.remove(b)
    # Asteroids/Bombs
    for a in Asteroids:
        AsteroidRadius = a.get_radius()
        for b in Bombs:
            XDiff = abs(a.position[0] - b.position[0])
            if XDiff <= (AsteroidRadius / 2.0) + 35:
                YDiff = abs(a.position[1] - b.position[1])
                if YDiff <= (AsteroidRadius / 2.0) + 35:
                    if (XDiff ** 2) + (YDiff ** 2) <= \
                            (((AsteroidRadius / 2.0) + 35) ** 2):  # 35 = bomb radius
                        a.stamina = 0
                        for a2 in Asteroids:
                            AsteroidRadius = a2.get_radius()
                            XDiff = abs(a2.position[0] - b.position[0])
                            if XDiff <= (AsteroidRadius / 2.0) + 150:
                                YDiff = abs(a2.position[1] - b.position[1])
                                if YDiff <= (AsteroidRadius / 2.0) + 150:
                                    if (XDiff ** 2) + (YDiff ** 2) <= \
                                            (((AsteroidRadius / 2.0) + 150) ** 2):
                                        a2.stamina = 0
                        Explosions.append(Classes.Explosion("Bomb", 1, b.position))
                        Bombs.remove(b)
    # PowerUps/Self
    for p in PowerUps:
        XDiff = abs(p.position[0] - p1.position[0])
        if p1.shielded:
            Radius = 8 + 37
        else:
            Radius = 8 + 27
        if XDiff <= Radius:
            YDiff = abs(p.position[1] - p1.position[1])
            if YDiff <= Radius:
                if (XDiff ** 2) + (YDiff ** 2) <= (Radius ** 2):
                    if p.type == "Weaponry":
                        upgrade_choice = random.choice(
                            ["Upgrade Single Double Triple Quadruple",
                             "Upgrade Direction of Fire",
                             "Upgrade Bullet Damage",
                             "Upgrade Bullet Reload Time",
                             "Upgrade Bullet Speed",
                             "Change Weapon Type"])
                        if upgrade_choice == "Upgrade Single Double Triple Quadruple":
                            if p1.forward_fire_type == "Single Shot":
                                p1.forward_fire_type = "Double Shot"
                            elif p1.forward_fire_type == "Double Shot":
                                p1.forward_fire_type = "Triple Shot"
                            elif p1.forward_fire_type == "Triple Shot":
                                p1.forward_fire_type = "Quadruple Shot"
                            else:
                                upgrade_choice = "Upgrade Direction of Fire"
                        if upgrade_choice == "Upgrade Direction of Fire":
                            if p1.fire_direction == "Forward":
                                upgrade_choice_2 = random.choice(
                                    ["Upgrade to Sides", "Upgrade to Backwards"])
                                if upgrade_choice_2 == "Upgrade to Sides":
                                    p1.fire_direction = "Forward, Sides"
                                elif upgrade_choice_2 == "Upgrade to Backwards":
                                    p1.fire_direction = "Forward, Backward"
                            elif p1.fire_direction == "Forward, Backward" or \
                                            p1.fire_direction == "Forward, Sides":
                                p1.fire_direction = "Forward, Backward, Sides"
                            else:
                                upgrade_choice = "Upgrade Bullet Damage"
                        if upgrade_choice == "Upgrade Bullet Damage":
                            if p1.bullet_damage < 10:
                                p1.bullet_damage += 1
                            else:
                                upgrade_choice = "Upgrade Bullet Reload Time"
                        if upgrade_choice == "Upgrade Bullet Reload Time":
                            if p1.total_weapon_reload_time > 10:
                                p1.total_weapon_reload_time -= 2
                            else:
                                upgrade_choice = "Upgrade Bullet Speed"
                        if upgrade_choice == "Upgrade Bullet Speed":
                            if p1.bullet_speed < 10:
                                p1.bullet_speed += 1
                            else:
                                upgrade_choice = "Change Weapon Type"
                        if upgrade_choice == "Change Weapon Type":
                            if p1.weapon_type == "Plasma Cannon":
                                p1.weapon_type = "Plasma Blast"
                            else:
                                p1.weapon_type = "Plasma Cannon"
                    elif p.type == "Shields":
                        p1.shield_discharge_rate *= 0.5
                    elif p.type == "Thrust":
                        if p1.thrust < 0.025:
                            p1.thrust += .0025
                    elif p.type == "Bomb":
                        if p1.bomb_ammo < 5:
                            p1.bomb_ammo += 1
                    PowerUps.remove(p)


def Update():
    # Self
    if p1.weapon_reloading_time > 0:
        p1.weapon_reloading_time -= 1
    else:
        p1.weapon_reloading_time = 0
    if p1.bomb_reload_time < 100:
        p1.bomb_reload_time += 0.25
    else:
        p1.bomb_reload_time = 100
    if p1.shielded: p1.energy -= p1.shield_discharge_rate
    p1.energy += float(p1.energy_recharge_rate)
    if p1.energy > 100.0: p1.energy = 100.0
    if p1.being_hit > 0: p1.being_hit -= 1
    # Bullets
    for b in Bullets:
        b.time += 1
        if b.time > 300:
            Bullets.remove(b)
    # Asteroids
    for a in Asteroids:
        a.rotation += a.rotate_speed
        if a.rotation > 360.0:
            a.rotation -= 360.0
        elif a.rotation < -360.0:
            a.rotation += 360.0
        if a.being_hit > 0:
            a.being_hit -= 1
        else:
            a.being_hit = 0
    # Power Ups
    for p in PowerUps:
        p.frame += 1
        if p.type != "Bomb":
            if p.frame > 8:   p.frame = 1
        else:
            if p.frame > 180: p.frame = 1
        p.time += 1
        if p.time >= 2000:
            PowerUps.remove(p)
        p.rotate += 2
    # Explosions
    for e in Explosions:
        e.frame += 1


def rndint(number):
    return int(round(number))


def Draw():
    # Clear
    Surface.fill((0, 0, 0))
    # Self
    ToDraw = True
    for e in Explosions:
        if e.type == "Self": ToDraw = False; break
    if ToDraw:
        if not p1.being_hit:
            ShipImageRotated = pygame.transform.rotozoom(
                Images.ShipImages[0], p1.rotation, 1.0)
        else:
            ShipImageRotated = pygame.transform.rotozoom(
                Images.ShipImages[1], p1.rotation, 1.0)
        height = ShipImageRotated.get_height() / 2.0
        width = ShipImageRotated.get_width() / 2.0
        BlitPos = [rndint(p1.position[0] - width), rndint(p1.position[1] + height)]
        Surface.blit(ShipImageRotated, (BlitPos[0], Screen[1] - BlitPos[1]))
        if p1.shielded:
            Surface.blit(Images.ShieldImage,
                         (p1.position[0] - 38, Screen[1] -(p1.position[1] + 38)))
    # Bullets
    for b in Bullets:
        if b.type == "Plasma Cannon":
            BulletImage = Images.BulletImages[0]
        elif b.type == "Plasma Blast":
            BulletImage = Images.BulletImages[1]
        Surface.blit(BulletImage, (rndint(b.position[0] - 11),
                                   Screen[1] - rndint(b.position[1] + 11)))
    # Bombs
    for b in Bombs:
        Surface.blit(b.image, (b.position[0] - b.width,
                               Screen[1] - rndint(b.position[1] + b.height)))
    # Power Ups
    for p in PowerUps:
        if p.type == "Weaponry":
            Surface.blit(Images.Green_Power_Up_Frames[p.frame - 1],
                         (p.position[0] - 8, Screen[1] - (p.position[1] + 8)))
        elif p.type == "Shields":
            Surface.blit(Images.Blue_Power_Up_Frames[p.frame - 1],
                         (p.position[0] - 8, Screen[1] - (p.position[1] + 8)))
        elif p.type == "Thrust":
            Surface.blit(Images.Red_Power_Up_Frames[p.frame - 1],
                         (p.position[0] - 8, Screen[1] - (p.position[1] + 8)))
        elif p.type == "Bomb":
            Surface.blit(Images.BombPowerUpImages[int((p.frame / 12.0) - 1)],
                         (p.position[0] - 27, Screen[1] - rndint(p.position[1] + 18)))
    # Asteroids
    for a in Asteroids:
        if not a.being_hit:
            image = Images.AsteroidImages[4 - (a.size - 1)]
        else:
            image = Images.RedAsteroidImages[4 - (a.size - 1)]
        image = pygame.transform.rotozoom(image, a.rotation, 1.0)
        Surface.blit(image, (rndint(a.position[0] - (image.get_width() / 2.0)),
                             Screen[1] - rndint(a.position[1] +
                                                (image.get_height() / 2.0))))
    # Explosions
    for e in Explosions:
        try:
            if e.type == "Asteroid":
                index = int(e.frame / 4.0) - 1
                if index >= 17:
                    raise IndexError
                if e.size == 5:
                    Surface.blit(Images.Asteroid_Explosion_Frames[index],
                                 (rndint(e.position[0] - 71),
                                  rndint(Screen[1] - (e.position[1] + 100))))
                elif e.size == 4:
                    Surface.blit(Images.Asteroid_Explosion_Frames[index + 17],
                                 (rndint(e.position[0] - 54),
                                  rndint(Screen[1] - (e.position[1] + 75))))
                elif e.size == 3:
                    Surface.blit(Images.Asteroid_Explosion_Frames[index + 34],
                                 (rndint(e.position[0] - 36),
                                  rndint(Screen[1] - (e.position[1] + 50))))
                elif e.size == 2:
                    Surface.blit(Images.Asteroid_Explosion_Frames[index + 51],
                                 (rndint(e.position[0] - 27),
                                  rndint(Screen[1] - (e.position[1] + 38))))
                else:
                    Surface.blit(Images.Asteroid_Explosion_Frames[index + 68],
                                 (rndint(e.position[0] - 18),
                                  rndint(Screen[1] - (e.position[1] + 25))))
            if e.type == "Bomb":
                Surface.blit(Images.Bomb_Explosion_Frames[(e.frame / 12) - 1],
                    (e.position[0] - 90, Screen[1] - (e.position[1] + 68)))
            if e.type == "Self":
                Surface.blit(Images.Self_Explosion_Frames[e.frame / 27],
                    (e.position[0] - 128, Screen[1] - (e.position[1] + 96)))
        except:
            Explosions.remove(e)
            # HUD: Basic Info.
            # Energy Bar
    try:
        red_amt = rndint(((100 - p1.energy) / 100.0) * 255.0)
        green_amt = rndint((p1.energy / 100.0) * 255.0)
        energy_bar_surface = pygame.Surface((rndint(p1.energy), 7))
        energy_bar_surface.set_alpha(100)
        energy_bar_surface.fill((red_amt, green_amt, 0))
        Surface.blit(energy_bar_surface, (5, 5))
    except:
        pass
    pygame.draw.rect(Surface, (100, 100, 100), (4, 4, 102, 9), 1)
    percent_e = Font.render(str(rndint(p1.energy)) + "% Energy", True,
                            (200, 150, 150))
    width = percent_e.get_width()
    Surface.blit(percent_e, (55 - (width / 2.0), 12))
    # Health Bar
    try:
        red_amt = rndint(((100 - p1.health) / 100.0) * 255.0)
        green_amt = rndint((p1.health / 100.0) * 255.0)
        health_bar_surface = pygame.Surface((rndint(p1.health), 7))
        health_bar_surface.set_alpha(100)
        health_bar_surface.fill((red_amt, green_amt, 0))
        Surface.blit(health_bar_surface, (5, 25))
    except:
        pass
    pygame.draw.rect(Surface, (100, 100, 100), (4, 24, 102, 9), 1)
    percent_h = Font.render(str(rndint(p1.health)) + "% Health", True,
                            (200, 150, 150))
    width = percent_h.get_width()
    Surface.blit(percent_h, (55 - (width / 2.0), 32))
    # Bombs
    Surface.blit(Images.HudBomb[1], (110, 7))
    Surface.blit(Images.HudBomb[1], (137, 7))
    Surface.blit(Images.HudBomb[1], (164, 7))
    Surface.blit(Images.HudBomb[1], (191, 7))
    Surface.blit(Images.HudBomb[1], (218, 7))
    if p1.bomb_ammo > 0:  # 1-5
        Surface.blit(Images.HudBomb[0], (110, 7))
        if p1.bomb_ammo > 1:  # 2-5
            Surface.blit(Images.HudBomb[0], (137, 7))
            if p1.bomb_ammo > 2:  # 3-5
                Surface.blit(Images.HudBomb[0], (164, 7))
                if p1.bomb_ammo > 3:  # 4-5
                    Surface.blit(Images.HudBomb[0], (191, 7))
                    if p1.bomb_ammo > 4:  # 5
                        Surface.blit(Images.HudBomb[0], (218, 7))
    red_amt = rndint(((100 - p1.bomb_reload_time) / 100.0) * 255.0)
    green_amt = rndint((p1.bomb_reload_time / 100.0) * 255.0)
    bomb_reload_bar_surface = pygame.Surface(
        (rndint(p1.bomb_reload_time), 4))
    bomb_reload_bar_surface.set_alpha(100)
    bomb_reload_bar_surface.fill((red_amt, green_amt, 0))
    Surface.blit(bomb_reload_bar_surface, (127, 28))
    pygame.draw.rect(Surface, (100, 100, 100), (126, 27, 102, 6), 1)
    # HUD: Stats
    #   Ship Display
    Surface.blit(Images.ShipImages[2], (Screen[0] - 62, (Screen[1] / 2) - 170))
    if p1.forward_fire_type == "Single Shot":
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 44, (Screen[1] / 2) - 165))
    elif p1.forward_fire_type == "Double Shot":
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 49, (Screen[1] / 2) - 165))
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 39, (Screen[1] / 2) - 165))
    elif p1.forward_fire_type == "Triple Shot":
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 44, (Screen[1] / 2) - 165))
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 55, (Screen[1] / 2) - 165))
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 33, (Screen[1] / 2) - 165))
    elif p1.forward_fire_type == "Quadruple Shot":
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 62, (Screen[1] / 2) - 160))
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 26, (Screen[1] / 2) - 160))
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 53, (Screen[1] / 2) - 165))
        Surface.blit(Images.FireDisplay[0],
                     (Screen[0] - 35, (Screen[1] / 2) - 165))
    if p1.fire_direction == "Forward, Backward":
        Surface.blit(Images.FireDisplay[1],
                     (Screen[0] - 44, (Screen[1] / 2) - 120))
    elif p1.fire_direction == "Forward, Sides":
        Surface.blit(Images.FireDisplay[2],
                     (Screen[0] - 58, (Screen[1] / 2) - 145))
        Surface.blit(Images.FireDisplay[3],
                     (Screen[0] - 19, (Screen[1] / 2) - 145))
    elif p1.fire_direction == "Forward, Backward, Sides":
        Surface.blit(Images.FireDisplay[1],
                     (Screen[0] - 44, (Screen[1] / 2) - 120))
        Surface.blit(Images.FireDisplay[2],
                     (Screen[0] - 58, (Screen[1] / 2) - 145))
        Surface.blit(Images.FireDisplay[3],
                     (Screen[0] - 19, (Screen[1] / 2) - 145))
    if p1.weapon_type == "Plasma Cannon":
        weapon_type = Font2.render("Plasma Cannon", True, (200, 200, 200))
    else:
        weapon_type = Font2.render("Plasma Blast", True, (200, 200, 200))
    Surface.blit(weapon_type, (Screen[0] - 62, (Screen[1] / 2) - 115))
    #   Engines
    #       Thrust
    try:
        # 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225, 0.025
        thrust_rate = p1.thrust
        percent_thrust = (thrust_rate - 0.0075) / 0.02
        thrust_stat_bar_length = percent_thrust * 200.0
        thrust_stat_bar = pygame.Surface((7, rndint(thrust_stat_bar_length)))
        thrust_stat_bar.set_alpha(100)
        thrust_stat_bar.fill((255, 0, 0))
        translate_down = 200 - (thrust_stat_bar_length - 1)
        Surface.blit(thrust_stat_bar, (Screen[0] - 12, (Screen[1] / 2) - 100 +
                                       translate_down))
    except:
        pass
    pygame.draw.rect(Surface, (100, 100, 100),
                     (Screen[0] - 13, (Screen[1] / 2) - 101, 9, 202), 1)
    info = Font2.render(str(round(10000 * thrust_rate, 2)) + " Kn Thrust",
                        True, (200, 150, 150))
    info = pygame.transform.rotate(info, 90)
    Surface.blit(info, (Screen[0] - 16, (Screen[1] / 2) + 110))
    #   Shields
    #       Energy Discharge Rate
    try:
        discharge_rate = p1.shield_discharge_rate  # 0.2, 0.1, 0.05, 0.025, 0.0125, etc.
        percent_discharge = discharge_rate / 0.2  # 1, .5, .25, .125, etc.
        shields_stat_bar_length = (1 - percent_discharge) * 200
        shields_stat_bar = pygame.Surface((7, rndint(shields_stat_bar_length)))
        shields_stat_bar.set_alpha(100)
        shields_stat_bar.fill((0, 0, 255))
        translate_down = 200 - (shields_stat_bar_length - 1)
        Surface.blit(shields_stat_bar, (Screen[0] - 24,
                                        (Screen[1] / 2) - 100 + translate_down))
    except:
        pass
    pygame.draw.rect(Surface, (100, 100, 100),
                     (Screen[0] - 25, (Screen[1] / 2) - 101, 9, 202), 1)
    info = Font2.render(str(round((shields_stat_bar_length / 2.0), 2)) +
                        "% Shield Efficiency", True, (200, 150, 150))
    info = pygame.transform.rotate(info, 90)
    Surface.blit(info, (Screen[0] - 28, (Screen[1] / 2) + 110))
    #   Weaponry
    #       Fire Rate
    # 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13,
    # 12, 11, 10
    fire_rate = p1.total_weapon_reload_time
    fire_rate_multiplier = (20 - (fire_rate - 10)) / 20.0
    fire_rate_stat_bar_length = 200 * fire_rate_multiplier
    fire_rate_stat_bar = pygame.Surface((7, fire_rate_stat_bar_length))
    fire_rate_stat_bar.set_alpha(100)
    fire_rate_stat_bar.fill((0, 255, 0))
    translate_down = 200 - fire_rate_stat_bar_length
    Surface.blit(fire_rate_stat_bar, (Screen[0] - 36,
                                      (Screen[1] / 2) - 100 + translate_down))
    pygame.draw.rect(Surface, (100, 100, 100),
                     (Screen[0] - 37, (Screen[1] / 2) - 101, 9, 202), 1)
    info = Font2.render(str(fire_rate) + " Ms Reload Time", True,
                        (200, 150, 150))
    info = pygame.transform.rotate(info, 90)
    Surface.blit(info, (Screen[0] - 40, (Screen[1] / 2) + 110))
    #       Fire Speed
    fire_speed = p1.bullet_speed
    fire_speed_percentage = fire_speed / 10.0
    fire_speed_stat_bar_length = rndint(fire_speed_percentage * 200.0)
    fire_speed_stat_bar = pygame.Surface((7, fire_speed_stat_bar_length))
    fire_speed_stat_bar.set_alpha(100)
    fire_speed_stat_bar.fill((0, 255, 0))
    translate_down = 200 - fire_speed_stat_bar_length
    Surface.blit(fire_speed_stat_bar, (Screen[0] - 48,
                                       (Screen[1] / 2) - 100 + translate_down))
    pygame.draw.rect(Surface, (100, 100, 100),
                     (Screen[0] - 49, (Screen[1] / 2) - 101, 9, 202), 1)
    info = Font2.render(str(fire_speed) + " m/s bullet speed", True,
                        (200, 150, 150))
    info = pygame.transform.rotate(info, 90)
    Surface.blit(info, (Screen[0] - 52, (Screen[1] / 2) + 110))
    #       Fire Damage
    fire_damage = p1.bullet_damage
    fire_damage_percentage = fire_damage / 10.0
    fire_damage_stat_bar_length = rndint(fire_damage_percentage * 200.0)
    fire_damage_stat_bar = pygame.Surface((7, fire_speed_stat_bar_length))
    fire_damage_stat_bar.set_alpha(100)
    fire_damage_stat_bar.fill((0, 255, 0))
    translate_down = 200 - fire_speed_stat_bar_length
    Surface.blit(fire_damage_stat_bar, (Screen[0] - 60,
                                        (Screen[1] / 2) - 100 + translate_down))
    pygame.draw.rect(Surface, (100, 100, 100), (Screen[0] - 61,
                                                (Screen[1] / 2) - 101, 9, 202), 1)
    info = Font2.render(str(fire_speed) + "X bullet damage factor", True,
                        (200, 150, 150))
    info = pygame.transform.rotate(info, 90)
    Surface.blit(info, (Screen[0] - 64, (Screen[1] / 2) + 110))
    #   Level
    LevelInfoText = Font3.render("Level " + str(Level), True, (150, 150, 150))
    Surface.blit(LevelInfoText, ((Screen[0] / 2.0) -
                                 (LevelInfoText.get_width() / 2.0), 5))
    # Flip
    pygame.display.flip()


def main():
    while True:
        update_func_scalar = IdealFPS / TargetFPS
        GetInput()
        for x in xrange(int(round(update_func_scalar))):
            Move()
            CollisionDetect()
            Update()
        Draw()
        Clock.tick(TargetFPS)


if __name__ == '__main__':
    main()
