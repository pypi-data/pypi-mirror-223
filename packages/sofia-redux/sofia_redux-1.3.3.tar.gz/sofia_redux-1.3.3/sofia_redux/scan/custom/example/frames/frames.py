# Licensed under a 3-clause BSD style license - see LICENSE.rst

from astropy import log

from sofia_redux.scan.custom.example.flags.frame_flags import ExampleFrameFlags
from sofia_redux.scan.frames.horizontal_frames import HorizontalFrames

__all__ = ['ExampleFrames']


class ExampleFrames(HorizontalFrames):

    flagspace = ExampleFrameFlags

    def __init__(self):
        """
        Initialize frames for the example instrument.
        """
        super().__init__()
        self.default_info = None

    def copy(self):
        """
        Return a copy of the frames for the example instrument.

        Returns
        -------
        ExampleFrames
        """
        return super().copy()

    @property
    def info(self):
        """
        Return the scan info object.

        Returns
        -------
        ExampleInfo
        """
        info = super().info
        if info is not None:
            return info
        return self.default_info

    @property
    def site(self):
        """
        Return the site coordinates of the associated scan.

        Returns
        -------
        GeodeticCoordinates
        """
        return self.info.astrometry.site

    def read_hdu(self, hdu):
        """
        Read a single data HDU.

        Parameters
        ----------
        hdu : astropy.io.fits.hdu.table.BinTableHDU
            A data HDU containing "timestream" data.

        Returns
        -------
        None
        """
        table = hdu.data

        if 'DAC' in table.columns.names:
            log.debug("Reading data from HDU")
            data = table['DAC']
            n_records, n_rows, n_cols = data.shape
            log.debug(f"FITS HDU has {n_records} "
                      f"({n_rows} x {n_cols}) arrays.")

            row, col = self.channels.data.row, self.channels.data.col
            self.data[:] = data[:, row, col]
            log.debug('Done.')
        else:
            log.debug("No DAC column found in Data HDU.")

        self.info.set_frames_coordinates(self, table)
        self.chopper_position.zero()
        self.valid[:] = True
