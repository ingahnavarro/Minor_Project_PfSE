from dataclasses import dataclass
import numpy as np

@dataclass
class WoodProperties:
    """
    Represents the properties of a wood material.

    Args:
        name: The name of the wood material.
        specific_gravity: The specific gravity of the wood material.
        fibre_saturation_point: The fibre saturation point of the wood material.

    Returns:
        None

    Assumptions:
        The provided properties are valid (e.g., specific gravity is a positive number).
    """
    name: str
    specific_gravity: float
    fibre_saturation_point: float


@dataclass
class ElementProperties:
    """
    Represents the properties of a structural element.

    Args:
        name: The name of the element.
        width: The width of the element.
        depth: The depth of the element.
        length: The length of the element.

    Returns:
        None

    Assumptions:
        The provided dimensions are valid (positive).
    """
    name: str
    width: float
    depth: float
    length: float


import numpy as np


class WoodProperties:
    """
    Represents the properties of a wood material.

    Attributes:
        specific_gravity: The specific gravity of the wood.
        fibre_saturation_point: The fibre saturation point of the wood (%).
    """

    def __init__(self, specific_gravity: float, fibre_saturation_point: float):
        self.specific_gravity = specific_gravity
        self.fibre_saturation_point = fibre_saturation_point


class ElementProperties:
    """
    Represents the properties of a structural element.

    Attributes:
        width: The width of the element.
        depth: The depth of the element.
        length: The length of the element.
    """

    def __init__(self, width: float, depth: float, length: float):
        self.width = width
        self.depth = depth
        self.length = length


class WeightCalculator:
    """
    Calculates the weight of a wood element considering moisture content.

    Attributes:
        material (WoodProperties): Properties of the wood material.
        element (ElementProperties): Properties of the structural element.

    Methods:
        calculate_density_at_moisture_content(moisture_content) -> float:
            Calculates the density of the wood element considering its moisture content.
            Units: kg/m^3
        calculate_weight_at_moisture_content(moisture_content) -> float:
            Calculates the weight of the wood element considering its moisture content.
            Units: kg
    """

    def __init__(
        self,
        material: WoodProperties,
        element: ElementProperties,
    ):
        self.material = material
        self.element = element

    def calculate_density_at_moisture_content(self, moisture_content: float) -> float:
        """
        Calculates the density of the wood element at a given moisture content.

        Args:
            moisture_content: The moisture content of the wood, as a percentage.

        Returns:
            The density of the wood element in kg/m^3.

        Assumptions:
            - The moisture content is given as a percentage (e.g., 12.5 for 12.5%).
            - Density of water is 1000 kg/m^3
        """
        if not isinstance(moisture_content, (int, float)): #Errores: Added validation for moisture_content type
            raise TypeError("Moisture content must be a number (int or float)")
        if moisture_content < 0: #Errores: Added validation for moisture_content
            raise ValueError("Moisture content must be non-negative.")
        if self.material.fibre_saturation_point < 0: #Errores: Added validation for fibre saturation point
             raise ValueError("Fibre saturation point must be non-negative.")

        if moisture_content <= self.material.fibre_saturation_point: #Mejora: Changed the logic to consider fibre saturation point as the max density
            density_at_moisture = (
                self.material.specific_gravity
                * 1000
                * ((moisture_content / 100) + 1)
                / (
                    (self.material.fibre_saturation_point / 100)
                    * self.material.specific_gravity
                    + 1
                )
            )
        else: #Mejora: If moisture content is higher than fibre saturation point, density remains constant
            density_at_moisture = (
                self.material.specific_gravity
                * 1000
                * (
                    (self.material.fibre_saturation_point / 100)
                    + 1
                )
                / (
                    (self.material.fibre_saturation_point / 100)
                    * self.material.specific_gravity
                    + 1
                )
            )
        return density_at_moisture

    def calculate_weight_at_moisture_content(self, moisture_content: float) -> float:
        """
        Calculates the weight of the wood element at a given moisture content.

        Args:
            moisture_content: The moisture content of the wood, as a percentage.

        Returns:
            The weight of the wood element in kg.

        Assumptions:
           - The provided dimensions are valid (positive).
        """

        if not isinstance(moisture_content, (int, float)): #Errores: Validate the type of the input
            raise TypeError("Moisture content must be a number (int or float)")
        if moisture_content < 0:  #Errores: Add validation for moisture_content
            raise ValueError("Moisture content must be non-negative.")
        if self.element.width < 0 or self.element.depth < 0 or self.element.length < 0: #Errores: Added validation for attributes
            raise ValueError("Element dimensions must be non-negative values.")

        volume = self.element.width * self.element.depth * self.element.length  #Claridad: Calculate volume
        density = self.calculate_density_at_moisture_content(moisture_content)
        weight = volume * density #Claridad: Calculate the weight using the density
        return weight