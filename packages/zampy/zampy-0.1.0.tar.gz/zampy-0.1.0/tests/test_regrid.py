"""Unit test for regridding."""

import numpy as np
import pytest
from test_datasets import data_folder
from zampy.datasets.dataset_protocol import SpatialBounds
from zampy.datasets.eth_canopy_height import parse_tiff_file
from zampy.utils import regrid


path_dummy_data = data_folder / "eth-canopy-height"
XESMF_INSTALLED = True
# Since xesmf is only supported via conda, we need these checks to support
# tests cases running with and without conda environment in CD/CI
try:
    import xesmf as _  # noqa: F401 (unused import)
except ImportError:
    XESMF_INSTALLED = False

# ruff: noqa: B018


@pytest.mark.skipif(XESMF_INSTALLED, reason="xesmf is installed")
def assert_xesmf_available() -> None:
    """Test assert_xesmf_available function with exception case."""
    with pytest.raises(ImportError, match="Could not import the `xesmf`"):
        regrid.assert_xesmf_available()


@pytest.fixture
def dummy_dataset():
    ds = parse_tiff_file(
        path_dummy_data / "ETH_GlobalCanopyHeight_10m_2020_N51E003_Map.tif",
    )
    return ds


def test_infer_resolution(dummy_dataset):
    """Test resolution inferring function."""
    (resolution_lat, resolution_lon) = regrid.infer_resolution(dummy_dataset)
    expected_lat = 0.01
    expected_lon = 0.01

    assert resolution_lat == pytest.approx(expected_lat, 0.001)
    assert resolution_lon == pytest.approx(expected_lon, 0.001)


def test_groupby_regrid(dummy_dataset):
    """Test groupby regrid function."""
    bbox = SpatialBounds(54, 6, 51, 3)
    ds = regrid._groupby_regrid(data=dummy_dataset, spatial_bounds=bbox, resolution=1.0)
    expected_lat = [51.0, 52.0, 53.0, 54.0]
    expected_lon = [3.0, 4.0, 5.0, 6.0]

    np.testing.assert_allclose(ds.latitude.values, expected_lat)
    np.testing.assert_allclose(ds.longitude.values, expected_lon)


def test_interp_regrid(dummy_dataset):
    """Test interp regrid function."""
    bbox = SpatialBounds(51.1, 3.1, 51, 3)
    ds = regrid._interp_regrid(data=dummy_dataset, spatial_bounds=bbox, resolution=0.05)
    expected_lat = [51.0, 51.05, 51.1]
    expected_lon = [3.0, 3.05, 3.1]

    np.testing.assert_allclose(ds.latitude.values, expected_lat)
    np.testing.assert_allclose(ds.longitude.values, expected_lon)


def test_flox_regrid_coarser(dummy_dataset):
    """Test flox regridding at a coarser resolution

    Note that the native resolution is about lat/lon=0.01.
    """
    bbox = SpatialBounds(54, 6, 51, 3)
    ds = regrid.flox_regrid(data=dummy_dataset, spatial_bounds=bbox, resolution=1.0)
    expected_lat = [51.0, 52.0, 53.0, 54.0]
    expected_lon = [3.0, 4.0, 5.0, 6.0]

    np.testing.assert_allclose(ds.latitude.values, expected_lat)
    np.testing.assert_allclose(ds.longitude.values, expected_lon)


def test_flox_regrid_finer(dummy_dataset):
    """Test flox regridding at a finer resolution

    Note that the native resolution is about lat/lon=0.01.
    """
    bbox = SpatialBounds(51.02, 3.02, 51, 3)
    ds = regrid.flox_regrid(data=dummy_dataset, spatial_bounds=bbox, resolution=0.002)
    # only compare first 5 index
    expected_lat = [51.0, 51.002, 51.004, 51.006, 51.008]
    expected_lon = [3.0, 3.002, 3.004, 3.006, 3.008]

    np.testing.assert_allclose(ds.latitude.values[:5], expected_lat)
    np.testing.assert_allclose(ds.longitude.values[:5], expected_lon)


def test_flox_regrid_close(dummy_dataset):
    """Test flox regridding at a resolution close to native.

    Note that the native resolution is about lat/lon=0.01.
    """
    bbox = SpatialBounds(51.1, 3.1, 51, 3)
    ds = regrid.flox_regrid(data=dummy_dataset, spatial_bounds=bbox, resolution=0.02)
    expected_lat = [51.0, 51.02, 51.04, 51.06, 51.08, 51.1]
    expected_lon = [3.0, 3.02, 3.04, 3.06, 3.08, 3.1]

    np.testing.assert_allclose(ds.latitude.values, expected_lat)
    np.testing.assert_allclose(ds.longitude.values, expected_lon)


def test_regrid_data_flox(dummy_dataset):
    bbox = SpatialBounds(54, 6, 51, 3)
    ds = regrid.regrid_data(
        data=dummy_dataset, spatial_bounds=bbox, resolution=1.0, method="flox"
    )
    expected_lat = [51.0, 52.0, 53.0, 54.0]
    expected_lon = [3.0, 4.0, 5.0, 6.0]

    np.testing.assert_allclose(ds.latitude.values, expected_lat)
    np.testing.assert_allclose(ds.longitude.values, expected_lon)


def test_regrid_data_unknown_method(dummy_dataset):
    bbox = SpatialBounds(54, 6, 51, 3)
    with pytest.raises(ValueError):
        regrid.regrid_data(
            data=dummy_dataset,
            spatial_bounds=bbox,
            resolution=1.0,
            method="fake_method",
        )
