import random
import pyxel

class Powerups:
    """
    Types :
        helmet      -> invincibilité temporaire
        stopwatch   -> ennemis figés
        shovel      -> base invincible
        star        -> lvl up du tank
        pomegranate -> explose tous les ennemis
        tankupup    -> +1 vie
        gun         -> arme améliorée
    """

    TYPES = [
        "helmet",
        "stopwatch",
        "pomegranate",
        "tankupup",      
    ]
    #"shovel",
    #"star",
    #"gun"

    def __init__(self):
       
        self.active = False
        self.type = None
        self.x = 0
        self.y = 0

        self.next_spawn_timer = random.randint(300, 800) 
        self.frame = 0

    def spawn(self, map_):
        self.type = random.choice(self.TYPES)

        while True:
            tx = random.randint(0, len(map_[0]) - 1)
            ty = random.randint(0, len(map_) - 1)

            if map_[ty][tx] in (0, 3, 5): 
                break

        self.x = tx * 16
        self.y = ty * 16
        self.active = True

    def update(self, map_):
        if not self.active:
            self.frame += 1
            if self.frame > self.next_spawn_timer:
                self.frame = 0
                self.next_spawn_timer = random.randint(300, 800)
                self.spawn(map_)


    def check_pickup(self, x_tank, y_tank):
        if not self.active:
            return None

        if (x_tank + 16 > self.x and x_tank < self.x + 16 and
            y_tank + 16 > self.y and y_tank < self.y + 16):

            picked = self.type
            self.active = False
            self.type = None
            return picked

        return None
    

    def draw(self):
        if not self.active:
            return

        icon_x = {
            "helmet":      0,
            "stopwatch":   16,
            "shovel":      32,
            "star":        48,
            "pomegranate": 64,
            "tankupup":    80,
            "gun":         96,
        }[self.type]

        pyxel.blt(self.x, self.y, 0, icon_x, 80, 16, 16, colkey=0)
