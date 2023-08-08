import contextlib

import h5py
from nxtomo.io import HDF5File

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass
from silx.io.url import DataUrl


class _BaseReader(contextlib.AbstractContextManager):
    def __init__(self, url: DataUrl):
        if not isinstance(url, DataUrl):
            raise TypeError(f"url should be an instance of DataUrl. Not {type(url)}")
        if url.scheme() not in ("silx", "h5py"):
            raise ValueError("Valid scheme are silx and h5py")
        if url.data_slice() is not None:
            raise ValueError(
                "Data slices are not managed. Data path should "
                "point to a bliss node (h5py.Group)"
            )
        self._url = url
        self._file_handler = None

    def __exit__(self, *exc):
        return self._file_handler.close()


class EntryReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = HDF5File(filename=self._url.file_path(), mode="r")
        if self._url.data_path() == "":
            entry = self._file_handler
        elif self._url.data_path() not in self._file_handler:
            raise KeyError(
                f"data path '{self._url.data_path()}' doesn't exists from '{self._url.file_path()}'"
            )
        else:
            entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Group):
            raise ValueError("Data path should point to a bliss node (h5py.Group)")
        return entry


class DatasetReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = HDF5File(filename=self._url.file_path(), mode="r")
        entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Dataset):
            raise ValueError(
                f"Data path ({self._url.path()}) should point to a dataset (h5py.Dataset)"
            )
        return entry
