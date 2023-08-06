from gym_cas import *
from gym_cas.vector import Arrow2DSeries, Arrow3DSeries

def test_plot_vector_2d():
    p = plot_vector([1,2],show=False)
    s = p.series
    assert isinstance(p, MB)
    assert len(s) == 1
    assert isinstance(s[0], Arrow2DSeries)
    assert (s[0].get_data() == [[0],[0],[1],[2]]).all()


def test_plot_vector_3d():
    p = plot_vector([1, 2, 3],show=False)
    s = p.series
    assert isinstance(p, MB)
    assert len(s) == 1
    assert isinstance(s[0], Arrow3DSeries)
    assert not s[0].is_streamlines
    assert (s[0].get_data() == [[0],[0],[0],[1],[2],[3]]).all()
    assert s[0].get_label(False) == ""
