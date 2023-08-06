from functools import partial

import numpy as np

from yt_napari._ds_cache import dataset_cache
from yt_napari._widget_reader import ReaderWidget, SelectionEntry
from yt_napari.viewer import Scene

# note: the cache is disabled for all the tests in this file due to flakiness
# in github CI. It may be that loading from a true file, rather than the
# yt_ugrid_ds_fn fixture would fix that...


def test_widget_reader_add_selections(make_napari_viewer, yt_ugrid_ds_fn):
    viewer = make_napari_viewer()
    r = ReaderWidget(napari_viewer=viewer)
    r.add_new_button.click()
    assert len(r.active_selections) == 1
    sel = list(r.active_selections.values())[0]
    assert isinstance(sel, SelectionEntry)
    assert sel.selection_type == "Region"
    sel.expand()
    sel.expand()
    r.layer_deletion_button.click()
    assert len(r.active_selections) == 0

    r.new_selection_type.setCurrentIndex(1)
    r.add_new_button.click()
    assert len(r.active_selections) == 1
    sel = list(r.active_selections.values())[0]
    assert isinstance(sel, SelectionEntry)
    assert sel.selection_type == "Slice"


def _rebuild_data(final_shape, data):
    # the yt file thats being loaded from the pytest fixture is a saved
    # dataset created from an in-memory uniform grid, and the re-loaded
    # dataset will not have the full functionality of a ds. so here, we
    # inject a correctly shaped random array here. If we start using full
    # test datasets from yt in testing, this should be changed.
    return np.random.random(final_shape) * data.mean()


def test_widget_reader(make_napari_viewer, yt_ugrid_ds_fn):

    viewer = make_napari_viewer()
    r = ReaderWidget(napari_viewer=viewer)
    r.ds_container.filename.value = yt_ugrid_ds_fn
    r.ds_container.store_in_cache.value = False
    r.add_new_button.click()
    sel = list(r.active_selections.values())[0]
    assert isinstance(sel, SelectionEntry)

    mgui_region = sel.selection_container_raw
    mgui_region.fields.field_type.value = "gas"
    mgui_region.fields.field_name.value = "density"
    mgui_region.resolution.value = (10, 10, 10)

    rebuild = partial(_rebuild_data, mgui_region.resolution.value)
    r._post_load_function = rebuild
    r.load_data()


def test_subsequent_load(make_napari_viewer, yt_ugrid_ds_fn):
    viewer = make_napari_viewer()

    r = ReaderWidget(napari_viewer=viewer)
    r.ds_container.filename.value = yt_ugrid_ds_fn
    r.ds_container.store_in_cache.value = False
    r.add_new_button.click()

    sel = list(r.active_selections.values())[0]
    assert isinstance(sel, SelectionEntry)

    mgui_region = sel.selection_container_raw
    mgui_region.fields.field_type.value = "gas"
    mgui_region.fields.field_name.value = "density"
    mgui_region.resolution.value = (10, 10, 10)

    rebuild = partial(_rebuild_data, mgui_region.resolution.value)
    r._post_load_function = rebuild
    r.load_data()

    # alter parameters, load again
    mgui_region.fields.field_name.value = "temperature"
    mgui_region.left_edge.value.value = (0.4, 0.4, 0.4)
    mgui_region.right_edge.value.value = (0.6, 0.6, 0.6)
    r.load_data()

    # the viewer should now have two images
    assert len(viewer.layers) == 2

    temp_layer = viewer.layers[1]
    assert temp_layer.metadata["_yt_napari_layer"] is True

    r.clear_cache()
    assert len(dataset_cache.available) == 0

    _ = r.yt_scene
    yt_scene = r.yt_scene
    assert isinstance(yt_scene, Scene)
