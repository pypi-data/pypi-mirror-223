# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 09:26:02 2021

@author: zhoup
"""

from abinitostudio.io.vasp_io import readCHGCAR
from abinitostudio.structure.plot_structure import plot_str
import numpy as np
from tvtk.api import tvtk

def plot_cell(cell, scene):
    for nr, i in enumerate(cell):
        coord = np.zeros((4, 3), dtype=float)
        coord[1] = i
        for nr2, j in enumerate(cell):
            if nr == nr2:
                continue

            coord[2] = i + j
            for nr3, k in enumerate(cell):
                if nr3 == nr or nr3 == nr2:
                    continue
                coord[3] = i + j + k
                scene.mlab.plot3d(*coord.T, color=(0, 0, 0), line_width=0.02)
                
def generate_structured_grid(x, y, z, scalars):
    pts = np.empty(z.shape + (3,), dtype=float)
    pts[..., 0] = x
    pts[..., 1] = y
    pts[..., 2] = z

    pts = pts.transpose(2, 1, 0, 3).copy()
    pts.shape = int(pts.size / 3), 3
    scalars = scalars.T.copy()

    sg = tvtk.StructuredGrid(dimensions=x.shape, points=pts)
    sg.point_data.scalars = scalars.ravel()
    sg.point_data.scalars.name = 'scalars'
    return sg

    
    

def plot_CHGCAR(filename, scene):
    
    scene.mlab.clf()
    
    grid, cell, chg = readCHGCAR(filename)
    scaled_coord = [np.linspace(0, 1, grid[i], endpoint=True) for i in range(3)]
    ABC = np.array(np.meshgrid(*scaled_coord, indexing="ij"))
    
    transformation_matrix = cell.T
    x, y, z = np.einsum('ij,jabc->iabc', transformation_matrix, ABC)
    
    sgrid = generate_structured_grid(x, y, z, chg)
    src = scene.mlab.pipeline.add_dataset(sgrid)
    max_v = np.max(chg)
    isosurface = scene.mlab.pipeline.iso_surface(src, contours=7, vmax = 1.7*max_v )
    plot_cell(cell, scene)
    supercell = (1, 1, 1)
    plot_str('POSCAR_tmp', scene, supercell)
                    

    
    # scene.mlab.clf()
    # scene.mlab.contour3d(chg, contours=4,)
    # source = scene.mlab.pipeline.scalar_field(chg)
    
    # min = chg.min()
    # max = chg.max()
    # vol = scene.mlab.pipeline.volume(source, vmin=min + 0.65 * (max - min),
    #                                vmax=min + 0.9 * (max - min))

   # scene.mlab.view(132, 54, 45, [21, 20, 21.5])
    
    