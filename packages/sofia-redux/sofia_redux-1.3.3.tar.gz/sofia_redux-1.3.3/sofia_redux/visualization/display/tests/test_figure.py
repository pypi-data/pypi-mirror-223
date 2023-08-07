#  Licensed under a 3-clause BSD style license - see LICENSE.rst

import logging
from astropy import units as u
from matplotlib import figure as mpf
from matplotlib import gridspec
from matplotlib import backend_bases as mpb
import pytest
import pytestqt.exceptions as pe

from sofia_redux.visualization.display import figure, gallery, blitting, pane
from sofia_redux.visualization.models import high_model, reference_model
from sofia_redux.visualization import signals
from sofia_redux.visualization.utils import eye_error

PyQt5 = pytest.importorskip('PyQt5')


class TestFigure(object):

    def test_init(self, fig_widget, qtbot):
        sigs = signals.Signals()

        correct_flags = {'gs': None, 'block_current_pane_signal': False,
                         'highlight_pane': True, 'show_markers': False,
                         'show_grid': False, 'show_error': True,
                         'dark_mode': False, '_cursor_mode': None,
                         '_cursor_pane': None}
        correct_types = {'fig': mpf.Figure, 'gallery': gallery.Gallery,
                         'blitter': blitting.BlitManager, 'panes': list,
                         '_cursor_locations': list, '_fit_params': list,
                         '_current_pane': list}
        correct_values = {'layout': 'grid',
                          'color_cycle': 'Accessible', 'plot_type': 'Step'}

        obj = figure.Figure(figure_widget=fig_widget, signals=sigs)

        assert isinstance(obj, figure.Figure)
        assert obj.signals == sigs
        assert obj.widget == fig_widget

        for field, flag in correct_flags.items():
            assert getattr(obj, field) is flag
        for field, value in correct_types.items():
            assert isinstance(getattr(obj, field), value)
        for field, value in correct_values.items():
            assert getattr(obj, field) == value

    @pytest.mark.parametrize('state', [True, False, None])
    def test_set_pane_highlight_flag(self, blank_figure, mocker, state, qtbot):

        art_mock = mocker.patch.object(gallery.Gallery,
                                       'set_pane_highlight_flag')
        blank_figure.set_pane_highlight_flag(state)

        assert blank_figure.highlight_pane is state
        assert art_mock.called_with({'state': state})

    @pytest.mark.parametrize('value', [True, False, None])
    def test_set_block_current_pane_signal(self, blank_figure, value):
        blank_figure.set_block_current_pane_signal(value)
        assert blank_figure.block_current_pane_signal is value

        blank_figure.set_block_current_pane_signal()
        assert blank_figure.block_current_pane_signal is True

    @pytest.mark.parametrize('value', ['grid', 'columns'])
    def test_set_layout_style(self, blank_figure, value):
        blank_figure.set_layout_style(value)
        assert blank_figure.layout == value

        blank_figure.set_layout_style()
        assert blank_figure.layout == 'grid'

    def test_populated(self, blank_figure):
        value = blank_figure.populated()
        assert not value

        panes = ['one', 'two', 'three']
        blank_figure.panes = panes
        value = blank_figure.populated()
        assert value

    def test_current_pane_setting(self, blank_figure, qtbot, mocker):
        value = 5
        with qtbot.wait_signal(blank_figure.signals.current_pane_changed):
            blank_figure.current_pane = value
        assert blank_figure.current_pane == list()

        mocker.patch.object(blank_figure, 'valid_pane', return_value=True)
        with qtbot.wait_signal(blank_figure.signals.current_pane_changed):
            blank_figure.current_pane = value
        assert blank_figure.current_pane == [value]

    def test_pane_count(self, blank_figure):
        length = 4
        blank_figure.panes = ['a'] * length

        assert blank_figure.pane_count() == length

    def test_pane_layout(self, blank_figure):
        gs = blank_figure.pane_layout()
        assert gs is None

        shape = (2, 3)
        blank_figure.gs = gridspec.GridSpec(shape[0], shape[1],
                                            figure=blank_figure.fig)
        gs = blank_figure.pane_layout()
        assert gs == shape

    def test_add_panes_two_dim(self, blank_figure, mocker):
        methods = ['set_plot_type', 'set_markers', 'set_grid',
                   'set_error', 'create_artists_from_current_models']
        for method in methods:
            mocker.patch.object(pane.TwoDimPane, method)
        assert len(blank_figure.panes) == 0
        n_panes = 2
        blank_figure.add_panes(n_dims=2, n_panes=n_panes)
        assert len(blank_figure.panes) == n_panes
        assert all([isinstance(p, pane.TwoDimPane)
                    for p in blank_figure.panes])

    def test_add_panes_failures(self, blank_figure):
        count = blank_figure.pane_count()

        blank_figure.add_panes(None, 0)
        new_count = blank_figure.pane_count()

        assert new_count == count

        with pytest.raises(RuntimeError) as e:
            blank_figure.add_panes([1, 1, 1], 1)
        assert 'Length of pane dimensions' in str(e)

        with pytest.raises(RuntimeError) as e:
            blank_figure.add_panes([3, 1, 1], 3)
        assert 'Invalid number of dimensions' in str(e)

    def test_remove_artists(self, blank_figure, mocker):
        mock = mocker.patch.object(gallery.Gallery,
                                   'reset_artists')

        blank_figure.remove_artists()

        assert mock.called_with({'selection': 'all'})

    def test_reset_artists_fail(self, blank_figure, mocker, caplog):
        sigs = signals.Signals()
        caplog.set_level(logging.DEBUG)
        mocker.patch.object(pane.OneDimPane,
                            'create_artists_from_current_models',
                            return_value=[1, 2])
        mocker.patch.object(gallery.Gallery, 'add_drawings',
                            return_value=0)
        mocker.patch.object(figure.Figure, '_add_pane_artists')

        blank_figure.panes = [pane.OneDimPane(sigs)]

        blank_figure.reset_artists()

        assert 'Error encountered while creating artists' in caplog.text

    def test_add_pane_artists(self, blank_figure, mocker):
        sigs = signals.Signals()
        add_mock = mocker.patch.object(gallery.Gallery, 'add_patches')
        blank_figure.panes = [pane.OneDimPane(sigs)]
        blank_figure._current_pane = list()
        expected = {'pane_0': {'kind': 'border',
                               'artist': None,
                               'visible': True}}

        # test show, no current: visible
        blank_figure.highlight_pane = True
        blank_figure._add_pane_artists()
        assert add_mock.called_with(expected)

        # test show, None current: visible
        blank_figure._current_pane = None
        blank_figure._add_pane_artists()
        assert add_mock.called_with(expected)

        # test show, current matches: visible
        blank_figure._current_pane = [0]
        blank_figure._add_pane_artists()
        assert add_mock.called_with(expected)

        # test show, current does not match: not visible
        expected['pane_0']['visible'] = False
        blank_figure._current_pane = [1]
        blank_figure._add_pane_artists()
        assert add_mock.called_with(expected)

        # test no show, current does match: not visible
        blank_figure.highlight_pane = False
        blank_figure._current_pane = [0]
        blank_figure._add_pane_artists()
        assert add_mock.called_with(expected)

        # test no show, current does not match: not visible
        blank_figure._current_pane = [1]
        blank_figure._add_pane_artists()
        assert add_mock.called_with(expected)

    def test_add_crosshair(self, blank_figure, mocker):

        m1 = mocker.patch.object(blank_figure.gallery, 'add_crosshairs')

        # no lines added for no panes
        expected = list()
        blank_figure._add_crosshair()
        m1.assert_called_with(expected)

        # 1 pane => 2 lines added
        blank_figure.add_panes(n_dims=0, n_panes=1)
        blank_figure._add_crosshair()
        assert len(m1.call_args[0][0]) == 2

    def test_pane_details(self, blank_figure):
        expected = dict()
        assert blank_figure.pane_details() == expected

        blank_figure.add_panes(1, 2)
        expected = {'pane_0': {}, 'pane_1': {}}
        assert blank_figure.pane_details() == expected

    def test_change_current_pane(self, blank_figure):
        blank_figure.panes = [0, 1, 2, 3, 4, 5]
        blank_figure.current_pane = [0]
        assert not blank_figure.change_current_pane([0])
        assert blank_figure.current_pane == [0]

        assert blank_figure.change_current_pane(list())
        assert blank_figure.current_pane == list()

        blank_figure.current_pane = [0, 1, 2, 3]
        assert blank_figure.change_current_pane([1, 2])
        assert blank_figure.current_pane == [1, 2]

        assert not blank_figure.change_current_pane([6])
        assert blank_figure.current_pane == [1, 2]

    def test_determine_selected_pane(self, blank_figure):
        n_panes = 3
        fig = mpf.Figure()
        axes = fig.subplots(1, n_panes)
        sigs = signals.Signals()
        blank_figure.panes = [pane.OneDimPane(sigs, ax) for ax in axes]

        for i, ax in enumerate(axes):
            found = blank_figure.determine_selected_pane(ax)
            assert found == [i]

        found = blank_figure.determine_selected_pane(all_ax=True)
        assert found == [0, 1, 2]

        ax = fig.add_subplot()
        found = blank_figure.determine_selected_pane(ax)
        assert isinstance(found, list) and len(found) == 0

    def test_determine_pane_from_model(self, blank_figure, mocker):
        sigs = signals.Signals()

        count = 3
        blank_figure.panes = [pane.OneDimPane(sigs) for _ in range(count)]

        mocker.patch.object(pane.OneDimPane, 'contains_model',
                            return_value=True)
        matching = blank_figure.determine_pane_from_model('test')
        assert len(matching) == count
        assert isinstance(matching[0][1], pane.OneDimPane)

    def test_get_current_pane(self, blank_figure):
        assert blank_figure.get_current_pane() is None

        blank_figure.panes = ['a', 'b', 'c', 'd', 'e']
        blank_figure.current_pane = [2, 3]
        assert blank_figure.get_current_pane() == ['c', 'd']

        blank_figure.panes = ['a', 'b', 'c', 'd', 'e']
        blank_figure.current_pane = None
        assert blank_figure.get_current_pane() == list()

    def test_assign_models_split(self, grism_hdul, blank_figure):
        blank_figure.add_panes(n_dims=1, n_panes=2)
        model_1 = high_model.Grism(grism_hdul)
        model_2 = high_model.Grism(grism_hdul)
        models = {model_1.id: model_1, model_2.id: model_2}

        blank_figure.assign_models('split', models)

        assert all([len(p.models) == 1 for p in blank_figure.panes])

    def test_assign_models_bad(self, blank_figure):
        models = dict()
        with pytest.raises(RuntimeError) as msg:
            blank_figure.assign_models(mode='default', models=models)

        assert 'Invalid mode' in str(msg)

    @pytest.mark.parametrize('mode', ['split', 'first', 'last', 'assigned'])
    def test_assign_models_errors(self, mode, blank_figure, mocker,
                                  grism_hdul):
        mocker.patch.object(blank_figure, 'add_model_to_pane',
                            side_effect=eye_error.EyeError)

        blank_figure.add_panes(n_dims=1, n_panes=2)
        model_1 = high_model.Grism(grism_hdul)
        model_2 = high_model.Grism(grism_hdul)
        models = {model_1.id: model_1, model_2.id: model_2}
        indicies = [0, 1]

        result = blank_figure.assign_models(mode, models, indicies)
        assert result == 2

    @pytest.mark.parametrize('layout,shape', [('rows', (3, 1)),
                                              ('columns', (1, 3)),
                                              ('grid', (2, 2))])
    def test_add_model_to_pane_different(self, blank_figure, mocker,
                                         caplog, grism_hdul, layout, shape):
        caplog.set_level(logging.DEBUG)
        mocker.patch.object(figure.Figure, 'model_matches_pane',
                            return_value=False)

        blank_figure.set_layout_style(layout)

        model = high_model.Grism(grism_hdul)
        blank_figure.add_panes(n_dims=1, n_panes=1)
        assert blank_figure.pane_count() == 1

        blank_figure.add_model_to_pane(model)
        assert blank_figure.pane_count() == 2

        assert 'Added model to panes' in caplog.text

        blank_figure.add_panes(n_dims=0, n_panes=1)
        assert blank_figure.pane_count() == 3
        assert blank_figure.pane_layout() == shape

        # setting overplot state should reassign axes
        blank_figure.set_overplot_state(True, 'all')
        assert blank_figure.pane_count() == 3
        for pane_ in blank_figure.panes:
            assert pane_.show_overplot

    @pytest.mark.parametrize('matches', [True, False])
    def test_add_model_to_pane_bad(self, blank_figure, mocker, grism_hdul,
                                   caplog, matches):
        caplog.set_level(logging.INFO)
        mocker.patch.object(pane.OneDimPane, 'add_model',
                            side_effect=eye_error.EyeError)
        mocker.patch.object(figure.Figure, 'model_matches_pane',
                            return_value=matches)
        remove_mock = mocker.patch.object(pane.OneDimPane, 'remove_model')

        with pytest.raises(eye_error.EyeError):
            blank_figure.add_model_to_pane(high_model.Grism(grism_hdul))

        assert 'Added model to panes' not in caplog.text
        assert remove_mock.called_once

    def test_remove_model_from_pane(self, blank_figure, mocker):

        remove = mocker.patch.object(pane.OneDimPane, 'remove_model')
        sigs = signals.Signals()
        with pytest.raises(RuntimeError) as msg:
            blank_figure.remove_model_from_pane()
        assert 'Must specify which model' in str(msg)

        count = 4
        panes = [pane.OneDimPane(sigs) for i in range(count)]
        blank_figure.panes = panes

        blank_figure.remove_model_from_pane(filename='test',
                                            panes=panes[0])
        assert remove.call_count == 1

        # good call with int
        blank_figure.remove_model_from_pane(model_id='test',
                                            panes=0)
        assert remove.call_count == 2

        # good call with None
        blank_figure.remove_model_from_pane(model_id='test',
                                            panes=None)
        assert remove.call_count == 6

        # bad call with int
        blank_figure.remove_model_from_pane(filename='test',
                                            panes=42)
        assert remove.call_count == 6

        # bad call with non-int
        blank_figure.remove_model_from_pane(filename='test',
                                            panes='bad')
        assert remove.call_count == 6

        mock = mocker.patch.object(figure.Figure, 'end_cursor_records')
        blank_figure.recording = False
        blank_figure.remove_model_from_pane(filename='test',
                                            panes=panes[0])
        assert mock.call_count == 0

        blank_figure.recording = True
        blank_figure.remove_model_from_pane(filename='test',
                                            panes=panes[0])
        assert mock.call_count == 1

    def test_remove_all_panes(self, blank_figure):
        count = 4
        sigs = signals.Signals()
        panes = [pane.OneDimPane(sigs) for i in range(count)]
        blank_figure.panes = panes

        blank_figure.remove_all_panes()
        assert blank_figure.pane_count() == 0

        blank_figure.add_panes(0, 1)
        assert blank_figure.pane_count() == 1

    @pytest.mark.parametrize('flags, pane_count, ax_val',
                             [(None, 1, ''),
                              ('all', 4, ''),
                              ([1, 3], 2, ''),
                              ({'pane': 'all'}, 4, ''),
                              ({'pane': 'all', 'axis': 'test'}, 4, 'test'),
                              ({'pane': 'current'}, 1, ''),
                              ({'pane': 'current', 'axis': 'alt'}, 1, 'alt')])
    def test_parse_pane_flag(self, blank_figure, flags, pane_count, ax_val):
        # set a list of 4 panes
        sigs = signals.Signals()
        blank_figure.panes = [pane.OneDimPane(sigs) for _ in range(4)]
        blank_figure.current_pane = [0]

        panes, axis = blank_figure.parse_pane_flag(flags)
        assert len(panes) == pane_count
        assert axis == ax_val

        panes, axis = blank_figure.parse_pane_flag([blank_figure.panes[0]])
        assert len(panes) == 1
        assert panes[0] is blank_figure.panes[0]

        panes, axis = blank_figure.parse_pane_flag(
            {'pane': [blank_figure.panes[1]]})
        assert len(panes) == 1
        assert panes[0] is blank_figure.panes[1]

    def test_parse_pane_flag_fail(self, blank_figure, capsys):
        panes = [2.5, 'bad']
        with pytest.raises(TypeError) as msg:
            blank_figure.parse_pane_flag(panes)
        assert 'only contain integers or Pane' in str(msg)

        panes = {'bad_key': 'bad'}
        with pytest.raises(eye_error.EyeError) as msg:
            blank_figure.parse_pane_flag(panes)
        assert 'Unable to parse pane flag' in str(msg)

        panes = {'pane': 'bad'}
        with pytest.raises(eye_error.EyeError) as msg:
            blank_figure.parse_pane_flag(panes)
        assert 'Unable to parse pane flag' in str(msg)
        capsys.readouterr()

        blank_figure.parse_pane_flag(4)
        assert 'Invalid index' in capsys.readouterr().out

        blank_figure.parse_pane_flag({'pane': [4]})
        assert 'Invalid pane flag: 4' in capsys.readouterr().out

        blank_figure.parse_pane_flag({'pane': ['a']})
        assert 'Invalid pane flag: a' in capsys.readouterr().out

    def test_set_enabled(self, blank_figure, mocker, qtbot):
        model_mock = mocker.patch.object(pane.OneDimPane,
                                         'set_model_enabled')
        art_mock = mocker.patch.object(gallery.Gallery,
                                       'update_artist_options')
        vis_mock = mocker.patch.object(pane.OneDimPane,
                                       'update_visibility')
        pid = 0
        mid = 1
        state = True
        sigs = signals.Signals()

        blank_figure.panes = [pane.OneDimPane(sigs), pane.OneDimPane(sigs)]
        with qtbot.wait_signal(blank_figure.signals.atrophy):
            blank_figure.set_enabled(pid, mid, state)

        assert model_mock.called_with({'model_id': mid, 'state': state})
        assert art_mock.called_with({'pane': pid})
        assert vis_mock.called_once()

    def test_set_all_enabled(self, blank_figure, mocker, qtbot):
        model_mock = mocker.patch.object(pane.OneDimPane,
                                         'set_all_models_enabled')
        art_mock = mocker.patch.object(gallery.Gallery,
                                       'update_artist_options')
        vis_mock = mocker.patch.object(pane.OneDimPane,
                                       'update_visibility')
        pid = 0
        state = True
        sigs = signals.Signals()

        blank_figure.panes = [pane.OneDimPane(sigs), pane.OneDimPane(sigs)]
        with qtbot.wait_signal(blank_figure.signals.atrophy):
            blank_figure.set_all_enabled(pid, state)

        assert model_mock.called_with({'state': state})
        assert art_mock.called_with({'pane': pid})
        assert vis_mock.called_once()

    def test_get_markers(self, blank_figure, grism_hdul):
        model = high_model.Grism(grism_hdul)
        blank_figure.add_model_to_pane(model)

        assert blank_figure.get_markers(model.id, 0) == ['x']

    def test_get_colors(self, blank_figure, grism_hdul):
        model = high_model.Grism(grism_hdul)
        blank_figure.add_model_to_pane(model)

        colors = blank_figure.get_colors(model.id, 0)
        assert len(colors) == 1
        assert isinstance(colors[0], list)
        assert len(colors[0]) == 1
        assert isinstance(colors[0][0], str)

    @pytest.mark.parametrize('panes_list', [[0, 1, 2], 0, [0], []])
    def test_crosshair(self, blank_figure, mocker, qtbot, panes_list):
        direction = 'v'
        mocker.patch.object(figure.Figure, 'determine_selected_pane',
                            return_value=panes_list)
        art_mock = mocker.patch.object(gallery.Gallery, 'update_crosshair')
        cross_mock = mocker.patch.object(figure.Figure,
                                         '_parse_cursor_direction',
                                         return_value=direction)
        sigs = signals.Signals()

        blank_figure.panes = [pane.OneDimPane(sigs)]
        blank_figure._cursor_pane = [0]
        event = mpb.MouseEvent(x=2, y=3, canvas=blank_figure.widget.canvas,
                               name='motion_notify_event')
        event.xdata = 2
        event.ydata = 3

        if isinstance(panes_list, list) and len(panes_list) == 0:
            blank_figure.crosshair(event)
            assert art_mock.call_count == 0
            assert cross_mock.call_count == 0
        else:
            with qtbot.wait_signal(blank_figure.signals.atrophy):
                blank_figure.crosshair(event)

            assert art_mock.called_with({'data_point': (2, 3),
                                         'direction': direction})
            assert cross_mock.called_with({'mode': 'crosshair'})

    def test_reset_data_points_empty(self, blank_figure, mocker):
        mock = mocker.patch.object(gallery.Gallery, 'hide_cursor_markers')

        blank_figure.reset_data_points()

        assert mock.call_count == 0

    def test_reset_zoom_empty(self, blank_figure, mocker, qtbot):
        with pytest.raises(pe.TimeoutError):
            with qtbot.wait_signal(blank_figure.signals.atrophy_bg_partial):
                blank_figure.reset_zoom()
        sigs = signals.Signals()

        n_panes = 4
        blank_figure.panes = [pane.OneDimPane(sigs) for i in range(n_panes)]
        blank_figure.current_pane = [0]
        zoom_mock = mocker.patch.object(pane.OneDimPane, 'reset_zoom')
        with qtbot.wait_signal(blank_figure.signals.atrophy_bg_partial):
            blank_figure.reset_zoom(all_panes=True)

        assert zoom_mock.call_count == n_panes

        # test without all panes - should call once more
        with qtbot.wait_signal(blank_figure.signals.atrophy_bg_partial):
            blank_figure.reset_zoom(all_panes=False)
        assert zoom_mock.call_count == n_panes + 1

    @pytest.mark.parametrize('cursor,result',
                             [('fit', 'v'), ('y_zoom', 'h'), ('other', 'hv')])
    def test_parse_cursor_direction_crosshair(self, blank_figure, cursor,
                                              result):
        blank_figure._cursor_mode = cursor
        direction = blank_figure._parse_cursor_direction('crosshair')

        assert direction == result

    def test_clear_lines_all(self, blank_figure, mocker):
        reset_mock = mocker.patch.object(gallery.Gallery,
                                         'reset_artists')
        sigs = signals.Signals()
        panes = [pane.OneDimPane(sigs) for i in range(3)]
        blank_figure.panes = panes

        blank_figure.clear_lines(flags='v', all_panes=True)
        assert reset_mock.called_with({'panes': panes})
        assert reset_mock.call_count == 1

        blank_figure.clear_lines(flags='v', all_panes=False)
        assert reset_mock.called_with({'panes': [panes[0]]})
        assert reset_mock.call_count == 2

    def test_add_remove_pane(self, blank_figure, qtbot):
        blank_figure.add_panes(1, 3)
        assert blank_figure.current_pane is not None
        assert len(blank_figure.current_pane) == 1

        # remove first
        blank_figure.remove_pane([0])
        assert len(blank_figure.current_pane) == 1

        # remove last
        blank_figure.remove_pane([2])
        assert len(blank_figure.current_pane) == 1

        # remove none
        blank_figure.remove_pane(None)
        assert len(blank_figure.current_pane) == 1

        # remove final
        blank_figure.remove_pane([0])
        assert len(blank_figure.current_pane) == 0

    def test_change_axis_field(self, blank_figure, mocker):
        set_mock = mocker.patch.object(pane.OneDimPane, 'set_fields')
        fields = {'x': 'wavepos', 'y': 'spectral_flux'}
        f1 = fields.copy()
        f2 = {'x': 'wavepos', 'y_alt': 'spectral_flux'}
        f3 = {'x': 'wavepos', 'y': 'spectral_flux',
              'y_alt': 'spectral_flux'}

        # no panes
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=(None, None))
        blank_figure.change_axis_field(fields)
        assert set_mock.call_count == 0
        assert fields == f1
        sigs = signals.Signals()

        # a valid pane, primary axes
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=([pane.OneDimPane(sigs)], 'primary'))
        blank_figure.change_axis_field(fields)
        assert set_mock.call_count == 1
        assert fields == f1

        # secondary axis
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=([pane.OneDimPane(sigs)], 'alt'))
        blank_figure.change_axis_field(fields)
        assert set_mock.call_count == 2
        assert fields == f2

        # both axes
        fields = f1.copy()
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=([pane.OneDimPane(sigs)], 'both'))
        blank_figure.change_axis_field(fields)
        assert set_mock.call_count == 3
        assert fields == f3

    def test_set_orders(self, blank_figure, mocker):
        orders = {0: {'id': [1, 2, 3]}}
        set_patch = mocker.patch.object(pane.OneDimPane, 'set_orders')

        # pane is None, nothing happens
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=(None, None))
        sigs = signals.Signals()
        blank_figure.set_orders(orders)
        assert set_patch.call_count == 0

        # pane is single valued, set is called
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=(pane.OneDimPane(sigs), None))
        blank_figure.set_orders(orders)
        assert set_patch.call_count == 1

        # pane is list, only the first is called
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=([pane.OneDimPane(sigs),
                                          pane.OneDimPane(sigs)], None))
        blank_figure.set_orders(orders)
        assert set_patch.call_count == 2

    def test_set_scales(self, blank_figure, mocker):
        sigs = signals.Signals()
        scales = {'x': 'linear', 'y': 'log'}
        s1 = scales.copy()
        s2 = {'x': 'linear', 'y_alt': 'log'}
        s3 = {'x': 'linear', 'y': 'log', 'y_alt': 'log'}
        set_patch = mocker.patch.object(pane.OneDimPane, 'set_scales')

        # pane is None, nothing happens
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=(None, 'all'))
        blank_figure.set_scales(scales)
        assert set_patch.call_count == 0
        assert scales == s1

        # pane is list, set is called for primary on all
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=([pane.OneDimPane(sigs),
                                          pane.OneDimPane(sigs)], 'primary'))
        blank_figure.set_scales(scales)
        assert set_patch.call_count == 2
        assert scales == s1

        # call for alt
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=([pane.OneDimPane(sigs),
                                          pane.OneDimPane(sigs)], 'alt'))
        blank_figure.set_scales(scales)
        assert set_patch.call_count == 4
        assert scales == s2

        # call for both
        scales = s1.copy()
        mocker.patch.object(blank_figure, 'parse_pane_flag',
                            return_value=([pane.OneDimPane(sigs),
                                           pane.OneDimPane(sigs)], 'all'))
        blank_figure.set_scales(scales)
        assert set_patch.call_count == 6
        assert scales == s3

    def test_end_fit(self, blank_figure, mocker):
        sigs = signals.Signals()
        blank_figure.panes = [pane.OneDimPane(sigs)]
        fit_mock = mocker.patch.object(pane.OneDimPane, 'perform_fit',
                                       return_value=({}, list()))

        # one location - does nothing
        blank_figure._cursor_locations = [[0, 1]]
        blank_figure._end_fit(0)
        assert fit_mock.call_count == 0

        # two locations - should perform fit
        blank_figure._cursor_locations = [[0, 1], [2, 3]]
        blank_figure._end_fit(0)
        assert fit_mock.call_count == 1

        # same if locations are reversed
        blank_figure._cursor_locations = [[2, 3], [0, 1]]
        blank_figure._end_fit(0)
        assert fit_mock.call_count == 2

    def test_toggle_fits_visibility(self, blank_figure, gauss_model_fit,
                                    moffat_model_fit, grism_hdul):
        # no fits, nothing happens
        fits = list()
        blank_figure.toggle_fits_visibility(fits)
        assert len(blank_figure.gallery.arts['fit']) == 0

        # with fit, no panes, nothing happens
        fits = [gauss_model_fit]
        blank_figure.toggle_fits_visibility(fits)
        assert len(blank_figure.gallery.arts['fit']) == 0

        # with fit and pane and matching fields, fit gallery
        # are attempted to be regenerated, but fail because
        # there's no model in the pane
        blank_figure.add_panes(1)
        gauss_model_fit.fields = {'x': 'wavepos', 'y': 'spectral_flux'}
        gauss_model_fit.order = 0
        blank_figure.toggle_fits_visibility(fits)
        assert len(blank_figure.gallery.arts['fit']) == 0

        # add a model to the pane
        model = high_model.Grism(grism_hdul)
        blank_figure.add_model_to_pane(model)
        gauss_model_fit.model_id = model.id
        blank_figure.toggle_fits_visibility(fits)
        assert len(blank_figure.gallery.arts['fit']) == 2
        art1 = blank_figure.gallery.arts['fit'][0].get_artist()

        # remake when axis matches: artist is updated in place
        gauss_model_fit.axis = blank_figure.panes[0].axes()[0]
        blank_figure.toggle_fits_visibility(fits)
        assert len(blank_figure.gallery.arts['fit']) == 2
        art2 = blank_figure.gallery.arts['fit'][0].get_artist()
        assert art2 == art1

        # remake when original artist has been lost: replaces with new artist
        blank_figure.gallery.arts['fit'] = list()
        blank_figure.toggle_fits_visibility(fits)
        assert len(blank_figure.gallery.arts['fit']) == 2
        art3 = blank_figure.gallery.arts['fit'][0].get_artist()
        assert art3 != art1

        # stale_fit_artists should do the same: reset and replace
        blank_figure.stale_fit_artists(fits)
        assert len(blank_figure.gallery.arts['fit']) == 2
        art4 = blank_figure.gallery.arts['fit'][0].get_artist()
        assert art4 != art1

        # with another fit artist added to the same pane:
        # should add the gallery and not reset in between
        moffat_model_fit.fields = {'x': 'wavepos', 'y': 'spectral_flux'}
        moffat_model_fit.order = 0
        moffat_model_fit.model_id = model.id
        moffat_model_fit.axis = blank_figure.panes[0].axes()[0]
        fits.append(moffat_model_fit)
        blank_figure.stale_fit_artists(fits)
        assert len(blank_figure.gallery.arts['fit']) == 4

    def test_update_reference_lines(self, caplog, qtbot, blank_figure,
                                    grism_hdul):
        caplog.set_level(logging.DEBUG)

        # only reset for empty reference/panes
        ref = reference_model.ReferenceData()
        with qtbot.wait_signal(blank_figure.signals.atrophy_bg_partial):
            blank_figure.update_reference_lines(ref)
        assert 'Resetting reference artists' in caplog.text
        assert 'Updated reference' not in caplog.text

        # add data and lines
        model = high_model.Grism(grism_hdul)
        blank_figure.add_model_to_pane(model)
        ref.line_list = {'1': [5.1], '2': [6.3], '3': [7.4]}
        ref.line_unit = u.um
        ref.set_visibility('all', True)

        # reference lines added
        with qtbot.wait_signal(blank_figure.signals.atrophy_bg_partial):
            blank_figure.update_reference_lines(ref)
        assert 'Resetting reference artists' in caplog.text
        assert 'Updated reference' in caplog.text

    def test_model_extensions(self, mocker, blank_figure, grism_hdul):
        model = high_model.Grism(grism_hdul)
        blank_figure.add_model_to_pane(model)

        ext = blank_figure.model_extensions(model.id)
        assert ext == list()
        ext = blank_figure.model_extensions(model.id, pane_index=0)
        assert 'SPECTRAL_FLUX' in ext

    def test_unload_reference_model(self, mocker, blank_figure, grism_hdul):
        ref = reference_model.ReferenceData()

        # no op if no panes
        blank_figure.unload_reference_model(ref)

        # add a pane: calls unload_ref_model
        model = high_model.Grism(grism_hdul)
        blank_figure.add_model_to_pane(model)

        m1 = mocker.patch.object(blank_figure.panes[0], 'unload_ref_model')
        blank_figure.unload_reference_model(ref)
        m1.assert_called_once()

    def test_change_axis_limits(self, mocker, blank_figure, grism_hdul):
        # add data and lines
        model = high_model.Grism(grism_hdul)
        blank_figure.add_model_to_pane(model)
        ref = reference_model.ReferenceData()
        ref.line_list = {'1': [5.1], '2': [6.3], '3': [7.4]}
        ref.line_unit = u.um
        ref.set_visibility('all', True)
        blank_figure.update_reference_lines(ref)

        m1 = mocker.patch.object(blank_figure.gallery,
                                 'update_reference_data')

        # change limits
        blank_figure.change_axis_limits({'x': [4, 6]})
        assert m1.call_count == 1

        # reset zoom: update called again
        blank_figure.reset_zoom()
        assert m1.call_count == 2

        # zoom by mouse: also calls update
        blank_figure._cursor_locations = [[4, 4], [6, 4]]
        blank_figure._end_zoom(0, 'x')
        assert m1.call_count == 3

    def test_end_zoom_bad_call(self, blank_figure, mocker, caplog, grism_hdul):
        caplog.set_level(logging.DEBUG)
        model = high_model.Grism(grism_hdul)
        blank_figure.add_model_to_pane(model)

        blank_figure._cursor_locations = [(2, 4)]
        blank_figure._cursor_mode = 'x-zoom'

        blank_figure._end_zoom(0)

        assert 'Cancelling zoom' in caplog.text
        assert len(blank_figure._cursor_locations) == 0
