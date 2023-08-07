# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest

from sofia_redux.toolkit.resampling.grid.base_grid import BaseGrid
from sofia_redux.toolkit.resampling.tree.base_tree import BaseTree


def test_regular():
    rand = np.random.RandomState(42)
    grid = BaseGrid(np.arange(3), np.arange(3))
    assert grid.regular
    grid = BaseGrid(rand.random((2, 3)))
    assert not grid.regular
    with pytest.raises(AttributeError) as err:
        grid.regular = False
    assert "has no setter" in str(err.value)


def test_singular():
    grid = BaseGrid(np.arange(3), np.arange(3))
    assert not grid.singular
    grid = BaseGrid(1, 1)
    with pytest.raises(AttributeError) as err:
        grid.singular = True
    assert "has no setter" in str(err.value)


def test_shape():
    grid = BaseGrid(np.arange(3), np.arange(4))
    assert grid.shape == (4, 3)
    with pytest.raises(AttributeError) as err:
        grid.shape = (2, 3)
    assert "has no setter" in str(err.value)


def test_size():
    grid = BaseGrid(np.arange(3), np.arange(4))
    assert grid.size == 12
    with pytest.raises(AttributeError) as err:
        grid.size = 100
    assert "has no setter" in str(err.value)


def test_scale_factor():
    grid = BaseGrid(np.arange(3), np.arange(4), scale_factor=[2, 3],
                    scale_offset=[4, 5])
    assert np.allclose(grid.scale_factor, [2, 3])
    with pytest.raises(AttributeError) as err:
        grid.scale_factor = None
    assert "has no setter" in str(err.value)


def test_scale_offset():
    grid = BaseGrid(np.arange(3), np.arange(4), scale_factor=[2, 3],
                    scale_offset=[4, 5])
    assert np.allclose(grid.scale_offset, [4, 5])
    with pytest.raises(AttributeError) as err:
        grid.scale_offset = None
    assert "has no setter" in str(err.value).lower()


def test_tree_class():
    grid = BaseGrid(np.arange(3), np.arange(4))
    assert grid.tree_class == BaseTree
    with pytest.raises(AttributeError) as err:
        grid.tree_class = None
    assert "has no setter" in str(err.value).lower()
