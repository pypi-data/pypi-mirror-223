from typing import Iterable
import h5py
import numpy
from silx.io.utils import h5py_read_dataset

from nxtomo.io import HDF5File


def cast_and_check_array_1D(array, array_name):
    if not isinstance(array, (type(None), numpy.ndarray, Iterable)):
        raise TypeError(
            f"{array_name} is expected to be None, or an Iterable. Not {type(array)}"
        )
    if array is not None and not isinstance(array, numpy.ndarray):
        array = numpy.asarray(array)
    if array is not None and array.ndim > 1:
        raise ValueError(f"{array_name} is expected to be 0 or 1d not {array.ndim}")
    return array


def get_data_and_unit(file_path, data_path, default_unit):
    with HDF5File(file_path, mode="r") as h5f:
        if data_path in h5f and isinstance(h5f[data_path], h5py.Dataset):
            dataset = h5f[data_path]
            unit = None
            if "unit" in dataset.attrs:
                unit = dataset.attrs["unit"]
            elif "units" in dataset.attrs:
                unit = dataset.attrs["units"]
            else:
                unit = default_unit
            if hasattr(unit, "decode"):
                # handle Diamond dataset
                unit = unit.decode()
            return h5py_read_dataset(dataset), unit
        else:
            return None, default_unit


def get_data(file_path, data_path):
    with HDF5File(file_path, mode="r") as h5f:
        if data_path in h5f:
            return h5py_read_dataset(h5f[data_path])
        else:
            return None
