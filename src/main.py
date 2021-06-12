import pygame
import sys
from pygame import key
from pygame.locals import *
from pygame.mixer import unpause
import random
import tkinter as tk
import tkinter.messagebox as msg

root = tk.Tk()
root.withdraw()

FPS = 15
fpsClock = pygame.time.Clock()

IMAGE_BACKGROUND = pygame.image.load("assets/download.jpg")
IMAGE_BACKGROUND = pygame.transform.scale(IMAGE_BACKGROUND, (1000, 610))


class Application(object):
    __sprite_config = {u"x": 450, u"y": 475}

    __bullets = []
    __asteriods = []

    def __init__(self, **kwargs) -> None:
        self.DIS_SURF = pygame.display.set_mode((kwargs["width"], kwargs["height"]))

        pygame.display.set_caption("Astermates")

        self.__obj_start__()
        rand_time = int(random.random() * 1000)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.__sprite_config["x"] - 1 > 0:
                    self.__sprite_config["x"] -= 1

            elif keys[pygame.K_RIGHT]:
                if self.__sprite_config["x"] + 1 < 900:
                    self.__sprite_config["x"] += 1

            elif keys[pygame.K_SPACE]:
                self.__bullets.append(
                    {
                        u"x": self.__sprite_config["x"] + 50 + 10,
                        u"y": self.__sprite_config["y"],
                    }
                )

            self.DIS_SURF.blit(IMAGE_BACKGROUND, (0, 0))
            self.DIS_SURF.blit(
                self.__man_sprite,
                (self.__sprite_config["x"], self.__sprite_config["y"]),
            )

            bidx = -1
            for j in range(len(self.__asteriods)):
                if self.__sprite_config["x"] in range(self.__asteriods[j]["x"] - 128, self.__asteriods[j]["x"] + 128) and self.__sprite_config["y"] in range(int(self.__asteriods[j]["y"]), int(self.__asteriods[j]["y"]) + 10):
                    msg.showinfo(title="Information", message="You lost!")
                    sys.exit(0)
                doBreak = False
                for k in range(len(self.__bullets)):
                    if self.__bullets[k]["x"] in range(
                        self.__asteriods[j]["x"], self.__asteriods[j]["x"] + 64
                    ) and self.__bullets[k]["y"] in range(int(self.__asteriods[j]["y"]), int(self.__asteriods[j]["y"]) + 64):
                        bidx = j
                        doBreak = True
                        break
                if doBreak:
                    break
            if bidx != -1:
                del self.__asteriods[bidx]

            for i in range(len(self.__bullets)):
                pygame.draw.rect(
                    self.DIS_SURF,
                    (255, 0, 0),
                    (self.__bullets[i]["x"], self.__bullets[i]["y"], 10, 20),
                )
                self.__bullets[i]["y"] -= 1

            i = 0
            while i < len(self.__asteriods):
                if i < 0:
                    i = 0
                    continue
                if i >= len(self.__asteriods):
                    break
                if self.__asteriods[i]["y"] > 600:
                    del self.__asteriods[i]
                    i -= 2
                    continue
                self.DIS_SURF.blit(
                    self.__asteroid_sprite,
                    (self.__asteriods[i]["x"], self.__asteriods[i]["y"]),
                )
                self.__asteriods[i]["y"] += 0.1
                i += 1

            del i
            i = 0

            while i < len(self.__bullets):
                if i < 0:
                    i = 0
                    continue
                if self.__bullets[i]["y"] < 0:
                    del self.__bullets[i]
                    i -= 2
                    continue
                i += 1

            del i

            if not rand_time and len(self.__asteriods) < 5:
                self.__asteriods.append({u"x": random.randint(100, 900), u"y": 100})
                rand_time = int(random.random() * 1000)

            pygame.display.flip()
            if rand_time > 0:
                rand_time -= 1

    def __obj_start__(self):
        self.DIS_SURF.blit(IMAGE_BACKGROUND, (0, 0))

        self.__man_sprite = pygame.image.load("assets/image.png").convert_alpha()
        self.__man_sprite = pygame.transform.scale(self.__man_sprite, (128, 128))

        self.__asteroid_sprite = pygame.image.load(
            "assets/asteriod.png"
        ).convert_alpha()
        self.__asteroid_sprite = pygame.transform.scale(
            self.__asteroid_sprite, (64, 64)
        )

    def __render_bullet__(self, x, y):
        self.__asteriods.append({u"x": random.randint(100, 900), u"y": 100})


if __name__ == "__main__":
    pygame.init()
    root = Application(width=1000, height=600)
