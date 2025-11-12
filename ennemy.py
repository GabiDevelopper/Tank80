from random import choice, randint

class Ennemi:
    def __init__(self):
        self.nb_tank_ennemi = 0
        self.nb_max_tank_ennemi = 4 #4
        self.frame = 0
        self.frame2 = 0

        self.tanks_position = []  # (direction, x, y)
        self.tirs_ennemi = []     # [(x, y, direction)]
        self.tirs_speed = 8

        self.taille_tank = 16
        self.ROWS = 15
        self.COLS = 15
        self.obstacles = [1, 2, 4, [9, "h"], [9, "b"], [9, "g"], [9, "d"]]

        self.joueur_touche = False
        self.vies = 3

        self.animation_spawn = []

        self.explosions = []   # (x, y, frame, type)


    def est_accesible(self, x_cible, y_cible, x, y, x_tank, y_tank, map_):
        marge = 2
        taille = self.taille_tank

        if not (0 <= x_cible < self.COLS * taille and 0 <= y_cible < self.ROWS * taille):
            return False

        for ty in range((y_cible + marge) // taille, (y_cible + taille - marge - 1) // taille + 1):
            for tx in range((x_cible + marge) // taille, (x_cible + taille - marge - 1) // taille + 1):

                if ty < 0 or ty >= len(map_) or tx < 0 or tx >= len(map_[0]):
                    return False

                case = map_[ty][tx]


                if case in (1, 2, 4, 5):
                    return False
                elif isinstance(case, list) and case[0] == 9:
                    bx = tx * self.taille_tank
                    by = ty * self.taille_tank

                    if case[1] == "h": 
                        bx1, by1 = bx, by
                        bx2, by2 = bx + self.taille_tank, by + self.taille_tank//2
                    elif case[1] == "b":  
                        bx1, by1 = bx, by + self.taille_tank//2
                        bx2, by2 = bx + self.taille_tank, by + self.taille_tank
                    elif case[1] == "g":  
                        bx1, by1 = bx, by
                        bx2, by2 = bx + self.taille_tank//2, by + self.taille_tank
                    elif case[1] == "d": 
                        bx1, by1 = bx + self.taille_tank//2, by
                        bx2, by2 = bx + self.taille_tank, by + self.taille_tank

                    if not (x_cible + self.taille_tank <= bx1 or x_cible >= bx2 or
                            y_cible + self.taille_tank <= by1 or y_cible >= by2):
                        return False

        if (x_cible + taille > x_tank and x_cible < x_tank + taille and
            y_cible + taille > y_tank and y_cible < y_tank + taille):
            return False

        for (d, xte, yte) in self.tanks_position:
            if (xte, yte) != (x, y):
                if not (x_cible + taille <= xte or x_cible >= xte + taille
                        or y_cible + taille <= yte or y_cible >= yte + taille):
                    return False

        return True

    def animation_spawn_ennemi(self):
        new_spawns = []
        self.frame2 += 1

        if self.frame2 < 2:
            return
        self.frame2 = 0

        for (stade, direction, x, y) in self.animation_spawn:
            if stade < 12:
                new_spawns.append((stade + 1, direction, x, y))
            else:
                self.tanks_position.append((direction, x, y))

        self.animation_spawn = new_spawns

            
            

    def spawn_tank_ennemi(self, map_):
        if len(self.tanks_position) + len(self.animation_spawn) < self.nb_max_tank_ennemi and randint(1, 100) < 10:
            choix = choice((0, 112, 224))
            case_x = choix // 16

            if map_[0][case_x] in (0, 3):
                collision_spawn = False

                for (d, x, y) in self.tanks_position:
                    if not (choix + self.taille_tank <= x or choix >= x + self.taille_tank
                            or 0 + self.taille_tank <= y or 0 >= y + self.taille_tank):
                        collision_spawn = True
                        break

                for (stade, d, x, y) in self.animation_spawn:
                    if not (choix + self.taille_tank <= x or choix >= x + self.taille_tank
                            or 0 + self.taille_tank <= y or 0 >= y + self.taille_tank):
                        collision_spawn = True
                        break

                if not collision_spawn:
                    self.animation_spawn.append((1, "b", choix, 0))



    def cree_tirs_ennemi(self, map_, x, y, direction):
        if len(self.tirs_ennemi) < 5:
            taille = self.taille_tank
            tx, ty = x // taille, y // taille

            if direction == "h":  
                x_tir = x 
                y_tir = y - 6
            elif direction == "b": 
                x_tir = x
                y_tir = y + 6
            elif direction == "g": 
                x_tir = x - 6
                y_tir = y 
            elif direction == "d":  
                x_tir = x + 6
                y_tir = y 
            else:
                return

            if not (0 <= x_tir < self.COLS * taille and 0 <= y_tir < self.ROWS * taille):
                return

            tx, ty = x_tir // taille, y_tir // taille
            case = map_[ty][tx]

            if case == 0:
                self.tirs_ennemi.append((direction, x_tir, y_tir))



    def mouvements_ennemi(self, map_, x_tank, y_tank):
        x_totem = y_totem = None
        for y, ligne in enumerate(map_):
            for x, val in enumerate(ligne):
                if val == 4:
                    x_totem, y_totem = x * 16, y * 16
                    break
            if x_totem is not None:
                break

        if x_totem is None:
            return

        nouvelles_positions = []
        self.frame += 1
        if self.frame < 2:
            return
        self.frame = 0

        directions = {
            "h": (0, -4),
            "b": (0, 4),
            "g": (-4, 0),
            "d": (4, 0)
        }

        for (direction, x, y) in self.tanks_position:
            dx = x_totem - x
            dy = y_totem - y
            moved = False
            tir = False

            vx, vy = directions[direction]
            nx, ny = x + vx, y + vy

            if self.est_accesible(nx, ny, x, y, x_tank, y_tank, map_):
                nouvelles_positions.append((direction, nx, ny))
                moved = True

            if not moved:
                options = []
                if abs(dx) > abs(dy):
                    if dx > 0: options.append("d")
                    elif dx < 0: options.append("g")
                    if dy > 0: options.append("b")
                    elif dy < 0: options.append("h")
                else:
                    if dy > 0: options.append("b")
                    elif dy < 0: options.append("h")
                    if dx > 0: options.append("d")
                    elif dx < 0: options.append("g")

                for d in ["h", "b", "g", "d"]:
                    if d not in options:
                        options.append(d)

                for d in options:
                    vx, vy = directions[d]
                    nx, ny = x + vx, y + vy
                    if self.est_accesible(nx, ny, x, y, x_tank, y_tank, map_):
                        nouvelles_positions.append((d, nx, ny))
                        moved = True
                        break

                if not moved:
                    tir = True
                    nouvelles_positions.append((direction, x, y))

            same_row = abs(y - y_tank) < 8 and abs(x - x_tank) < self.COLS * 16
            same_col = abs(x - x_tank) < 8 and abs(y - y_tank) < self.ROWS * 16
            same_row_totem = abs(y - y_totem) < 8
            same_col_totem = abs(x - x_totem) < 8

            if same_row or same_col or same_row_totem or same_col_totem or tir:
                if randint(0, 100) < 10: 
                    self.cree_tirs_ennemi(map_, x, y, direction)

        self.tanks_position = [elem for elem in nouvelles_positions]



    def deplacer_tirs_ennemi(self):
        speed = self.tirs_speed
        
        for i, (direction, x, y) in enumerate(self.tirs_ennemi):
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
                self.tirs_ennemi[i] = (direction, new_x, new_y)
            elif direction in ("g", "d") and (new_x < 224 and new_x > 0):
                self.tirs_ennemi[i] = (direction, new_x, new_y)
            elif new_x in (0, 224) or new_y in (0, 224):
                self.tirs_ennemi.pop(i)
                self.explosions.append([x, y, 0, "tir"])


    def degats_tirs_ennemi(self, map_, x_tank, y_tank, bouclier):
        taille_tank = 16 
        
        for i, (direction, x, y) in enumerate(self.tirs_ennemi[:]): 
            ty = y // 16
            tx = x // 16

            if (x + 8 > x_tank and x < x_tank + taille_tank and
                y + 8 > y_tank and y < y_tank + taille_tank):

                if bouclier:
                    self.tirs_ennemi.pop(i)
                    return

                self.tirs_ennemi.pop(i)
                self.joueur_touche = True  
                self.vies -= 1
                return


            if ty > 0 and ty < len(map_) - 1:
                if direction == "h":
                    cible = map_[ty - 1][tx]
                    if cible in self.obstacles:
                        if cible == 1:
                            map_[ty - 1][tx] = [9, direction]
                        elif cible == 4:
                            map_[ty - 1][tx] = 10
                        elif isinstance(cible, list) and cible[0] == 9:
                            map_[ty - 1][tx] = 0
                        self.tirs_ennemi.pop(i)
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
                        self.tirs_ennemi.pop(i)
                        return

            if tx > 0 and tx < len(map_[0]) - 1:
                if direction == "g":
                    cible = map_[ty][tx - 1]
                    if cible in self.obstacles:
                        if cible == 1:
                            map_[ty][tx - 1] = [9, direction]
                        elif cible == 4:
                            map_[ty][tx - 1] = 10
                        elif isinstance(cible, list) and cible[0] == 9:
                            map_[ty][tx - 1] = 0
                        self.tirs_ennemi.pop(i)
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
                        self.tirs_ennemi.pop(i)
                        return


