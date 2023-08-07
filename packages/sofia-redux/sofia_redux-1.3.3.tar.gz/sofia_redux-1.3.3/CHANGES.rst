1.3.3
=====
- Updated FIFI-LS pipeline to v2.8.0, including separate spatial flats for
  each dichroic.
- Updated calibration files for HAWC, FORCAST, and EXES for prior cycles with
  new analysis from data reprocessing efforts.
- Minor updates for compatibility with third-party dependency changes.
- Update packaging for PEP compliance.

1.3.2 (2023-03-29)
==================
- Minor bug fixes for EXES edge cases (raster flats with non-standard
  overlaps; occasional spurious zero-length orders).
- Updated calibration files for EXES.
- Environment update for astropy management.


1.3.1 (2023-02-11)
==================
- Minor fixes for the spectral viewer, relating to plotting multiple
  spectra with potentially mismatched units.


1.3.0 (2022-12-21)
==================

- Added EXES support (EXES Redux v3.0.0).
- Updated FORCAST pipeline to v2.7.0 to allow the use of measured
  water vapor values in calibration routines.
- Updated FIFI-LS pipeline to v2.7.1, including a bug fix to spectral
  maps rotated to align detector orientation.
- Updated HAWC pipeline to v3.2.0, including improved identification and
  cleaning for discrepant artifacts in scan maps, caused by detector
  level jumps.
- Updated the spectral viewer interface to better control spectra in
  multiple files, apertures, and orders.


1.2.8 (2022-10-25)
==================

- Calibration updates for FORCAST flight series OC9V and HAWC flight
  series OC9W.
- Expanded acceptable formats for reference line lists in the spectral
  viewer.


1.2.7 (2022-09-15)
==================

- Updated FORCAST pipeline to v2.6.0, including additional parameters to
  allow reduction in detector coordinates and a bug fix for water vapor
  optimization in spectroscopy calibration.
- Updated FIFI-LS pipeline to v2.7.0, including improved spatial calibration
  and astrometry fixes for the final spectral cube and an experimental
  scan reduction improvement for OTF data.
- Updated HAWC pipeline to v3.1.0, including a new parameter for the
  scan mapping steps, allowing reduction at alternate grid scales.
- Calibration data updates for FIFI-LS flight series OC9T.
- Added FIFI-LS support to the scan module.
- Added support for more general spectral formats, e.g. text files and simple
  FITS files, to the spectral viewer.


1.2.6 (2022-07-25)
==================

- Calibration data updates for HAWC flight series OC9Q-R.


1.2.5 (2022-06-10)
==================

- Calibration data updates for FORCAST flight series OC9P.
- Add pixel unit display to spectral viewer tool.


1.2.4 (2022-05-25)
==================

- Updated FORCAST pipeline to v2.5.0, including support for NXCAC slit scans.
- Updated FIFI-LS pipeline to v2.6.1, including performance improvements
  and additional memory management for large data sets.
- Calibration data updates for FORCAST and FIFI-LS.


1.2.3 (2022-04-06)
==================

- Updated FORCAST pipeline to v2.4.0, removing scikit-image as a dependency.
- Added a line list overplot feature to the spectral viewer tool.
- Improved log messages for the QAD image viewer tools.
- Completed test coverage and associated minor fixes for the scan module.


1.2.2 (2022-03-15)
==================

- Updated FORCAST and FIFI-LS calibration files.
- Increased test coverage and minor bug fixes for the scan module.


1.2.1 (2022-02-22)
==================

- Various build and test error fixes, including missing scan
  package configuration files.


1.2.0 (2022-02-18)
==================

- Added HAWC+ support (HAWC DRP v3.0.0).
- Updated FIFI-LS bad pixel and flat files.


1.1.1 (2021-12-13)
==================

- Updated FIFI-LS pipeline to v2.6.0, including simplified
  wavelength calibration format.
- Refactored toolkit algorithms for more generalized resampling
  and improved multiprocessing support.


1.1.0 (2021-09-27)
==================

- Added FLITECAM support (FLITECAM Redux v2.0.0) for all observation
  modes.


1.0.0 (2021-07-15)
==================

- Initial release, including FORCAST Redux v2.3.0 and FIFI-LS Redux v2.5.1.
