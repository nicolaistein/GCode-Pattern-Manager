import igl
import numpy as np
import os
from logger import log


class LSCM:
    def __init__(self, objPath):
        self.objPath = objPath

    def execute(self):
        root_folder = os.getcwd()

        v, f = igl.read_triangle_mesh(os.path.join(root_folder, self.objPath))
        log("Vertices: " + str(len(v)))
        log("Faces: " + str(len(f)))

        if len(f) > 0 and type(f[0]) is not np.ndarray:
            f = np.matrix([list(f)])

        b = np.array([2, 1])
        bnd = igl.boundary_loop(f)
        log("Boundary loop length: " + str(len(bnd)))

        b[0] = bnd[0]
        b[1] = bnd[int(bnd.size / 2)]

        bc = np.array([[0.0, 0.0], [1.0, 0.0]])
        _, uv = igl.lscm(v, f, b, bc)

        return uv
