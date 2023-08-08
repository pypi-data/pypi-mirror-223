"""Utilities for input / output for data and models."""

###################################################################################################
###################################################################################################

def load_model(file_name, file_path=None, regenerate=True):
    """Load a model file.

    Parameters
    ----------
    file_name : str or FileObject
        File to load the data from.
    file_path : Path or str, optional
        Path to directory to load from. If None, loads from current directory.
    regenerate : bool, optional, default: True
        Whether to regenerate the model fit from the loaded data, if data is available.

    Returns
    -------
    model : SpectralModel
        Object with the loaded data.
    """

    # Initialize a model object (imported locally to avoid circular imports)
    from specparam.objs import SpectralModel
    model = SpectralModel()

    # Load data into object
    model.load(file_name, file_path, regenerate)

    return model


def load_group(file_name, file_path=None):
    """Load a group file.

    Parameters
    ----------
    file_name : str
        File to load data data.
    file_path : Path or str, optional
        Path to directory to load from. If None, loads from current directory.

    Returns
    -------
    group : SpectralGroupModel
        Object with the loaded data.
    """

    # Initialize a group object (imported locally to avoid circular imports)
    from specparam.objs import SpectralGroupModel
    group = SpectralGroupModel()

    # Load data into object
    group.load(file_name, file_path)

    return group
