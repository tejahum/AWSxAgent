import math
from typing import Dict, Any
from pymongo import MongoClient, errors

def simulate_rocket_launch(thrust: float, mass: float, burn_time: float, dt: float = 0.1) -> float:
    """
    Simulates a very basic vertical rocket launch using constant thrust.
    Returns the maximum altitude (in meters) reached.

    Parameters:
    - thrust: constant thrust force in newtons
    - mass: total mass in kilograms
    - burn_time: duration of thrust in seconds
    - dt: simulation time step in seconds
    """
    g = 9.81  # gravity (m/s²)
    velocity = 0.0
    altitude = 0.0
    for t in [i * dt for i in range(int(burn_time / dt))]:
        acceleration = (thrust / mass) - g
        velocity += acceleration * dt
        altitude += velocity * dt
    if velocity > 0:
        altitude += (velocity**2) / (2 * g)
    return altitude
