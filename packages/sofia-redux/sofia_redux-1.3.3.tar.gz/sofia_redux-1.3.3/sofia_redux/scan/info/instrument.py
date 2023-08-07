# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
from astropy import constants, units

from sofia_redux.scan.info.base import InfoBase
from sofia_redux.scan.flags.mounts import Mount

__all__ = ['InstrumentInfo']


class InstrumentInfo(InfoBase):

    def __init__(self):
        """
        Initialize the instrument information.

        The instrument information contains parameters relating to the
        observing instrument such as the observing frequency, resolution,
        sampling interval, gain, and number of channels.
        """
        super().__init__()
        self.configuration = None
        self.name = None
        self.mount = Mount.UNKNOWN
        self.frequency = np.nan * units.Unit('Hz')
        self.angular_resolution = np.nan * units.Unit('radian')
        self.resolution = np.nan * self.get_size_unit()
        self.integration_time = np.nan * units.s
        self.sampling_interval = np.nan * units.s
        self.overlap_point_size = np.nan * self.get_size_unit()
        self.gain = 1.0
        self.n_store_channels = 0
        self.n_mapping_channels = 0

    @property
    def log_id(self):
        """
        Return the string log ID for the info.

        The log ID is used to extract certain information from table data.

        Returns
        -------
        str
        """
        return 'inst'

    def set_mount(self, mount):
        """
        Set the telescope mount for the instrument.

        Parameters
        ----------
        mount : Mount or int or str
            The actual Mount flag type, it's integer representation (be
            careful it's correct), or the string name for the mount.

        Returns
        -------
        None
        """
        if isinstance(mount, int):
            self.mount = Mount(mount)
        elif isinstance(mount, str):
            self.mount = getattr(Mount, mount, None)
            if self.mount is None:
                raise ValueError(f"{mount} is not a valid Mount.")
        elif isinstance(mount, Mount):
            self.mount = mount
        else:
            raise ValueError(f"{mount!r} is not a valid Mount.")

    @staticmethod
    def get_size_unit():
        """
        Return the size unit of the instrument.

        Returns
        -------
        units.Unit
        """
        return units.Unit('arcsec')

    @staticmethod
    def get_spectral_unit():
        """
        Return the size unit of the instrument.

        Returns
        -------
        units.Unit
        """
        return units.Unit('um')

    def get_source_size(self):
        """
        Return the size of the source for the instrument.

        Returns
        -------
        units.Quantity
        """
        if self.configuration is None:
            source_size = 0.0
        else:
            source_size = self.configuration.get_float(
                'sourcesize', default=0.0)
        source_size *= self.get_size_unit()
        beam_size = self.resolution
        return np.hypot(source_size, beam_size)

    def get_stability(self):
        """
        Return the instrument stability timescale.

        The stability time scale is the expected time over which the instrument
        is expected to produce somewhat consistent results.  This is used to
        determine the number of frames from which to perform baseline
        subtraction and other operations.

        Returns
        -------
        time : units.Quantity
            The stability time for the instrument.
        """
        if self.configuration is None:
            return 10.0 * units.s
        else:
            return self.configuration.get_float('stability',
                                                default=10.0) * units.s

    def get_point_size(self):
        """
        Return the instrument point size (instrument resolution).

        Returns
        -------
        units.Quantity
        """
        return self.resolution

    def get_spectral_size(self):
        """
        Return the instrument spectral point size.

        Returns
        -------
        units.Quantity
        """
        return np.nan * self.get_spectral_unit()

    def get_data_unit(self):
        """
        Return the data unit of the instrument

        Returns
        -------
        astropy.units.Unit
        """
        if self.configuration is None:
            dataunit = 'count'
        else:
            dataunit = self.configuration.get('dataunit', default='count')
        return units.Unit(dataunit)

    def jansky_per_beam(self):
        """
        Return the Jansky's per beam.

        Returns
        -------
        astropy.units.Quantity
        """
        if (self.configuration is None
                or not self.configuration.has_option('jansky')):
            return 1.0 * units.Unit('Jy/beam')

        try:
            conversion = (1 * self.get_data_unit()).to('Jy').value
        except Exception:
            conversion = 1.0

        jansky = self.configuration.get_float('jansky')
        if self.configuration.get_bool('jansky.inverse'):
            jansky = 1.0 / jansky

        return jansky * conversion * units.Unit('Jy/beam')

    def kelvin(self):
        """
        Return the instrument temperature in Kelvin.

        Returns
        -------
        astropy.units.Quantity
        """
        if self.configuration is None:
            return np.nan * units.Unit('Kelvin')

        elif self.configuration.has_option('kelvin'):
            return (self.configuration.get_float('kelvin')
                    * units.Unit('Kelvin'))

        elif self.configuration.has_option('k2jy'):
            jy = self.jansky_per_beam().to('Jy/beam').value
            k2jy = self.configuration.get_float('k2jy')
            return jy * k2jy * units.Unit('Kelvin')

        else:
            return np.nan * units.Unit('Kelvin')

    def edit_image_header(self, header, scans=None):
        """
        Edit an image header with available information.

        Parameters
        ----------
        header : astropy.fits.Header
            The FITS header to apply.
        scans : list (Scan), optional
            A list of scans to use during editing.

        Returns
        -------
        None
        """
        header['INSTRUME'] = self.name, 'The instrument used.'
        header['V2JY'] = (self.jansky_per_beam().value,
                          '1 Jy/beam in instrument data units.')

    def validate_scan(self, scan):
        """
        Validate scan information with *THIS* information.

        Parameters
        ----------
        scan : Scan

        Returns
        -------
        None
        """
        instrument = scan.info.instrument

        if self.configuration.is_configured('frequency'):
            instrument.frequency = self.configuration.get_float(
                'frequency') * units.Unit('Hz')
        elif self.configuration.is_configured('wavelength'):
            wavelength = self.configuration.get_float(
                'wavelength') * units.Unit('um')
            instrument.frequency = (
                constants.c / wavelength).decompose().to('Hz')

        if self.configuration.is_configured('resolution'):
            instrument.resolution = self.configuration.get_float(
                'resolution') * self.get_size_unit()

        if self.configuration.is_configured('gain'):
            instrument.gain = self.configuration.get_float('gain')

    @staticmethod
    def get_focus_string(focus=None):
        """
        Return a string describing the focus.

        Parameters
        ----------
        focus : InstantFocus, optional

        Returns
        -------
        str
        """
        if focus is None:
            return "No instant focus"
        result = ''
        mm = units.Unit('mm')
        for dimension in ['x', 'y', 'z']:
            value = getattr(focus, dimension)
            weight = getattr(focus, f'{dimension}_weight')
            if value is None:
                continue
            if not isinstance(value, units.Quantity):
                value = value * mm
            if not isinstance(weight, units.Quantity):
                weight = weight / (mm ** 2)
            rms = np.sqrt(1 / weight)
            result += f'\n  Focus.dX --> {value} +- {rms}'

        return result
