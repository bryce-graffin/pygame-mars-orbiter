"""
Module containing utility functions for various calculations.
"""

def calculate_eccentricity(dist_list: list) -> float:
    """
    Calculate & return eccentricity (deviation of orbit from circularity) from a list of radii.

    Note: This should return a value between `0.0` and `1.0`, where `0.0` is a perfectly circular orbit and `1.0` is a parabolic trajectory (i.e., escape trajectory).

    :param dist_list: List of distances from the center of the planet at various points in the orbit.
    :type dist_list: list
    """
    # potential future improvement: make apoapsis/periapsis attr. of the satellite and update during each loop
    apoapsis = max(dist_list)  # highest point in orbit
    periapsis = min(dist_list)  # lowest point in orbit
    return (apoapsis - periapsis) / (apoapsis + periapsis)  # eccentricity formula
