import os
import pkg_resources
import numpy as np
from typing import Union
from .geometry import FoilGeom


class Database(FoilGeom):
    def __init__(
        self,
        name: str,
        n_side: Union[int, None] = None,
        closedTE: bool = True,
        **spacing_kwargs,
    ):
        fname = os.path.join(f"airfoil_database", f"{name}.dat")
        # import the geometry file using pkg_resource so that it could be included in dist
        coord = np.loadtxt(pkg_resources.resource_stream(__name__, fname), skiprows=1)
        super().__init__(coord, n_side, closedTE, name, **spacing_kwargs)
