#  Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest
import logging
import copy
import uuid
import numpy as np
import astropy.io.fits as pf

from sofia_redux.visualization.models import high_model, mid_model, low_model
from sofia_redux.visualization.utils import eye_error


class TestHighModel(object):

    def test_init(self, grism_hdul):
        model = high_model.HighModel(grism_hdul)

        assert model.filename == grism_hdul.filename()
        assert model.id != grism_hdul.filename()
        assert isinstance(model.id, uuid.UUID)
        assert model.index == 0
        assert model.enabled

    def test_init_other_filenames(self, grism_hdul):
        hdu = pf.ImageHDU()
        hdul = pf.HDUList(hdu)
        model = high_model.HighModel(hdul)
        assert model.filename == 'UNKNOWN'

        hdul[0].header['FILENAME'] = 'TEST'
        model = high_model.HighModel(hdul)
        assert model.filename == 'TEST'

    def test_not_implemented(self, grism_hdul):
        model = high_model.HighModel(grism_hdul)

        bad_functions = {'load_data': {'f': model.load_data, 'args': None},
                         'retrieve': {'f': model.retrieve, 'args': None},
                         'valid_field': {'f': model.valid_field,
                                         'args': 'foo'}}

        for bad in bad_functions.values():
            with pytest.raises(NotImplementedError):
                if bad['args']:
                    bad['f'](bad['args'])
                else:
                    bad['f']()

    def test_copy(self, grism_hdul):
        model = high_model.Grism(grism_hdul)

        new_model = copy.copy(model)

        assert model.id == new_model.id
        assert model.filename == new_model.filename
        assert id(model) != id(new_model)

        old_mid_model = model.retrieve(order=0, level='low', field='wavepos')
        new_mid_model = new_model.retrieve(order=0, level='low',
                                           field='wavepos')
        assert id(old_mid_model) == id(new_mid_model)

        old_low_model = model.retrieve(order=0, level='raw', field='wavepos')
        new_low_model = new_model.retrieve(order=0, level='raw',
                                           field='wavepos')
        assert id(old_low_model) == id(new_low_model)
        assert np.mean(old_low_model) == np.mean(new_low_model)

    def test_deepcopy(self, grism_hdul):
        model = high_model.Grism(grism_hdul)

        new_model = copy.deepcopy(model)

        assert model.id == new_model.id
        assert model.filename == new_model.filename
        assert id(model) != id(new_model)

        old_mid_model = model.retrieve(order=0, level='low', field='wavepos')
        new_mid_model = new_model.retrieve(order=0, level='low',
                                           field='wavepos')
        assert id(old_mid_model) != id(new_mid_model)

        old_low_model = model.retrieve(order=0, level='raw', field='wavepos')
        new_low_model = new_model.retrieve(order=0, level='raw',
                                           field='wavepos')
        assert id(old_low_model) != id(new_low_model)
        assert np.mean(old_low_model) == np.mean(new_low_model)

        for old_mid, new_mid in zip(model.orders, new_model.orders):
            assert id(old_mid) != id(new_mid)
            for old_low, new_low in zip(old_mid.data.values(),
                                        new_mid.data.values()):
                assert id(new_low) != id(old_low)

    @pytest.mark.parametrize('extname,naxis1,naxis2,result',
                             [('spectral_flux', 100, 100, True),
                              ('flux', 100, 5, True),
                              ('flux', 0, 5, False),
                              ('flux', 100, 10, False)
                              ])
    def test_spectral_test(self, extname, naxis1, naxis2, result,
                           multiorder_hdul_spec):

        multiorder_hdul_spec[0].header['EXTNAME'] = extname
        multiorder_hdul_spec[0].header['NAXIS1'] = naxis1
        multiorder_hdul_spec[0].header['NAXIS2'] = naxis2

        model = high_model.HighModel(multiorder_hdul_spec)

        output = model.spectral_test()

        assert output is result

    @pytest.mark.parametrize('num_ord,num_aper,flag',
                             [(2, 1, 'disable'), (1, 2, 'enable'),
                              (1, 1, 'disable'), (0, 0, 'disable')])
    def test_enable_orders(self, mocker, caplog, num_ord, num_aper, flag,
                           multiorder_multiap_hdul):
        caplog.set_level(logging.DEBUG)
        model = high_model.MultiOrder(multiorder_multiap_hdul)
        model.num_orders = num_ord
        model.num_aperture = num_aper
        order = mocker.Mock(spec=mid_model.Order, number=2, aperture=1)
        model.orders = [order]

        model.enable_orders([1, 3], True)

        assert 'Enable [1, 3]' in caplog.text
        assert f'Setting Order 2, Aperture 1 to {flag}' in caplog.text

    @pytest.mark.parametrize('instrument,prodtype,result',
                             [(None, None, True),
                              ('flitecam', 'spectra', True),
                              ('forcast', 'combspec', True),
                              ('exes', 'spectra_1d', True),
                              ('exes', 'debounced', False),
                              ('general', 'debounced', True),
                              ('hawc', 'debounced', True)])
    def test_spectral_data_check(self, instrument, prodtype, result,
                                 grism_hdul):
        model = high_model.Grism(grism_hdul)
        model.hdul[0].header['INSTRUME'] = instrument
        model.hdul[0].header['PRODTYPE'] = prodtype

        if result:
            output = model.spectral_data_check()
            assert output is True
        else:
            with pytest.raises(eye_error.EyeError) as msg:
                model.spectral_data_check()
            assert 'do not contain spectral data' in str(msg)


class TestGrism(object):

    def test_init(self, grism_hdul):
        model = high_model.Grism(grism_hdul)
        assert model.default_ndims == 1
        assert model.default_field == 'spectral_flux'
        assert isinstance(model.books, list)
        assert isinstance(model.orders, list)

    @pytest.mark.parametrize(
        'spec_test,spec_only,img_only,gen_only,load_ord,load_book',
        [(False, False, False, False, False, False),
         (True, True, False, False, True, False),
         (True, False, True, False, False, True),
         (True, False, False, True, True, False),
         (True, False, False, False, True, True)])
    def test_load_data(self, mocker, grism_hdul, spec_test, spec_only,
                       img_only, gen_only, load_ord, load_book):
        model = high_model.Grism(grism_hdul)
        mocker.patch.object(high_model.HighModel, 'spectral_test',
                            return_value=spec_test)
        mocker.patch.object(high_model.Grism, '_spectra_only',
                            return_value=spec_only)
        mocker.patch.object(high_model.Grism, '_image_only',
                            return_value=img_only)
        mocker.patch.object(high_model.Grism, '_general_only',
                            return_value=gen_only)
        ord_mock = mocker.patch.object(high_model.Grism, '_load_order')
        book_mook = mocker.patch.object(high_model.Grism, '_load_book')

        if spec_test:
            model.load_data()
            assert ord_mock.called is load_ord
            assert book_mook.called is load_book
        else:
            with pytest.raises(eye_error.EyeError) as msg:
                model.load_data()
            assert 'No spectral data present' in str(msg)

    @pytest.mark.parametrize('spec_val,img_val,order_count,book_count',
                             [(True, False, 1, 0), (False, True, 0, 1),
                              (False, False, 1, 1)])
    def test_load_data_combined(self, grism_hdul, mocker, spec_val,
                                img_val, order_count, book_count):
        model = high_model.Grism(grism_hdul)

        order_mock = mocker.patch.object(high_model.Grism, '_load_order')
        book_mock = mocker.patch.object(high_model.Grism, '_load_book')
        mocker.patch.object(high_model.Grism, '_spectra_only',
                            return_value=spec_val)
        mocker.patch.object(high_model.Grism, '_image_only',
                            return_value=img_val)

        model.load_data()

        assert order_mock.call_count == order_count
        assert book_mock.call_count == book_count

    @pytest.mark.parametrize('filename,result',
                             [('CLN', True), ('DRP', True), ('LNZ', True),
                              ('STK', True), ('LOC', True), ('TRC', True),
                              ('APS', True), ('BGS', True), ('CAL', False)])
    def test_image_only(self, grism_hdul, filename, result):
        model = high_model.Grism(grism_hdul)
        model.filename = f'grism_{filename}_100.fits'

        out = model._image_only()

        assert out is result

    @pytest.mark.parametrize('filename,result',
                             [('CMB', True), ('MRG', True), ('SPC', True),
                              ('CAL', True), ('RSP', True), ('IRS', True),
                              ('CLN', False), ('BGS', False), ('COA', False)])
    def test_spectra_only(self, grism_hdul, filename, result):
        model = high_model.Grism(grism_hdul)
        model.filename = f'grism_{filename}_100.fits'

        out = model._spectra_only()

        assert out is result

    @pytest.mark.parametrize('filename,result',
                             [('csv', True), ('dat', True), ('fits', False)])
    def test_general_only(self, grism_hdul, filename, result):
        model = high_model.Grism(grism_hdul)
        model.filename = f'grism_CAL_100.{filename}'
        out = model._general_only()

        assert out is result

    @pytest.mark.parametrize('instrument,result',
                             [('General', True), ('FORCAST', False)])
    def test_general_only_2(self, grism_hdul, instrument, result):
        model = high_model.Grism(grism_hdul)
        model.filename = 'grism_CAL_100.fits'
        model.hdul[0].header['instrume'] = f'{instrument}'
        out = model._general_only()
        assert out is result

    def test_load_order(self, grism_hdul):
        model = high_model.Grism(grism_hdul)
        model.orders = list()

        model._load_order()

        assert len(model.orders) == 1

    def test_load_book(self, grism_hdul):
        model = high_model.Grism(grism_hdul)
        model.books = list()

        model._load_book()

        assert len(model.books) == 1

    def test_retrieve(self, grism_hdul):
        model = high_model.Grism(grism_hdul)

        value = model.retrieve(book=True, level='high')
        assert isinstance(value, mid_model.Book)

        # value = model.retrieve(book=True, level='low')
        # assert isinstance(value, mid_model.Book)

        # value = model.retrieve(book=True, level='raw')
        # assert isinstance(value, mid_model.Book)

        value = model.retrieve(order=0, level='high')
        assert isinstance(value, mid_model.Order)

        value = model.retrieve(order=0, level='low', field='spectral_flux')
        assert isinstance(value, low_model.Spectrum)

        value = model.retrieve(order=0, level='raw', field='spectral_flux')
        assert isinstance(value, np.ndarray)

        value = model.retrieve(order='0.0', level='raw', field='spectral_flux')
        assert isinstance(value, np.ndarray)

        value = model.retrieve(order='0', level='raw', field='spectral_flux',
                               aperture='a')
        assert isinstance(value, np.ndarray)

    @pytest.mark.parametrize('order,book', [(True, None), (None, True)])
    def test_retrieve_empty(self, grism_hdul, order, book):
        model = high_model.Grism(grism_hdul)
        model.books.clear()
        model.orders.clear()

        value = model.retrieve(order=order, book=book)
        assert value is None

    def test_retrieve_fail(self, grism_hdul):
        model = high_model.Grism(grism_hdul)

        with pytest.raises(RuntimeError) as msg:
            model.retrieve(book=True, order=True)
        assert 'Invalid identifier' in str(msg)

        with pytest.raises(RuntimeError) as msg:
            model.retrieve(book=True, level='mid')
        assert 'Invalid level' in str(msg)

    @pytest.mark.parametrize('field,result', [('spectral_flux', True),
                                              ('transmission', True),
                                              ('polarization', False)])
    def test_valid_field(self, field, result, grism_hdul, caplog):
        caplog.set_level(logging.DEBUG)
        model = high_model.Grism(grism_hdul)

        check = model.valid_field(field)
        if result:
            assert check
            assert 'is valid' in caplog.text
        else:
            assert not check
            assert 'is not valid' in caplog.text

    def test_enable_orders(self, grism_hdul):
        model = high_model.Grism(grism_hdul)
        target_orders = list(range(len(model.orders)))
        for order in model.orders:
            order.enabled = False

        model.enable_orders(target_orders, True)

        assert all([o.enabled for o in model.orders])

    def test_list_enabled(self, grism_hdul):
        model = high_model.Grism(grism_hdul)

        enabled = model.list_enabled()

        assert len(enabled['orders']) == 1
        assert len(enabled['books']) == 1

    def test_multi_aperture_split(self, multi_ap_grism_hdul):
        model = high_model.Grism(multi_ap_grism_hdul)
        assert model.num_orders == 1
        assert model.num_aperture == 2
        assert isinstance(model.orders, list)

        for order in range(2):
            value = model.retrieve(order=order, level='high')
            assert isinstance(value, mid_model.Order)

            value = model.retrieve(order=order, level='low',
                                   field='spectral_flux')
            assert isinstance(value, low_model.Spectrum)

    def test_multi_aperture_combined(self, multiorder_hdul_spec):
        model = high_model.Grism(multiorder_hdul_spec)
        assert model.num_orders == 1
        assert model.num_aperture == 10
        assert isinstance(model.orders, list)
        for order in range(10):
            value = model.retrieve(order=order, level='high')
            assert isinstance(value, mid_model.Order)

            value = model.retrieve(order=order, level='low',
                                   field='spectral_flux')
            assert isinstance(value, low_model.Spectrum)

    def test_mult_ap_multi_order(self, multiorder_multiap_hdul):
        model = high_model.MultiOrder(multiorder_multiap_hdul)
        assert model.num_orders == 5
        assert model.num_aperture == 3
        assert len(model.orders) == 15
        assert all([len(o.name.split('.')) == 2 for o in model.orders])


class TestMultiOrder(object):

    def test_init_merged(self, multiorder_hdul_merged, tmp_path):
        filename = str(tmp_path / 'multiorder_merged.fits')
        multiorder_hdul_merged.writeto(filename, overwrite=True)
        model = high_model.MultiOrder(multiorder_hdul_merged)
        assert model.default_ndims == 1
        assert isinstance(model.orders, list)
        assert len(model.orders) == 1
        assert len(model.orders[0].data) > 0

    def test_init_spec(self, multiorder_hdul_spec):
        model = high_model.MultiOrder(multiorder_hdul_spec)
        assert model.default_ndims == 1
        assert isinstance(model.orders, list)

    def test_load_data(self, multiorder_hdul_spec, caplog):
        caplog.set_level(logging.DEBUG)
        model = high_model.MultiOrder(multiorder_hdul_spec)

        model.orders.clear()
        model.num_orders = 0

        model.load_data()

        norders = multiorder_hdul_spec[0].header['norders']
        naps = multiorder_hdul_spec[0].header['naps']
        assert model.num_orders == norders
        assert f'Loading {norders} orders and {naps} apertures' in caplog.text
        assert len(model.orders) == norders
        assert all([isinstance(o, mid_model.Order) for o in model.orders])

    def test_load_data_general(self, general_hdul, mocker):
        mocker.patch.object(high_model.MultiOrder,
                            '_determine_aperture_count',
                            return_value=1)
        book_mock = mocker.patch.object(mid_model, 'Book')

        model = high_model.MultiOrder(general_hdul, general=True)
        assert model.num_orders == 1
        assert model.num_aperture == 1
        assert book_mock.call_count == 0

        general_hdul[0].header['PRODTYPE'] = 'UNKNOWN'
        model = high_model.MultiOrder(general_hdul, general=True)
        model.load_data(general=True)
        assert book_mock.call_count == 2

    def test_load_data_split(self, multiorder_hdul_spec, mocker,
                             split_order_hdul):
        order_mock = mocker.patch.object(mid_model, 'Order')
        book_mock = mocker.patch.object(mid_model, 'Book')

        mocker.patch.object(high_model.MultiOrder, '_determine_aperture_count',
                            return_value=1)
        multiorder_hdul_spec[0].header['NORDERS'] = 1

        high_model.MultiOrder(multiorder_hdul_spec)
        assert order_mock.call_count == 1
        assert book_mock.call_count == 1

        mocker.patch.object(high_model.MultiOrder,
                            '_determine_aperture_count',
                            return_value=2)
        multiorder_hdul_spec[0].header['NORDERS'] = 3
        order_mock.reset_mock()
        book_mock.reset_mock()
        with pytest.raises(eye_error.EyeError) as msg:
            high_model.MultiOrder(multiorder_hdul_spec)
        assert 'No spectral data found in HDUL' in str(msg)

    def test_load_data_split_2(self, mocker, split_order_hdul):
        order_mock = mocker.patch.object(mid_model, 'Order')
        book_mock = mocker.patch.object(mid_model, 'Book')

        mocker.patch.object(high_model.MultiOrder,
                            '_determine_aperture_count',
                            return_value=1)
        split_order_hdul[0].header['NORDERS'] = 1
        high_model.MultiOrder(split_order_hdul)
        assert order_mock.call_count == 1
        assert book_mock.call_count == 1

        order_mock.reset_mock()
        book_mock.reset_mock()
        mocker.patch.object(high_model.MultiOrder, '_determine_aperture_count',
                            return_value=3)
        split_order_hdul[0].header['NORDERS'] = 2
        high_model.MultiOrder(split_order_hdul)
        assert order_mock.call_count == 6
        assert book_mock.call_count == 6

        order_mock.reset_mock()
        book_mock.reset_mock()
        assert order_mock.call_count == 0
        assert book_mock.call_count == 0
        mocker.patch.object(high_model.MultiOrder, '_determine_aperture_count',
                            return_value=1)
        split_order_hdul[0].header['NORDERS'] = 2
        high_model.MultiOrder(split_order_hdul)
        assert order_mock.call_count == 2
        assert book_mock.call_count == 2

    @pytest.mark.parametrize('naps,app,ncol,general,extension,result',
                             [(3, None, 2, False, 'Primary', 3),
                              (None, None, 2, True, 'Primary', 2),
                              (None, None, 1, False,
                               'SPECTRAL_FLUX_ORDER_01', 1),
                              (None, None, 1, False, 'SPECTRAL_FLUX', 1),
                              (None, None, 2, True, 'SPECTRAL_FLUX', 2),
                              (None, None, 2, False, 'SPECTRAL_FLUX', 2),
                              (None, None, 2, False, 'Other', 1),
                              (None, '2,3', 1, False, 'Other', 2)])
    def test_determine_aperture_count(self, caplog, naps, app, ncol,
                                      general, extension, result,
                                      multiorder_hdul_spec):
        caplog.set_level(logging.DEBUG)
        data = np.zeros((ncol, 100))
        header = pf.header.Header()
        if naps:
            header['NAPS'] = naps
        if app:
            header['APPOSO01'] = app

        hdu = pf.PrimaryHDU(data=data, header=header)
        hdu_2 = pf.ImageHDU(data=data, header=header, name=extension)
        hdul = pf.HDUList([hdu, hdu_2])

        model = high_model.MultiOrder(multiorder_hdul_spec)
        model.hdul = hdul

        count = model._determine_aperture_count(general)
        assert count == result

    def test_retrieve(self, multiorder_hdul_spec):
        model = high_model.MultiOrder(multiorder_hdul_spec)

        value = model.retrieve(level='high')
        assert isinstance(value, mid_model.Order)
        assert value.name == 'Order_1'

        value = model.retrieve(level='low', field='spectral_flux')
        assert isinstance(value, low_model.Spectrum)
        assert value.name == 'spectral_flux'

        value = model.retrieve(level='high', field='spectral_flux',
                               order='0', aperture='a')
        assert isinstance(value, mid_model.Order)
        assert value.aperture == 0

    def test_retrieve_fail(self, multiorder_hdul_spec, caplog):
        model = high_model.MultiOrder(multiorder_hdul_spec)

        with pytest.raises(TypeError) as msg:
            model.retrieve(order='one', level='high')
        assert 'must be a number' in str(msg)

        caplog.set_level(logging.DEBUG)
        assert 'Need to provide field' not in caplog.text
        result = model.retrieve(level='low')
        assert result is None
        assert 'Need to provide field' in caplog.text

        model.orders = list()
        result = model.retrieve(level='low', field='spectral_flux')
        assert result is None

    def test_enable_orders(self, multiorder_hdul_spec, caplog):
        caplog.set_level(logging.DEBUG)
        model = high_model.MultiOrder(multiorder_hdul_spec)

        on_flag = [1, 2, 3]
        off_flag = [4, 5, 6, 7, 8, 9]

        model.enable_orders(on_flag)

        assert all([o.enabled if i in on_flag else not o.enabled
                    for i, o in enumerate(model.orders)])
        for flag in on_flag:
            assert f'Order {flag}, Aperture {0} to enable' in caplog.text
        for flag in off_flag:
            assert f'Order {flag}, Aperture {0} to disable' in caplog.text

    def test_list_enabled(self, multiorder_hdul_spec, caplog):
        caplog.set_level(logging.DEBUG)
        model = high_model.MultiOrder(multiorder_hdul_spec)

        enabled = model.list_enabled()
        assert len(enabled['books']) == 0
        assert len(enabled['orders']) == 10
        assert 'Current enabled fields' in caplog.text

    @pytest.mark.parametrize('field,result', [('spectral_flux', True),
                                              ('spectral_error', True),
                                              ('flux', False),
                                              ('transmission', True),
                                              ('wavepos', True)])
    def test_valid_field(self, multiorder_hdul_spec, caplog,
                         field, result):
        caplog.set_level(logging.DEBUG)
        model = high_model.MultiOrder(multiorder_hdul_spec)

        value = model.valid_field(field)
        assert value is result
        assert 'Valid field check for' in caplog.text
