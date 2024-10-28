#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, Node, load
from texture import Texture, Textured
from perlin import completeNoise
from transform import (
    scale,
    rotate,
    translate,
    identity,
    vec,
    quaternion,
    quaternion_from_euler,
    quaternion_from_axis_angle,
    quaternion_mul
)
import math
import curve
from tree import create_trees, create_grass
from animation import KeyFrames, KeyFrameControlNode

# -------------- Example textured plane class ---------------------------------
class TexturedFloor(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file, tex_file2 ,tex_file3, tex_file4):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        self.heights = {}

        # setup plane mesh to be textured
        base_coords, normals, tangents, indices = self._make_floor(257)

        scaled = 10 * np.array(base_coords, np.float32)
        self.points = scaled


        mesh = Mesh(shader, attributes=dict(position=scaled, normal=normals, tangent=tangents), index=indices, light_dir=(-1, -1, -1))
        
        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        texture2 = Texture(tex_file2, self.wrap, *self.filter)
        texture3 = Texture(tex_file3, self.wrap, *self.filter)
        texture4 = Texture(tex_file4, self.wrap, *self.filter)

        super().__init__(mesh, herbe_map=texture, rock_map= texture2, rock_normal = texture4, sand_map= texture3)

    def get_points(self):
        return self.points
    def _make_floor(self, n):
        #perlin_grid = perlinNoise(n+1, n+1, 8, 8)
        perlin_grid = completeNoise(n+1, n+1, 8, 8, 4, 15)
        step = 2 / n
        points = []
        normals = [[] for _ in range((n+1)**2)]
        tangents = [[] for _ in range((n+1)**2)]
        indices = []
        for j in range(n+1):
            for i in range(n+1):
                # points and init normals
                x = -1 + i * step
                y = -1 + j * step
                x *= 2
                y *= 2
                z = perlin_grid[j][i] / 100
                delta = math.sqrt((x**2) + (y**2))
                z *= math.cos(delta*math.pi/(2*math.sqrt(2)))
                points.append((x, y, z))
        delta = (n-1)/2
        for row in range(n):
            for col in range(n):
                sradius = (row-delta)**2 + (col - delta)**2
                if (sradius <= delta**2):
                    # indices
                    a = row*(n + 1) + col
                    b = a + 1
                    d = a + (n + 1)
                    c = d + 1
                    indices.extend([a, b, c, a, c, d])
                    # prepare all normals
                    (xa, ya, za) = points[a]
                    (xb, yb, zb) = points[b]
                    (xc, yc, zc) = points[c]
                    (xd, yd, zd) = points[d]
                    ab = (xb-xa, yb-ya, zb-za)
                    ac = (xc-xa, yc-ya, zc-za)
                    ad = (xd-xa, yd-ya, zd-za)
                    # cross product
                    n1 = (ac[1]*ab[2] - ac[2]*ab[1], ac[2]*ab[0] - ac[0]*ab[2], ac[0]*ab[1] - ac[1]*ab[0])
                    n2 = (ad[1]*ac[2] - ad[2]*ac[1], ad[2]*ac[0] - ad[0]*ac[2], ad[0]*ac[1] - ad[1]*ac[0])
                    t1 = ab # u = AB
                    t2 = (xc - xd, yc - yd, zc - zd) # u = DC
                    #bt_v = (-ad[0], -ad[1], -ad[2])
                    # a & c are on both triangles
                    normals[a].append(n1)
                    normals[a].append(n2)
                    normals[b].append(n1)
                    normals[c].append(n1)
                    normals[c].append(n2)
                    normals[d].append(n2)
                    tangents[a].append(t1)
                    tangents[a].append(t2)
                    tangents[b].append(t1)
                    tangents[c].append(t1)
                    tangents[c].append(t2)
                    tangents[d].append(t2)

        # normals final value
        for n in range(len(normals)):
            normals[n] = average(*normals[n])
        for n in range(len(tangents)):
            tangents[n] = average(*tangents[n])
        # for n in range(len(bitangents)):
        #     bitangents[n] = average(*bitangents[n])

        points = tuple(points)
        indices = np.array(indices, np.uint32)
        return points, normals, tangents, indices

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)

class TexturedLava(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)

        # setup plane mesh to be textured
        scale_factor = 1.1
        height= 7
        base_coords = [(-1.0*scale_factor, -1.0*scale_factor, height), (1.0*scale_factor, -1.0*scale_factor, height), (-1.0*scale_factor, 1.0*scale_factor, height), (1.0*scale_factor, 1.0*scale_factor, height)]
        indices = [0, 1, 3, 0, 3, 2]

        mesh = Mesh(shader, attributes=dict(position=base_coords), index=indices, light_dir=(-1, -1, -1))
        
        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

class Particles(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)

        base_coords = ((-0.1, 0.1, 0), (-0.1, -0.1, 0), (0.1, 0.1, 0), (0.1, -0.1, 0))
    
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 3, 0, 3, 2), np.uint32)
        
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        super().__init__(mesh)


class TexturedWater(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_reflec, tex_refrac, tex_dudv, tex_normal, tex_depth):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)

        # setup plane mesh to be textured
        scale_factor = 100
        base_coords = [(-1.0*scale_factor, -1.0*scale_factor, 0), (1.0*scale_factor, -1.0*scale_factor, 0), (-1.0*scale_factor, 1.0*scale_factor, 0), (1.0*scale_factor, 1.0*scale_factor, 0)]

        indices = [0, 1, 3, 0, 3, 2]
        
        mesh = Mesh(shader, attributes=dict(position=base_coords), index=indices, light_dir=(-1, -1, -1))
        
        texture_reflec = Texture()
        texture_reflec.glid = tex_reflec

        texture_refrac = Texture()
        texture_refrac.glid = tex_refrac

        texture_dudv = Texture(tex_dudv, self.wrap, *self.filter)
        normal = Texture(tex_normal, self.wrap, *self.filter)

        texture_depth = Texture()
        texture_depth.glid = tex_depth

        super().__init__(mesh, reflex_map=texture_reflec, refrac_map = texture_refrac, dudv_map = texture_dudv, normal_map = normal, depth_map = texture_depth)



# -------------- Example textured plane class ---------------------------------
class TexturedPlane(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        base_coords = ((-1.0, -1.0, 0), (1.0, -1.0, 0), (-1.0, 1.0, 0), (1.0, 1.0, 0))

        scaled = 1 * np.array(base_coords, np.float32)
        indices = np.array((0, 3, 1, 0, 2, 3), np.uint32)

        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=((0,1), (1, 1), (0, 0), (1, 0))), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)


def average(*vectors):
    n = len(vectors)
    if n == 0:
        return (0, 0, 0)
    x = sum(v[0] for v in vectors) / n
    y = sum(v[1] for v in vectors) / n
    z = sum(v[2] for v in vectors) / n
    return (x, y, z)

def interp(x):
    return (3*x*x-2*x*x*x)


def get_valid_points(points):
    def in_circle(center, rayon, point):
        x, y = point
        cx, cy = center
        return math.sqrt((x-cx)**2 + (cy-y)**2) < rayon
    res = []
    volcano_center = 0,0
    volcano_rayon = 6
    sand_rayon = 10
    for p in points:
        x, z, y = p
        if not in_circle(volcano_center, volcano_rayon, (x,-z)) and \
                in_circle(volcano_center, sand_rayon, (x,-z)):
            res.append(p)
    return res

class SkyBox(Node):
    def __init__(self, children=(), transform=identity()):
        super().__init__(children, transform)
        shader = Shader("trunk_texture.vert", "trunk_texture.frag")
        front = Node(children=(TexturedPlane(shader, "skybox/front.jpg"),),
                     transform=translate(z=-1) @ rotate((0, 1, 0), 180))
        self.add(front)
        back = Node(children=(TexturedPlane(shader, "skybox/back.jpg"),),
                    transform=translate(z=1))
        self.add(back)
        left = Node(children=(TexturedPlane(shader, "skybox/left.jpg"),),
                    transform=rotate((0, 1, 0), 90) @ translate(z=1))
        self.add(left)
        right = Node(children=(TexturedPlane(shader, "skybox/right.jpg"),),
                     transform=rotate((0, 1, 0), -90) @ translate(z=1))
        self.add(right)
        top = Node(children=(TexturedPlane(shader, "skybox/top.jpg"),),
                   transform=rotate((0, 1, 0), 180) @ rotate((1, 0, 0), -90) @ translate(z=1))
        self.add(top)
        bottom = Node(children=(TexturedPlane(shader, "skybox/bottom.jpg"),),
                      transform=rotate((0, 1, 0), 180) @ rotate((1, 0, 0), 90) @ translate(z=1) )
        self.add(bottom)
    def draw(self, model, **other_uniforms):
        x, y, z = other_uniforms["w_camera_position"]
        self.transform = translate(x, y, z) @ rotate((1, 0, 0), 90)
        GL.glDisable(GL.GL_DEPTH_TEST)  # depth test now enabled (TP2)
        super().draw(model, **other_uniforms)
        GL.glEnable(GL.GL_DEPTH_TEST)  # depth test now enabled (TP2)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("texture.vert", "texture.frag")
    shader_water = Shader("water.vert", "water.frag")
    shader_lava = Shader("lava.vert", "lava.frag")
    # shader_particles = Shader("particles.vert", "particles.frag")

    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])

    water_reflection = viewer.createReflexFrameBuffer()
    water_refraction, water_depth = viewer.createRefracFrameBuffer()

    floor = TexturedFloor(shader, "grass.png", "rock.jpg","sand.jpg", "rockmap.png")
    water = TexturedWater(shader_water, water_reflection, water_refraction, "waterDUDV.png", "waternormal.png", water_depth)
    lava = TexturedLava(shader_lava, "lava.jpg")

    floor_shape = Node()
    floor_shape.add(floor)
    water_shape = Node()
    water_shape.add(water)
    lava_shape = Node()
    lava_shape.add(lava)



    water.setRequireFB(True)

    viewer.add(SkyBox())
    if len(sys.argv) != 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by assimp.' % (sys.argv[0],))
        points = get_valid_points(floor.get_points())
        viewer.add(create_trees(nb_of_trees=3, complexity=3, points=points))
        viewer.add(create_trees(nb_of_trees=1, complexity=4, points=points))
        viewer.add(create_grass(nb_of_trees=100, complexity=2, points=points))
        viewer.add(floor)
        viewer.add(water_shape)
        viewer.add(lava)

    # adding bird animation
    translate_keys, rotate_keys, scale_keys = {}, {}, {}
    for i, theta in enumerate(range(0, 361, 20)):
        theta = math.radians(theta)
        translate_keys[i*2] = vec(7*math.cos(theta),7*math.sin(theta), 9)
        rotate_keys[i*2] = quaternion_from_axis_angle(vec(1, 0, 0), 90)
        rotate_keys[i*2] = quaternion_mul(rotate_keys[i*2], quaternion_from_axis_angle(vec(0, 0, 1), theta))
        scale_keys[i*2] = 1
    #                3: quaternion_from_euler(180, 0, 180), 4: quaternion()}
    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(Gull(shader))
    viewer.add(keynode)
    viewer.run()

class Gull(Node):
    """ Very simple cylinder based on provided load function """
    def __init__(self, shader):
        super().__init__()
        self.add(*load('gull.obj', shader))  # just load cylinder from file



if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
