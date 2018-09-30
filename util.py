from numpy import arctan, sqrt, pi


def cart_to_polar(x, y):
    """returns r absolute distance and theta in (-pi, pi)"""
    r = sqrt(x**2 + y**2)
    theta = arctan(x/y)
    # if quadrant II
    if (x < 0) & (y > 0):
        theta += pi
    # if quadrant III
    if (x < 0) & (y < 0):
        theta -= pi
    return r, theta


def highway_location_to_polar(x, delta_lane):
    return cart_to_polar(delta_lane * 3.7, x)