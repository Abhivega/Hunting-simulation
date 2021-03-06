from p5 import *
import random as rn
from copy import deepcopy


class Predator():

    def __init__(self, netw, net2):
        self.net = deepcopy(netw)
        self.net.recomb(net2)
        self.net.mutate()
        self.mini = 500
        self.score = 0
        self.tim = 0
        self.boundy = 0
        self.position = Vector(0, 0)
        self.position = Vector(rn.randint(0, 1200), rn.randint(0, 620))
        self.velocity = Vector(30, 30)
      #  self.velocity = Vector(random_uniform(low=-2, high=2),
      #                         random_uniform(low=-2, high=2))
        self.acceleration = Vector(0, 0)
        self.top_speed = 10
        self.kill = 0
        self.me = False

    def forone(self):
        self.mini = 600
        self.position = Vector(0, 0)
        self.position = Vector(rn.randint(0, 1200), rn.randint(0, 620))
        #  self.position = Vector(rn.randint(0, 680),
        #                         rn.randint(0, 500))
        self.velocity = Vector(30, 30)
        #  self.velocity = Vector(random_uniform(low=-2, high=2),
        #                         random_uniform(low=-2, high=2))
        self.acceleration = Vector(0, 0)
        self.top_speed = 10
        self.kill = 0
        self.boundy = 0
        self.tim = 1
        self.me = True

    def update(self):

        self.velocity.limit(self.top_speed)
        self.position += self.velocity
        self.velocity += self.acceleration
        self.acceleration = Vector(0, 0)

    def show(self):
        stroke(0)
        x = remap(self.kill, (0, 7), (0, 255))
        y = remap(self.kill, (0, 7), (255, 0))
        fill(x, y, 0)
        if self.me:
            fill(0)
        circle(self.position, 15)

    def checkobs(self):
        if self.position.y > 650:
            self.velocity.y = - self.velocity.y
            self.position = Vector(self.position.x, 650)
            self.acceleration = Vector(0, 0)

        elif self.position.y < 20:
            self.velocity.y = - self.velocity.y
            self.position = Vector(self.position.x, 20)
            self.acceleration = Vector(0, 0)

        elif (self.position.x > 1250):
            self.velocity.x = - self.velocity.x
            self.position = Vector(1250, self.position.y)
            self.acceleration = Vector(0, 0)

        elif self.position.x < 20:
            self.velocity.x = - self.velocity.x
            self.position = Vector(20, self.position.y)
            self.acceleration = Vector(0, 0)


    def hund(self, bird):
        k = []
        if len(bird) == 0:
            return
        for i, bir in enumerate(bird):
            k.append(dist(self.position, bir.position))

        kmin = int(min(k))
        i = k.index(min(k))
        if kmin < 500 and kmin > 15:
            m = remap(kmin, (500, 15), (2, 15))

            bird[i].chase = True
            diff = bird[i].position - self.position
            diff.normalize()
            x = self.net.compute([kmin / 500, diff[0], diff[1]])[0]
            y = self.net.compute([kmin / 500, diff[0], diff[1]])[1]
            self.acceleration = Vector(x, y) * m
            self.ismin(kmin)

        elif kmin < 15:
            bird.pop(i)
            self.headcount()

    def ismin(self, kmin):
        if kmin < self.mini:
            self.mini = kmin

    def rank(self):
        if self.kill == 0:
            self.score = self.mini
        else:
            self.score = 15 - (350 * self.boundy)
        return self.score

    def time(self):
        self.tim += 1

    def headcount(self):
        self.kill += 1
        self.boundy += self.kill / (self.tim + 1)
        self.tim = 0
    #    run = remap(self.kill, (0, 10), (8, 14))
    #    self.top_speed = run
        return (self.kill)

    def run(self, bird):

        self.update()
        self.hund(bird)
        self.checkobs()
        self.show()
