from mc.net.minecraft.character.Cube import Cube
from mc.net.minecraft.Textures import Textures
from mc.net.minecraft.Entity import Entity
from mc.CompatibilityShims import getNs
from pyglet import gl

import random
import math

class Zombie(Entity):

    def __init__(self, level, x, y, z):
        super().__init__(level)
        self.rotA = (random.random() + 1.0) * 0.01
        self.x = x
        self.y = y
        self.z = z
        self.timeOffs = random.random() * 1239813.0
        self.rot = random.random() * math.pi * 2.0
        self.speed = 1.0

        self.head = Cube(0, 0)
        self.head.addBox(-4.0, -8.0, -4.0, 8, 8, 8)

        self.body = Cube(16, 16)
        self.body.addBox(-4.0, 0.0, -2.0, 8, 12, 4)

        self.arm0 = Cube(40, 16)
        self.arm0.addBox(-3.0, -2.0, -2.0, 4, 12, 4)
        self.arm0.setPos(-5.0, 2.0, 0.0)

        self.arm1 = Cube(40, 16)
        self.arm1.addBox(-1.0, -2.0, -2.0, 4, 12, 4)
        self.arm1.setPos(5.0, 2.0, 0.0)

        self.leg0 = Cube(0, 16)
        self.leg0.addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.leg0.setPos(-2.0, 12.0, 0.0)

        self.leg1 = Cube(0, 16)
        self.leg1.addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.leg1.setPos(2.0, 12.0, 0.0)

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        xa = 0.0
        ya = 0.0

        self.rot += self.rotA
        self.rotA = self.rotA * 0.99
        self.rotA = self.rotA + (random.random() - random.random()) * random.random() * random.random() * 0.01
        xa = math.sin(self.rot)
        ya = math.cos(self.rot)

        if self.onGround and random.random() < 0.01:
            self.yd = 0.12

        self.moveRelative(xa, ya, 0.02 if self.onGround else 0.005)

        self.yd = self.yd - 0.005
        self.move(self.xd, self.yd, self.zd)
        self.xd *= 0.91
        self.yd *= 0.98
        self.zd *= 0.91

        if self.y > 100.0:
            self.resetPos()

        if self.onGround:
            self.xd *= 0.8
            self.zd *= 0.8

    def render(self, a):
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, Textures.loadTexture('char.png', gl.GL_NEAREST))

        gl.glPushMatrix()
        t = getNs() / 1000000000.0 * 10.0 * self.speed + self.timeOffs

        size = 0.05833333
        yy = -abs(math.sin(t * 0.6662)) * 5.0 - 23.0
        gl.glTranslatef(self.xo + (self.x - self.xo) * a, self.yo + (self.y - self.yo) * a, self.zo + (self.z - self.zo) * a)
        gl.glScalef(1.0, -1.0, 1.0)
        gl.glScalef(size, size, size)
        gl.glTranslatef(0.0, yy, 0.0)
        c = 57.29578
        gl.glRotatef(self.rot * c + 180.0, 0.0, 1.0, 0.0)

        self.head.yRot = math.sin(t * 0.83) * 1.0
        self.head.xRot = math.sin(t) * 0.8

        self.arm0.xRot = math.sin(t * 0.6662 + math.pi) * 2.0
        self.arm0.zRot = (math.sin(t * 0.2312) + 1.0) * 1.0

        self.arm1.xRot = math.sin(t * 0.6662) * 2.0
        self.arm1.zRot = (math.sin(t * 0.2812) - 1.0) * 1.0

        self.leg0.xRot = math.sin(t * 0.6662) * 1.4
        self.leg1.xRot = math.sin(t * 0.6662 + math.pi) * 1.4

        self.head.render()
        self.body.render()
        self.arm0.render()
        self.arm1.render()
        self.leg0.render()
        self.leg1.render()
        gl.glPopMatrix()
        gl.glDisable(gl.GL_TEXTURE_2D)
