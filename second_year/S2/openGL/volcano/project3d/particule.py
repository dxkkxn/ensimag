from core import Viewer
import numpy as np

class Particle:
    gravityEffect: float
    lifeLength: float
    rotation: float
    scale: float

    elapsedTime: float = 0

    def __init__(self, position, velocity, gravityEffect, lifeLength, rotation, scale):
        self.position = position
        self.velocity = velocity
        self.gravityEffect = gravityEffect
        self.lifeLength = lifeLength
        self.rotation = rotation
        self.scale = scale

    def update(self):  
        self.velocity.y += -9.81 * self.gravityEffect * Viewer.SceneTime
        change = np.multiply(self.velocity, Viewer.SceneTime)
        self.position = np.add(self.position, change)
        self.elapsedTime += 0.01
        return (self.elapsedTime < self.lifeLength)