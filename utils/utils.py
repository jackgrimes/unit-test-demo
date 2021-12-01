from math import pi


def area_of_cirle(r):
    return pi * r ** 2


def volume_of_cylinder(r, h):
    return h * area_of_cirle(r)
