"""Test functions for specparam.utils.io."""

import numpy as np

from specparam.core.items import OBJ_DESC
from specparam.objs import SpectralModel, SpectralGroupModel

from specparam.tests.settings import TEST_DATA_PATH

from specparam.utils.io import *

###################################################################################################
###################################################################################################

def test_load_model():

    file_name = 'test_all'

    tfm = load_model(file_name, TEST_DATA_PATH)

    assert isinstance(tfm, SpectralModel)

    # Check that all elements get loaded
    for result in OBJ_DESC['results']:
        assert not np.all(np.isnan(getattr(tfm, result)))
    for setting in OBJ_DESC['settings']:
        assert getattr(tfm, setting) is not None
    for data in OBJ_DESC['data']:
        assert getattr(tfm, data) is not None
    for meta_dat in OBJ_DESC['meta_data']:
        assert getattr(tfm, meta_dat) is not None

def test_load_group():

    file_name = 'test_group_all'
    tfg = load_group(file_name, TEST_DATA_PATH)

    assert isinstance(tfg, SpectralGroupModel)

    # Check that all elements get loaded
    assert len(tfg.group_results) > 0
    for setting in OBJ_DESC['settings']:
        assert getattr(tfg, setting) is not None
    assert tfg.power_spectra is not None
    for meta_dat in OBJ_DESC['meta_data']:
        assert getattr(tfg, meta_dat) is not None
