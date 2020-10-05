from netgen.geom2d import unit_square
from ngsolve import Mesh
from ngstents import TentSlab


def test_tent_properties():
    mesh = Mesh(unit_square.GenerateMesh(maxh=.2))
    mesh.Refine()
    mesh.Refine()
    dt = 0.05
    c = 16
    method = "vol"
    
    # Tent slab tests
    tentslab = TentSlab(mesh, method, 100000000)
    tentslab.SetWavespeed(c)
    success = tentslab.PitchTents(dt)
    try:
        assert success is True
    except AssertionError as e:
        msg = "Slab could not be pitched"
        e.args += ("Failed to pitch slab", msg)
        raise
    ntents = tentslab.GetNTents()
    maxslope = tentslab.MaxSlope()
    try:
        assert maxslope <= 1.0/c
    except AssertionError as e:
        msg = "max slope = " + str(maxslope)
        msg += "   1.0/c = " + str(1.0/c)
        e.args += ("Failed at MaxSlopeTest!", msg)
        raise

    tentslab.DrawPitchedTentsVTK()  # should create output.vtk

    # for ngsgui / tents_visualization and webgui
    results = tentslab.DrawPitchedTentsGL()
    tentdata, tenttimes, ntents, nlevels = results
    print(ntents)


if __name__ == "__main__":
    test_tent_properties()
