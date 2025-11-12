import pyxel
import copy
import time
from ennemy import *
from scores import * 
from maps import *
from power_ups import *


class Game():
    def __init__(self):
        self.ennemi = Ennemi()
        self.powerups = Powerups()
        self.state = "pseudo" #menu ou jeu ou leaderboard ou pseudo ou help
        self.TITLE = "Tank80"
        self.WIDHT = 256 #240
        self.HEIGHT = 256 #240
        self.CASE = 1
        self.FPS = 10 #10

        self.frame = 0
        self.frame2 = 0
        self.frame3 = 0
        self.frame4 = 0

        self.forme_bouclier = 1 #1 ou 2  0-96/16-96
        self.stopwatch = False
        self.stopwatch_timer = 0
        self.base_invincible = False
        self.base_invincible_timer = 0

        self.frame_tank = 0
        self.modele_tank = 1 #1 ou 2
        self.etat_eau = 1 #1 ou 2

        self.nb_max_tank_ennemi = 5
        self.level = 1
        self.direction = "h" #g, d, h, b

        self.taille_tank = 16
        self.ROWS = len(map1)
        self.COLS = len(map1[0])
        self.obstacles = [1, 2, 4, [9, "h"], [9, "b"], [9, "g"], [9, "d"]]

        self.nb_tank_a_eliminer = 20 #20
        self.tank_eliminer = 0

        self.old_life = self.ennemi.vies

        self.map1 = copy.deepcopy(map1)            
        self.map2 = copy.deepcopy(map2)
        self.map3 = copy.deepcopy(map3)
        self.map4 = copy.deepcopy(map4)
        self.map5 = copy.deepcopy(map5)
        
        self.map1copy = copy.deepcopy(self.map1)
        self.map2copy = copy.deepcopy(self.map2)
        self.map3copy = copy.deepcopy(self.map3)
        self.map4copy = copy.deepcopy(self.map4)
        self.map5copy = copy.deepcopy(self.map5)
        self.original_maps = [self.map1, self.map2, self.map3, self.map4, self.map5]
        self.maps = [self.map1copy, self.map2copy, self.map3copy, self.map4copy, self.map5copy]

        self.pseudo = "Unknown Player"
        self.score = 0

        #menu
        self.direction_menu = "+"
        self.x_menu = 115
        self.choix = 1

        self.old_map = [row[:] for row in first_old_map] 

        self.jeu = False

        self.x_tank = 64
        self.y_tank = 224

        self.tank_speed = 4
        self.tirs_speed = 8

        self.tirs = []

        self.y_game_over = 260
        self.game_over_bool = False

        self.saved = False
        self.level_screen_bool = False

        self.bouclier_bool = False

        pyxel.init(self.WIDHT, self.HEIGHT, title=self.TITLE, fps=self.FPS)
        pyxel.load("assets.pyxres")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)


    def level_screen(self):
            pyxel.cls(13)
            pyxel.text(100, 120, f"Stage {self.level}", 0)
            pyxel.flip()  # forcer l'affichage immédiat
            time.sleep(3)
            self.level_screen_bool = False
        
    def add_explosion(self, x, y, type_):
        """
        type_ = "tir"  -> 3 frames
        type_ = "tank" -> 5 frames
        """
        self.ennemi.explosions.append([x, y, 0, type_])


    def explosion_animation(self):
        nouvelles = []

        for x, y, frame, type_ in self.ennemi.explosions:
            if type_ == "tir":
                if frame < 3:
                    nouvelles.append([x, y, frame + 1, type_])
                else:
                    self.redessiner_apres_explosion(x, y, self.maps[self.level-1])

            elif type_ == "tank":
                if frame < 5:
                    nouvelles.append([x, y, frame + 1, type_])
                else:
                    map_ = self.maps[self.level-1]
                    self.redessiner_apres_explosion(x,     y,     map_)
                    self.redessiner_apres_explosion(x+16,  y,     map_)
                    self.redessiner_apres_explosion(x,     y+16,  map_)
                    self.redessiner_apres_explosion(x+16,  y+16,  map_)

        self.ennemi.explosions = nouvelles


    def draw_explosions(self):
        for x, y, frame, type_ in self.ennemi.explosions:

            if type_ == "tir":
                if frame == 0:
                    px, py = 160, 16
                elif frame == 1:
                    px, py = 176, 16
                else:
                    px, py = 192, 16

                pyxel.blt(x, y, 0, px, py, 16, 16, colkey=0)


            elif type_ == "tank":

                if frame == 0:
                    px, py = 160, 16
                    pyxel.blt(x, y, 0, px, py, 16, 16, colkey=0)

                elif frame == 1:
                    px, py = 176, 16
                    pyxel.blt(x, y, 0, px, py, 16, 16, colkey=0)

                elif frame == 2:
                    px, py = 192, 16
                    pyxel.blt(x, y, 0, px, py, 16, 16, colkey=0)

                elif frame == 3:
                    px, py = 208, 16
                    pyxel.blt(x,     y,     0, px,     py,     16, 16, colkey=0)
                    pyxel.blt(x+16,  y,     0, px+16,  py,     16, 16, colkey=0)
                    pyxel.blt(x,     y+16,  0, px,     py+16,  16, 16, colkey=0)
                    pyxel.blt(x+16,  y+16,  0, px+16,  py+16,  16, 16, colkey=0)

                elif frame == 4:
                    px, py = 80, 48
                    pyxel.blt(x,     y,     0, px,     py,     16, 16, colkey=0)
                    pyxel.blt(x+16,  y,     0, px+16,  py,     16, 16, colkey=0)
                    pyxel.blt(x,     y+16,  0, px,     py+16,  16, 16, colkey=0)
                    pyxel.blt(x+16,  y+16,  0, px+16,  py+16,  16, 16, colkey=0)


    def redessiner_apres_explosion(self, x, y, map_):
        size = 32
        for dy in range(0, size, 16):
            for dx in range(0, size, 16):

                tx = (x + dx) // 16
                ty = (y + dy) // 16

                if (
                    tx < 0 or
                    ty < 0 or
                    ty >= len(map_) or
                    tx >= len(map_[0])
                ):
                    continue

                tile = map_[ty][tx]

                pyxel.rect(tx*16, ty*16, 16, 16, 0)

                if tile == 1:
                    pyxel.blt(tx*16, ty*16, 0, 16, 0, 16, 16)
                elif tile == 2:
                    pyxel.blt(tx*16, ty*16, 0, 48, 0, 16, 16)
                elif tile == 4:
                    pyxel.blt(tx*16, ty*16, 0, 128, 0, 16, 16)
                elif tile == 10:
                    pyxel.blt(tx*16, ty*16, 0, 128, 16, 16, 16)
                elif tile == 3:
                    pyxel.blt(tx*16, ty*16, 0, 96, 0, 16, 16)
                elif tile == 5:
                    if self.etat_eau == 1:
                        pyxel.blt(tx*16, ty*16, 0, 0, 32, 16, 16)
                    else:
                        pyxel.blt(tx*16, ty*16, 0, 96, 16, 16, 16)
                elif isinstance(tile, list):
                    d = tile[1]
                    if d == "h":
                        pyxel.blt(tx*16, ty*16, 0, 112, 0, 16, 16)
                    elif d == "b":
                        pyxel.blt(tx*16, ty*16, 0, 112, 16, 16, 16)
                    elif d == "g":
                        pyxel.blt(tx*16, ty*16, 0, 144, 0, 16, 16)
                    elif d == "d":
                        pyxel.blt(tx*16, ty*16, 0, 144, 16, 16, 16)


    def rejouer(self):
        self.map1copy = copy.deepcopy(self.map1)
        self.map2copy = copy.deepcopy(self.map2)
        self.map3copy = copy.deepcopy(self.map3)
        self.map4copy = copy.deepcopy(self.map4)
        self.map5copy = copy.deepcopy(self.map5)
        self.maps = [self.map1copy, self.map2copy, self.map3copy, self.map4copy, self.map5copy]

        self.level = 1
        self.score = 0
        self.tirs = []

        self.ennemi.nb_tank_ennemi = 0
        self.ennemi.tanks_position = []
        self.ennemi.tirs_ennemi = []
        self.tank_eliminer = 0

        self.saved = False

        self.ennemi.vies = 3
        self.old_life = self.ennemi.vies

        self.x_tank = position_tank[self.level-1][0]
        self.y_tank = position_tank[self.level-1][1]
        self.old_x_tank = position_tank[self.level-1][0]
        self.old_y_tank = position_tank[self.level-1][1]

        self.direction = "h"
        self.old_direction = self.direction

        self.old_map = [row[:] for row in first_old_map]

        self.level_screen() 
        self.bouclier_bool = True 


    def level_up(self):
        if len(self.maps) >= (self.level + 1): #Pour s'arreter au niveau max -> depend du nombre de map
            self.level += 1
            self.tirs = []

            self.nb_tank_ennemi = 0
            self.ennemi.nb_tank_ennemi = 0
            self.ennemi.tanks_position = []
            self.ennemi.tirs_ennemi = []

            self.direction = "h"
            self.old_direction = self.direction

            self.x_tank = position_tank[self.level-1][0]
            self.y_tank = position_tank[self.level-1][1]
            self.old_x_tank = position_tank[self.level-1][0]
            self.old_y_tank = position_tank[self.level-1][1]

            self.old_map = [row[:] for row in first_old_map] 

            self.level_screen()  

    def animation_eau(self):
        if self.frame4 >= 5:
            self.frame4 = 0
            if self.etat_eau == 1:
                self.etat_eau = 2
            else:
                self.etat_eau = 1
        else:
            self.frame4 +=1

    def bouclier(self, time):
        if self.frame3 < self.FPS * time:
            self.frame3 += 1
            if self.frame3 % 3 == 0:
                self.forme_bouclier = 1 if self.forme_bouclier == 2 else 2
        else:
            self.frame3 = 0
            self.bouclier_bool = False


    def joueur_touché(self):
        if self.bouclier_bool is False:
            self.x_tank = position_tank[self.level-1][0]
            self.y_tank = position_tank[self.level-1][1]
            self.joueur_touché_bool = True
            self.bouclier_bool = True   
            self.frame3 = 0   

    def game_over(self):
        if self.y_game_over >= 128:
            self.y_game_over -= 8
        else:
            self.frame2 += 1
            if self.frame2 > 10:
                self.state = "menu"
                self.y_game_over = 260
                self.frame2 = 0
                self.game_over_bool = False
                self.saved = False

    def est_accesible(self, x_cible, y_cible, map_):
        taille_tank = 16
        marge = 2
        ennemis = self.ennemi

        ROWS, COLS = len(map_), len(map_[0])

        if not (0 <= x_cible < COLS * taille_tank and 0 <= y_cible < ROWS * taille_tank):
            return False

        for ty in range((y_cible + marge) // taille_tank, (y_cible + taille_tank - marge - 1) // taille_tank + 1):
            for tx in range((x_cible + marge) // taille_tank, (x_cible + taille_tank - marge - 1) // taille_tank + 1):

                if ty < 0 or ty >= ROWS or tx < 0 or tx >= COLS:
                    return False

                case = map_[ty][tx]


                if case in (1, 2, 4, 5):
                    return False
                elif isinstance(case, list) and case[0] == 9:
                    bx = tx * taille_tank
                    by = ty * taille_tank

                    if case[1] == "h": 
                        bx1, by1 = bx, by
                        bx2, by2 = bx + taille_tank, by + taille_tank//2
                    elif case[1] == "b":  
                        bx1, by1 = bx, by + taille_tank//2
                        bx2, by2 = bx + taille_tank, by + taille_tank
                    elif case[1] == "g":  
                        bx1, by1 = bx, by
                        bx2, by2 = bx + taille_tank//2, by + taille_tank
                    elif case[1] == "d": 
                        bx1, by1 = bx + taille_tank//2, by
                        bx2, by2 = bx + taille_tank, by + taille_tank

                    if not (x_cible + taille_tank <= bx1 or x_cible >= bx2 or
                            y_cible + taille_tank <= by1 or y_cible >= by2):
                        return False


        for (direction, xe, ye) in ennemis.tanks_position:
            if not (x_cible + taille_tank <= xe or x_cible >= xe + taille_tank
                    or y_cible + taille_tank <= ye or y_cible >= ye + taille_tank):
                return False

        return True



    def deplacer_tirs(self):
        speed = self.tirs_speed
        
        for i, (direction, x, y) in enumerate(self.tirs):
            new_x, new_y = x, y

            if direction == "h":
                if new_y >= speed:
                    new_y -= speed
                else:
                    new_y = 0

            elif direction == "b":
                if new_y <= 224-speed:
                    new_y += speed
                else: 
                    new_y = 224

            elif direction == "g":
                if new_x >= speed:
                    new_x -= speed
                else:
                    new_x = 0

            elif direction == "d":
                if new_x <= 224-speed:
                    new_x += speed
                else: 
                    new_x = 224


            if direction in ("h", "b") and (new_y < 224 and new_y > 0):
                self.tirs[i] = (direction, new_x, new_y)
            elif direction in ("g", "d") and (new_x < 224 and new_x > 0):
                self.tirs[i] = (direction, new_x, new_y)
            elif new_x in (0, 224) or new_y in (0, 224):
                self.tirs.pop(i)
                self.add_explosion(x, y, "tir")


    def degats_tirs(self, map_):
        taille = self.ennemi.taille_tank

        for i, (direction, x, y) in enumerate(self.tirs[:]):
            ty = (y + 9) // 16
            tx = (x + 8) // 16

            for (d, xe, ye) in self.ennemi.tanks_position:
                if (x + 8 > xe and x < xe + taille and 
                    y + 8 > ye and y < ye + taille):
                    self.ennemi.tanks_position.remove((d, xe, ye))
                    self.ennemi.nb_tank_ennemi -= 1
                    self.tank_eliminer += 1
                    self.score += 100
                    self.tirs.pop(i)
                    self.add_explosion(x, y, "tank")
                    return 
                
            if ty > 0 and ty < 14:
                if direction == "h":
                    cible = map_[ty - 1][tx]
                    if cible in self.obstacles:
                        if cible == 1:
                            map_[ty - 1][tx] = [9, direction]
                        elif cible == 4:
                            map_[ty - 1][tx] = 10
                        elif isinstance(cible, list) and cible[0] == 9:
                            map_[ty - 1][tx] = 0
                        self.tirs.pop(i)
                        self.add_explosion(x, y, "tir")
                        return

                elif direction == "b":
                    cible = map_[ty + 1][tx]
                    if cible in self.obstacles:
                        if cible == 1:
                            map_[ty + 1][tx] = [9, direction]
                        elif cible == 4:
                            map_[ty + 1][tx] = 10
                        elif isinstance(cible, list) and cible[0] == 9:
                            map_[ty + 1][tx] = 0
                        self.tirs.pop(i)
                        self.add_explosion(x, y, "tir")
                        return

            if tx > 0 and tx < 14:
                if direction == "g":
                    cible = map_[ty][tx - 1]
                    if cible in self.obstacles:
                        if cible == 1:
                            map_[ty][tx - 1] = [9, direction]
                        elif cible == 4:
                            map_[ty][tx - 1] = 10
                        elif isinstance(cible, list) and cible[0] == 9:
                            map_[ty][tx - 1] = 0
                        self.tirs.pop(i)
                        self.add_explosion(x, y, "tir")
                        return

                elif direction == "d":
                    cible = map_[ty][tx + 1]
                    if cible in self.obstacles:
                        if cible == 1:
                            map_[ty][tx + 1] = [9, direction]
                        elif cible == 4:
                            map_[ty][tx + 1] = 10
                        elif isinstance(cible, list) and cible[0] == 9:
                            map_[ty][tx + 1] = 0
                        self.tirs.pop(i)
                        self.add_explosion(x, y, "tir")
                        return


    def dessiner_map(self, map):
        for y, ligne in enumerate(map):
            for x, colonne in enumerate(ligne):

                if colonne in (0, 3, 5):
                    pyxel.rect((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 16, 16, 0)

                if colonne != self.old_map[y][x] or self.game_over_bool == True:
                    #Brique
                    if colonne == 1:
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0, 16, 0, 16, 16)
                    
                    #Brique incassable
                    elif colonne == 2:
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0, 48, 0, 16, 16)
                    
                    #Totem
                    elif colonne == 4:
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0, 128, 0, 16, 16)
                    
                    #Totem briser
                    elif colonne == 10:
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0, 128, 16, 16, 16)

        for i in range(16):
            pyxel.blt((self.WIDHT/16)*(i), (self.HEIGHT/16)*(15), 0, 224, 0, 16, 16)  
            pyxel.blt((self.WIDHT/16)*(15), (self.HEIGHT/16)*(i), 0, 224, 0, 16, 16)   

        pyxel.text(10, 246, f"Score: {self.score}", 8) 
        pyxel.text(75, 246, "Press 'a' to save and return to the menu", 8)   

        self.old_map = [row[:] for row in map] 
        

    def dessiner_elements_dynamique(self, map):
        water = False
        for y, ligne in enumerate(map):
            for x, colonne in enumerate(ligne):
                #Eau
                if colonne == 5:
                    if self.etat_eau == 1:
                        water = True
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0,  0, 32, 16, 16, colkey=0)
                    else:
                        water = True
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0,  96, 16, 16, 16, colkey=0)

                #Demi-brique
                elif type(colonne) == list: 
                    if colonne[0] == 9 and colonne[1] == "h":
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0, 112, 0, 16, 16)
                    elif colonne[0] == 9 and colonne[1] == "b":
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0, 112, 16, 16, 16)
                    elif colonne[0] == 9 and colonne[1] == "g":
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0, 144, 0, 16, 16)
                    elif colonne[0] == 9 and colonne[1] == "d":
                        pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0, 144, 16, 16, 16)
        
        if water is True:
            self.animation_eau()

        #Tank
        if self.modele_tank == 1:
            if self.direction == "h":
                pyxel.blt(self.x_tank, self.y_tank, 0, 0, 0, 16, 16)
            elif self.direction == "b":
                pyxel.blt(self.x_tank, self.y_tank, 0, 0, 16, 16, 16)
            elif self.direction == "g":
                pyxel.blt(self.x_tank, self.y_tank, 0, 32, 0, 16, 16)
            elif self.direction == "d":
                pyxel.blt(self.x_tank, self.y_tank, 0, 32, 16, 16, 16)
        elif self.modele_tank == 2:
            if self.direction == "h":
                pyxel.blt(self.x_tank, self.y_tank, 0, 0, 112, 16, 16)
            elif self.direction == "b":
                pyxel.blt(self.x_tank, self.y_tank, 0, 16, 112, 16, 16)
            elif self.direction == "g":
                pyxel.blt(self.x_tank, self.y_tank, 0, 32, 112, 16, 16)
            elif self.direction == "d":
                pyxel.blt(self.x_tank, self.y_tank, 0, 48, 112, 16, 16)

        #Bouclier
        if self.bouclier_bool == True:
            if self.forme_bouclier == 1:
                pyxel.blt(self.x_tank, self.y_tank, 0, 0, 96, 16, 16, colkey = 0)
            else:
                pyxel.blt(self.x_tank, self.y_tank, 0, 16, 96, 16, 16, colkey = 0)

        #Tank ennemi
        for (direction, x, y) in self.ennemi.tanks_position:
            if direction == "h":
                pyxel.blt(x, y, 0, 192, 0, 16, 16)
            elif direction == "b":
                pyxel.blt(x, y, 0, 208, 0, 16, 16)
            elif direction == "g":
                pyxel.blt(x, y, 0, 160, 0, 16, 16)
            elif direction == "d":
                pyxel.blt(x, y, 0, 176, 0, 16, 16)

        #Tirs
        for (direction, x, y) in self.tirs:
            if direction == "h":
                pyxel.blt(x, y, 0, 64, 0, 16, 16, colkey=0)
            elif direction == "b":
                pyxel.blt(x, y, 0, 64, 0, 16, -16, colkey=0)
            elif direction == "g":
                pyxel.blt(x, y, 0, 80, 0, 16, 16, colkey=0)
            elif direction == "d":
                pyxel.blt(x, y, 0, 80, 0, -16, 16,colkey=0)

        #Tirs ennemi
        for (direction, x, y) in self.ennemi.tirs_ennemi:
            if direction == "h":
                pyxel.blt(x, y, 0, 64, 16, 16, 16,colkey=0)
            elif direction == "b":
                pyxel.blt(x, y, 0, 64, 16, 16, -16,colkey=0)
            elif direction == "g":
                pyxel.blt(x, y, 0, 80, 16, 16, 16,colkey=0)
            elif direction == "d":
                pyxel.blt(x, y, 0, 80, 16, -16, 16,colkey=0)

        #Animation spawn ennemi
        for (stade, direction, x, y) in self.ennemi.animation_spawn:
            if stade in (1, 5, 9):
                pyxel.blt(x, y, 0, 16, 64, 16, 16, colkey=0)
            elif stade in (2, 6, 10):
                pyxel.blt(x, y, 0, 32, 64, 16, 16, colkey=0)
            elif stade in (3, 7, 11):
                pyxel.blt(x, y, 0, 48, 64, 16, 16, colkey=0)
            elif stade in (4, 8, 12):
                pyxel.blt(x, y, 0, 64, 64, 16, 16, colkey=0)

        #Animation explosions 
        self.draw_explosions()

        #Buisson
        for y, ligne in enumerate(map):
            for x, colonne in enumerate(ligne):
                if colonne == 3:
                    pyxel.blt((self.WIDHT/16)*(x), (self.HEIGHT/16)*(y), 0,  96, 0, 16, 16, colkey=0)


        #Game Over
        pyxel.rect(100, self.y_game_over-3, 50, 10, 0)
        pyxel.text(110, self.y_game_over,"Game Over", 8)

        #Vies
        pyxel.blt(240, 208, 0, 16, 16, 16, 16)
        pyxel.text(250, 218, str(self.ennemi.vies), 9)

        #Tank a eliminer
        x0, y0 = 240, 64 
        icon_w = 8
        icon_h = 8
        nbr_tank = 20 - len(self.ennemi.tanks_position) - len(self.ennemi.animation_spawn) - self.tank_eliminer
        nbr_tank_dessiner = 0

        for yt in range(10):
            for xt in range(2): 
                if nbr_tank_dessiner < nbr_tank:
                    px = x0 + xt * icon_w
                    py = y0 + yt * icon_h
                    pyxel.blt(px, py, 0, 48, 16, 8, 8)
                    nbr_tank_dessiner += 1
                else:
                    break



    def draw(self): 
        if self.state == "menu":
            self.jeu = False
            pyxel.mouse(True)
            pyxel.cls(0) 

            #animation texte
            if self.direction_menu == "+":
                self.x_menu += 1
                if self.x_menu >= 121:
                    self.direction_menu = "-"
            else:
                self.x_menu -= 1
                if self.x_menu <= 110:
                   self.direction_menu = "+"

            pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
            pyxel.text(self.x_menu, 245, "Press Enter to select", 7)

            pyxel.text(120, 141, "Play", 7)
            pyxel.text(107, 166, "Leaderboard", 7)
            pyxel.text(99, 190, "Choose a pseudo", 7)

            if self.choix == 1:
                pyxel.blt(70, 135, 0, 240, 0, 16, 16)
            elif self.choix == 2:
                pyxel.blt(70, 159, 0, 240, 0, 16, 16)
            elif self.choix == 3:
                pyxel.blt(70, 183, 0, 240, 0, 16, 16)


        elif self.state == "jeu":
            if self.jeu == False:
                pyxel.mouse(False)
                pyxel.cls(0)
                self.jeu = True
            self.dessiner_map(self.maps[self.level-1])
            self.dessiner_elements_dynamique(self.maps[self.level-1])
            self.powerups.draw()

        elif self.state == "leaderboard":
            self.jeu = False
            pyxel.mouse(True)
            pyxel.cls(0) 
            pyxel.bltm(0, 0, 0, 512, 0, 256, 256)
            draw_leaderboard(self)

        elif self.state == "pseudo":
            self.jeu = False
            pyxel.mouse(True)
            pyxel.cls(0) 
            pyxel.bltm(0, 0, 0, 768, 0, 256, 256)
            pyxel.text(90, 50, "Type your pseudo :", 7)
            pyxel.rect(68, 65, 120, 15, 1)
            pyxel.text(72, 69, self.pseudo + "_", 10)
            pyxel.text(90, 90, "(Enter to validate)", 8)

        elif self.state == "help":
            self.jeu = False
            pyxel.mouse(True)
            pyxel.cls(0) 
            pyxel.bltm(0, 0, 0, 256, 0, 256, 256)
            pyxel.text(40, 15, "'A' to return to the main menu", 7)
            pyxel.text(40, 30, "In the game:", 7)
            pyxel.text(50, 45, "Use ZQSD or arrow keys to move your tank", 7)
            pyxel.text(40, 60, "In the main menu:", 7)
            pyxel.text(50, 75, "Press '1' to start the game", 7)
            pyxel.text(50, 90, "Press '2' to open the leaderboard", 7)
            pyxel.text(50, 105, "Press '3' to choose a new nickname", 7)
            pyxel.text(50, 120, "Press Enter to confirm your choice", 7)
            pyxel.text(40, 135, "In the nickname menu:", 7)
            pyxel.text(50, 150, "Delete the name in the box and type your own", 7)
            pyxel.text(50, 165, "Press Enter to confirm your nickname", 7)


    def update(self):

        if self.state == "menu":
            if pyxel.btnr(pyxel.KEY_RETURN):
                if self.choix == 1:
                    self.state = "jeu"
                    self.rejouer()
                elif self.choix == 2:
                    self.state = "leaderboard"
                elif self.choix == 3:
                    self.state = "pseudo"
                elif self.choix == 4:
                    self.state = "help"


            if pyxel.btnr(pyxel.KEY_1):
                self.choix = 1
            if pyxel.btnr(pyxel.KEY_2):
                self.choix = 2
            if pyxel.btnr(pyxel.KEY_3):
                self.choix = 3
            
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                x_souris = pyxel.mouse_x
                y_souris = pyxel.mouse_y

                #detection case cliqué
                if x_souris >= 97 and x_souris <= 160:
                    if y_souris >= 140 and y_souris <= 155:
                        self.choix = 1
                        self.state = "jeu"
                        self.rejouer()
                    elif y_souris >= 160 and y_souris <= 175:
                        self.choix = 2
                        self.state = "leaderboard"
                    elif y_souris >= 184 and y_souris <= 200:
                        self.choix = 3
                        self.state = "pseudo"
                elif x_souris >= 180 and x_souris <= 190:
                    if y_souris >= 210 and y_souris <= 220:
                        self.choix = 4
                        self.state = "help"
                
            
        elif self.state == "jeu":
            if any(4 in ligne for ligne in self.maps[self.level - 1]) and self.ennemi.vies > 0:
                speed = self.tank_speed
                map_ = self.maps[self.level-1]

                #Petit cheat pour le fun ; )
                if pyxel.btnr(pyxel.KEY_P):
                    self.ennemi.vies += 1

                #quitter le jeu
                if pyxel.btnr(pyxel.KEY_A):
                    save = Save(self.pseudo, self.score)
                    save.save_score()
                    self.state = "menu"


                #afficher la map actuel
                if pyxel.btnr(pyxel.KEY_I):
                    print(len(self.ennemi.tanks_position))
                    print(len(self.ennemi.animation_spawn))
                    print(self.tank_eliminer)
                    print(len(self.ennemi.tanks_position) + len(self.ennemi.animation_spawn) + self.tank_eliminer)

                #aller vers le haut
                if (pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP)) and not ((pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN)) or (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT)) or (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT))):
                    self.direction = "h"
                    self.frame_tank += 1
                    if self.est_accesible(self.x_tank, self.y_tank-speed, map_):
                        self.y_tank -= speed


                #aller vers le bas
                if (pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN)) and not ((pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP)) or (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT)) or (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT))):
                    self.direction = "b"
                    self.frame_tank += 1
                    if self.est_accesible(self.x_tank, self.y_tank+speed, map_):
                        self.y_tank += speed


                #aller vers la gauche
                if (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT)) and not ((pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP)) or (pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN)) or (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT))):
                    self.direction = "g"
                    self.frame_tank += 1
                    if self.est_accesible(self.x_tank-speed, self.y_tank, map_):
                        self.x_tank -= speed


                #aller vers la droite
                if (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT)) and not ((pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN)) or (pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT)) or (pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP))):
                    self.direction = "d"
                    self.frame_tank += 1
                    if self.est_accesible(self.x_tank+speed, self.y_tank, map_):
                        self.x_tank += speed



                #tirer
                if pyxel.btnr(pyxel.KEY_SPACE):
                    if len(self.tirs) == 0:
                        ty = (self.y_tank + 9) // 16
                        tx = (self.x_tank + 8) // 16

                        if self.y_tank not in (0, 224):
                            if self.direction == "h":
                                if map_[ty-1][tx] in self.obstacles:
                                    if map_[ty-1][tx] == 1:
                                        map_[ty-1][tx] = [9, self.direction]

                                    elif map_[ty-1][tx] == 4:
                                        map_[ty-1][tx] = 10

                                    elif type(map_[ty-1][tx]) == list:
                                        if map_[ty-1][tx][0] == 9:
                                            map_[ty-1][tx] = 0
                                    
                                else:
                                    self.tirs.append((self.direction, self.x_tank, self.y_tank-1))

                            elif self.direction == "b":
                                if map_[ty+1][tx] in self.obstacles:
                                    if map_[ty+1][tx] == 1:
                                        map_[ty+1][tx] = [9, self.direction]

                                    elif map_[ty+1][tx] == 4:
                                        map_[ty+1][tx] = 10

                                    elif type(map_[ty+1][tx]) == list:
                                        if map_[ty+1][tx][0] == 9:
                                            map_[ty+1][tx] = 0
                                    
                                else:
                                    self.tirs.append((self.direction, self.x_tank, self.y_tank+1))

                        if self.x_tank not in (0, 224):
                            if self.direction == "g":
                                if map_[ty][tx-1] in self.obstacles:
                                    if map_[ty][tx-1] == 1:
                                        map_[ty][tx-1] = [9, self.direction]

                                    elif map_[ty][tx-1] == 4:
                                        map_[ty][tx-1] = 10

                                    elif type(map_[ty][tx-1]) == list:
                                        if map_[ty][tx-1][0] == 9:
                                            map_[ty][tx-1] = 0
                                        
                                else:
                                    self.tirs.append((self.direction, self.x_tank-1, self.y_tank))

                            elif self.direction == "d":
                                if map_[ty][tx+1] in self.obstacles:
                                    if map_[ty][tx+1] == 1:
                                        map_[ty][tx+1] = [9, self.direction]

                                    elif map_[ty][tx+1] == 4:
                                        map_[ty][tx+1] = 10

                                    elif type(map_[ty][tx+1]) == list:
                                        if map_[ty][tx+1][0] == 9:
                                            map_[ty][tx+1] = 0
                                        
                                else:
                                    self.tirs.append((self.direction, self.x_tank+1, self.y_tank))

                if self.frame_tank > 1:
                    self.frame_tank = 0
                    if self.modele_tank == 1:
                        self.modele_tank = 2
                    else: 
                        self.modele_tank = 1

                if self.bouclier_bool == False:
                    if self.old_life != self.ennemi.vies:
                        if self.ennemi.vies > 0:
                            self.old_life = self.ennemi.vies
                            self.joueur_touché()
                        else:
                            if self.saved == False:
                                save = Save(self.pseudo, self.score)
                                self.saved = True
                                save.save_score()
                            self.game_over()
                            self.game_over_bool = True

                if self.bouclier_bool == True:
                    self.bouclier(3)

                if self.tank_eliminer >= self.nb_tank_a_eliminer:   
                    self.tank_eliminer = 0
                    self.level_up()

                self.ennemi.animation_spawn_ennemi()
                self.degats_tirs(map_)
                self.ennemi.degats_tirs_ennemi(map_, self.x_tank, self.y_tank, self.bouclier_bool)
                self.deplacer_tirs()
                self.ennemi.deplacer_tirs_ennemi()
                self.explosion_animation()
                if len(self.ennemi.tanks_position) + len(self.ennemi.animation_spawn) + self.tank_eliminer < self.nb_tank_a_eliminer:
                    self.ennemi.spawn_tank_ennemi(map_)
                if not self.stopwatch:
                    self.ennemi.mouvements_ennemi(map_, self.x_tank, self.y_tank)

            
            else:
                if self.saved == False:
                    save = Save(self.pseudo, self.score)
                    save.save_score()
                    self.saved = True
                self.game_over()
                self.game_over_bool = True

            
            self.powerups.update(self.maps[self.level-1])
            picked = self.powerups.check_pickup(self.x_tank, self.y_tank)
            if picked == "helmet":
                self.bouclier_bool = True
                self.frame3 = -100
            elif picked == "stopwatch":
                self.stopwatch = True
                self.stopwatch_timer = 50
                """elif picked == "shovel":
                self.base_invincible = True
                self.base_invincible_timer = 300"""
                """elif picked == "star":
                self.tank_level += 1"""
            elif picked == "pomegranate":
                for (d, xe, ye) in self.ennemi.tanks_position[:]:
                    self.add_explosion(xe, ye, "tank")
                    self.ennemi.tanks_position.remove((d, xe, ye))
                    self.score += 100
            elif picked == "tankupup":
                self.ennemi.vies += 1
            """elif picked == "gun":
                self.gun_level += 1"""

            
            # Stopwatch
            if self.stopwatch:
                self.stopwatch_timer -= 1
                if self.stopwatch_timer <= 0:
                    self.stopwatch = False
                    for i in range(len(self.ennemi.tanks_position)):
                        self.ennemi.tanks_position[i] = self.ennemi.tanks_position[i]  # ou un reset du freeze si tu avais mis un bool dans Ennemi

            # Base invincible
            if self.base_invincible:
                self.base_invincible_timer -= 1
                if self.base_invincible_timer <= 0:
                    self.base_invincible = False

        elif self.state == "pseudo":
            if len(self.pseudo) < 29:
                for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
                    if pyxel.btnr(key):
                        self.pseudo += chr(key)

                for key in range(pyxel.KEY_0, pyxel.KEY_9 + 1):
                    if pyxel.btnr(key):
                        self.pseudo += chr(key)

                if pyxel.btnr(pyxel.KEY_SPACE):
                    self.pseudo += " "

            if pyxel.btn(pyxel.KEY_BACKSPACE):
                self.pseudo = self.pseudo[:-1]

            if pyxel.btnr(pyxel.KEY_RETURN):
                self.state = "menu" 


        else:
            if pyxel.btnr(pyxel.KEY_A):
                self.state = "menu"
            

Game()