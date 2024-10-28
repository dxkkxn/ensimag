# Inspired from https://gamedevelopment.tutsplus.com/tutorials/create-a-glowing-flowing-lava-river-using-bezier-curves-and-shaders--gamedev-919


import numpy as np
from transform import normalized, vec


class Point:

    def __init__(self, x, y):

        self.x = x

        self.y = y

    def __str__(self):

        return "Point(%s, %s)" % (self.x, self.y)

class Node:

    def __init__(self, position, control):

        self.position = position

        self.control = control

    def __str__(self):

        return "Node(%s, %s)" % (self.position, self.control)


# Calculate point coordinates on a quadratic bezier curve
def quadraticBezier(P0:Point, P1:Point, C:Point, t:float):
    x = (1 - t) * (1 - t) * P0.x + (2 - 2 * t) * t * C.x + t * t * P1.x

    y = (1 - t) * (1 - t) * P0.y + (2 - 2 * t) * t * C.y + t * t * P1.y

    return Point(x, y)


def convert_to_points(nodes , quality=10):
    points = []
    precision = 1 / quality
    steps = np.arange(0, 1+precision, precision)

    for i in range(len(nodes) - 1):
        current = nodes[i]
        next = nodes[i + 1]

        for step in steps:
            new_point = quadraticBezier(current.position, next.position, current.control, step)
            points.append(new_point)

    return points

def give_width(nodes, width):
    nodesWithOffset = []
    for i in range(len(nodes)):
        if i==0:
            normal = lineNormal(nodes[i].position, nodes[i].control)
            surface = lineNormal(nodes[i].position, nodes[i+1].position)
        elif i==len(nodes)-1:
            normal = lineNormal(nodes[i-1].control, nodes[i].position)
            surface = lineNormal(nodes[i-1].position, nodes[i].position)
        else:
            normal1 = lineNormal(nodes[i].position, nodes[i].control)
            normal2 = lineNormal(nodes[i-1].control, nodes[i].position)
            normal = Point(0.5*(normal1.x + normal2.x), 0.5*(normal1.y + normal2.y))
            normal = normalized(vec(normal.x, normal.y))
            normal = Point(normal[0], normal[1])
            surface = lineNormal(nodes[i].position, nodes[i+1].position)

        nodesWithOffset.append(
            Node(Point(nodes[i].position.x + normal.x * width,
            nodes[i].position.y + normal.y * width),
            Point(nodes[i].control.x + surface.x * width,
            nodes[i].control.y + surface.y * width))
        )
    return nodesWithOffset

def lineNormal(p1, p2):
    return Point(p2.y - p1.y, p1.x - p2.x)

def indice_curve(nodes):
    indice = []
    length= int(len(nodes)/2)
    for i in range(length-1):
        #making the square with 4 nodes
        # first triangle
        indice.append((len(nodes)/2)+i)
        indice.append(i+1)
        indice.append(i)
        # second triangle
        indice.append((len(nodes)/2)+i)
        indice.append((len(nodes)/2)+i+1)
        indice.append(i+1)
    return indice

def build_curve():
    nodes = [Node(Point(0, 0), Point(0.5, 0.3)), Node(Point(1, 0), Point(1.5, -0.2)), Node(Point(2, 0), Point(2.5, 1))]
    result = convert_to_points(nodes)
    nodes_width = give_width(nodes, 0.1)
    result_width = convert_to_points(nodes_width)
    result.extend(result_width)
    points =[]
    for point in result:
        tuple = (point.x, point.y, 0)
        points.append(tuple)
    indice = indice_curve(result)
    return points, indice

        
if __name__ == '__main__':
    nodes = [Node(Point(0, 0), Point(0.5, 0.3)), Node(Point(1, 0), Point(1.5, -0.2)), Node(Point(2, 0), Point(2.5, 1))]
    result = convert_to_points(nodes)
    nodes_width = give_width(nodes, 1)
    result_width = convert_to_points(nodes_width)
    nodes_river = result.append(result_width)


    # for point in result:
    #     print(point)