
import math
from typing import Dict

def calculate_flow_rate(area: float, velocity: float) -> float:
    """
    Calculate volumetric flow rate Q given cross-sectional area and fluid velocity.
    
    Q = A * v
    
    :param area: Cross-sectional area (m²)
    :param velocity: Fluid velocity (m/s)
    :return: Flow rate (m³/s)
    """
    return area * velocity

def calculate_velocity(flow_rate: float, area: float) -> float:
    """
    Calculate fluid velocity v given flow rate and cross-sectional area.
    
    v = Q / A
    
    :param flow_rate: Volumetric flow rate (m³/s)
    :param area: Cross-sectional area (m²)
    :return: Velocity (m/s)
    """
    return flow_rate / area

def cylinder_force(pressure: float, piston_area: float) -> float:
    """
    Calculate the force on a hydraulic piston.
    
    F = P * A
    
    :param pressure: Fluid pressure (Pa)
    :param piston_area: Piston face area (m²)
    :return: Force (N)
    """
    return pressure * piston_area

def pressure_from_force(force: float, piston_area: float) -> float:
    """
    Calculate fluid pressure given force and piston area.
    
    P = F / A
    
    :param force: Force applied to piston (N)
    :param piston_area: Piston face area (m²)
    :return: Pressure (Pa)
    """
    return force / piston_area

def pump_power(flow_rate: float, pressure_increase: float, efficiency: float = 1.0) -> float:
    """
    Estimate hydraulic pump power required.
    
    Power = (Q * ΔP) / η
    
    :param flow_rate: Flow rate delivered by pump (m³/s)
    :param pressure_increase: Pressure rise across pump (Pa)
    :param efficiency: Pump efficiency (0 < η ≤ 1)
    :return: Power (W)
    """
    return (flow_rate * pressure_increase) / efficiency

def darcy_weisbach_pressure_drop(
    length: float,
    diameter: float,
    flow_rate: float,
    density: float,
    viscosity: float,
    roughness: float = 1e-6
) -> float:
    """
    Compute pressure drop ΔP over a pipe using the Darcy–Weisbach equation.
    Approximates friction factor f via Blasius (for turbulent) or laminar formula.
    
    ΔP = f * (L/D) * (ρ * v² / 2)
    
    :param length: Pipe length (m)
    :param diameter: Pipe diameter (m)
    :param flow_rate: Volumetric flow rate (m³/s)
    :param density: Fluid density (kg/m³)
    :param viscosity: Fluid dynamic viscosity (Pa·s)
    :param roughness: Pipe absolute roughness (m)
    :return: Pressure drop (Pa)
    """
    A = math.pi * (diameter / 2) ** 2
    v = flow_rate / A
    Re = density * v * diameter / viscosity
    
    if Re < 2300:
        f = 64 / Re
    else:
        f = 0.079 * Re ** (-0.25)
    
    deltaP = f * (length / diameter) * (density * v ** 2 / 2)
    return deltaP

if __name__ == "__main__":
    print("Flow rate:", calculate_flow_rate(area=0.01, velocity=2.0), "m³/s")
    print("Cylinder force:", cylinder_force(pressure=2e7, piston_area=0.005), "N")
    print("Pump power:", pump_power(flow_rate=0.02, pressure_increase=5e6, efficiency=0.85), "W")
    print("Pressure drop:", darcy_weisbach_pressure_drop(
        length=10, diameter=0.05, flow_rate=0.02, density=1000, viscosity=1e-3
    ), "Pa")
