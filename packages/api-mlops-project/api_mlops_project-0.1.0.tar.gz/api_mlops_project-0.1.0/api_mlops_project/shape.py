from pydantic import BaseModel


class DataInput(BaseModel):
    """
    Model class for vibration data input.

    Attributes:
        vibration_x (float): Vibration value along the X-axis.
        vibration_y (float): Vibration value along the Y-axis.
        vibration_z (float): Vibration value along the Z-axis.
    """

    vibration_x: float
    vibration_y: float
    vibration_z: float
