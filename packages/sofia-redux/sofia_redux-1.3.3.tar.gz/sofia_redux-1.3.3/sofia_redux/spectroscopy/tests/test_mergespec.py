# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest

from sofia_redux.spectroscopy.mergespec import mergespec
from sofia_redux.toolkit.utilities.fits import set_log_level


@pytest.fixture
def spectra():
    spec1 = np.zeros((4, 10))
    spec1[0] = np.arange(10)
    spec1[1] = 1
    spec1[2] = 3
    spec1[3] = np.arange(10) % 2
    spec2 = np.zeros((4, 10))
    spec2[0] = np.arange(10) + 5.5
    spec2[1] = 2
    spec2[2] = 4
    spec2[3] = 2
    return spec1, spec2


def test_invalid_input(spectra):
    spec1, spec2 = spectra
    with pytest.raises(ValueError) as err:
        mergespec(spec1[0], spec2[0])
    assert "must have 2 dimensions" in str(err.value)
    with pytest.raises(ValueError) as err:
        mergespec([spec1[0]], [spec2[0]])
    assert "must have 2 or more rows" in str(err.value)
    with pytest.raises(ValueError) as err:
        mergespec(spec1, spec2[:-1])
    assert "must have equal rows" in str(err.value)


def test_no_overlap(spectra):
    spec1, spec2 = spectra
    spec2[0] += 100
    info = {}
    result = mergespec(spec1, spec2, info=info)
    assert np.isnan(info['overlap_range']).all()

    u = np.append(spec1, spec2, axis=1)
    u[1:, spec1.shape[1] - 1: spec1.shape[1] + 1] = np.nan
    assert np.allclose(u, result, equal_nan=True)

    # same result with spectra switched:
    # range is dynamically determined
    result = mergespec(spec2, spec1, info=info)
    assert np.allclose(u, result, equal_nan=True)


def test_edge_overlap(spectra):
    spec1, spec2 = spectra
    info = {}
    result = mergespec(spec1, spec2, info=info)
    assert np.allclose(result[:, :4], spec1[:, :4])
    assert np.allclose(result[:, -4:], spec2[:, -4:])
    assert np.allclose(result[:, 6], [6, 1.27, 2.56, 2], atol=0.01)
    assert np.allclose(result[:, 7], [7, 1.27, 2.56, 3], atol=0.01)
    assert np.allclose(info['overlap_range'], [6, 8])


def test_inside_overlap(spectra):
    spec1, spec2 = spectra
    spec2 = spec2[:, :3]
    info = {}
    result = mergespec(spec1, spec2, info=info)
    assert np.allclose(info['overlap_range'], [6, 7])
    assert np.allclose(result[:, :6], spec1[:, :6])
    assert np.allclose(result[:, 8:], spec1[:, 8:])
    assert np.allclose(result[:, 6], [6, 1.27, 2.56, 2], atol=0.01)
    assert np.allclose(result[:, 7], [7, 1.27, 2.56, 3], atol=0.01)


def test_dimensions_and_sum(spectra):
    ospec1, ospec2 = spectra
    spec1, spec2 = ospec1[:3], ospec2[:3]
    result = mergespec(spec1, spec2)
    assert np.allclose(result[:, 6], [6, 1.27, 2.56], atol=0.01)
    result = mergespec(spec1, spec2, sum_flux=True)
    assert np.allclose(result[:, 6], [6, 3, 5.74], atol=0.01)
    spec1, spec2 = ospec1[:2], ospec2[:2]
    result = mergespec(spec1, spec2)
    assert np.allclose(result[:, 6], [6, 1.5])
    result = mergespec(spec1, spec2, sum_flux=True)
    assert np.allclose(result[:, 6], [6, 3])


def test_nans(spectra):
    ospec1, ospec2 = spectra
    spec1, spec2 = ospec1.copy(), ospec2.copy()
    spec1[0, 0] = np.nan
    result = mergespec(spec1, spec2)
    assert result[0, 0] == 1
    spec1 = ospec1.copy()
    spec1[1, 0] = np.nan
    result = mergespec(spec1, spec2)
    assert result[0, 0] == 1
    spec1 = ospec1.copy()
    spec1[1, 7] = np.nan
    result = mergespec(spec1, spec2)
    assert np.allclose(result[:, 7], [7, np.nan, 0, 3], equal_nan=True)
    result = mergespec(spec1, spec2, sum_flux=True)
    assert np.allclose(result[:, 7], [7, np.nan, 5.74, 3],
                       equal_nan=True, atol=0.01)


@pytest.mark.parametrize('statistic,local',
                         [('mean', True), ('mean', False),
                          ('median', True), ('median', False),
                          ('max', True), ('max', False)])
def test_s2n_threshold(spectra, capsys, statistic, local):
    ospec1, ospec2 = spectra
    spec1, spec2 = ospec1.copy(), ospec2.copy()

    # good threshold passed, all data okay, result as expected
    result = mergespec(spec1, spec2, s2n_threshold=1.0,
                       s2n_statistic=statistic, local_noise=True)
    assert np.allclose(result[:, :4], spec1[:, :4])
    assert np.allclose(result[:, -4:], spec2[:, -4:])
    assert np.allclose(result[:, 6], [6, 1.27, 2.56, 2], atol=0.01)
    assert np.allclose(result[:, 7], [7, 1.27, 2.56, 3], atol=0.01)
    assert result.shape == (4, 15)
    assert np.sum(np.isnan(result)) == 0
    assert 'Bad S/N' not in capsys.readouterr().err

    # high error, low signal for one point in
    # spec2 in overlap => use spec1 value
    spec1, spec2 = ospec1.copy(), ospec2.copy()
    spec2[1, 1] /= 1000
    spec2[2, 1] *= 1000

    with set_log_level('DEBUG'):
        result2 = mergespec(spec1, spec2, s2n_threshold=1.0,
                            s2n_statistic=statistic, local_noise=local)
    assert result2.shape == (4, 15)
    assert np.sum(np.isnan(result2)) == 0
    assert np.allclose(result2[:, 7], [7, 1, 3, 3], atol=0.01)
    capt = capsys.readouterr()
    assert 'Bad S/N' not in capt.err
    assert statistic in capt.out
    if local:
        assert 'sliding standard dev' in capt.out
    else:
        assert 'input error' in capt.out

    # same result if testing on noise only
    result3 = mergespec(spec1, spec2, s2n_threshold=1.0, noise_test=True,
                        s2n_statistic=statistic, local_noise=local)
    assert result3.shape == (4, 15)
    assert np.sum(np.isnan(result3)) == 0
    assert np.allclose(result2[:, 7], [7, 1, 3, 3], atol=0.01)
    assert 'Bad S/N' not in capsys.readouterr().err

    # bad data - threshold ignored
    spec1, spec2 = ospec1.copy(), ospec2.copy()
    spec1[1] *= -1
    result = mergespec(spec1, spec2, s2n_threshold=1.0,
                       s2n_statistic=statistic, local_noise=local)
    assert np.sum(np.isnan(result)) == 0
    assert 'Bad S/N; ignoring threshold' in capsys.readouterr().err
