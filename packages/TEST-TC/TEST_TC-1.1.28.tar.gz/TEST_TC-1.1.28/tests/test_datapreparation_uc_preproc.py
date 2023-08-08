import pandas as pd
from test_tc.datapreparation.uc_preproc import TCPreprocess, TVPreprocess, TAPreprocess, TMPreprocess

def sample_data():
    # Sample data for testing
    data = {
        "column_a": [1, 2, 3],
        "column_b": [4, 5, 6],
        "column_c": [7, 8, 9],
        'target_col': ['a','a','b']
    }
    return pd.DataFrame(data)

def sample_dataTV():
    # Sample data for testing
    data = {
        "column_a": [1, 2, 3],
        "column_b": [4, 5, 6],
        "column_c": ['7', '8', '9'],
        'target_col': ['a','a','b']
    }
    return pd.DataFrame(data)

def test_TCPreprocess():

    hierarchy = {
        "level_1": "column_a",
        "level_2": "column_b",
        "level_3": "column_c"
    }
    conversion = {
        "level_1": None,
        "level_2": None,
        "level_3": "{7: 'seven', 8: 'eight', 9: 'nine'}"
    }

    target_col = "target_col"

    # Sample data for testing
    df = sample_data()
    preprocess = TCPreprocess(hierarchy, conversion, target_col)

    # Test fit method
    preprocess_fit = preprocess.fit()

    # fit() should return the same instance of the TCPreprocess object
    assert preprocess_fit is preprocess

    # Test transform method
    transformed_data = preprocess.transform(df)

    # Check if the columns are correctly mapped from the hierarchy and conversion dictionaries
    for value in transformed_data['column_c']:
        assert value in ['seven', 'eight', 'nine']

    # Check if the target col has been filtered
    assert transformed_data.shape[0] == 2
   
def test_TVPreprocess():

    hierarchy = {
        "level_1": "column_a",
        "level_2": "column_b",
        "level_3": "column_c"
    }
    conversion = {
        "level_1": None,
        "level_2": None,
        "level_3": "{7: 'seven', 8: 'eight', 9: 'nine'}"
    }

    # Sample data for testing
    df = sample_dataTV()
    preprocess = TVPreprocess(hierarchy, conversion)

    # Test fit method
    preprocess_fit = preprocess.fit()

    # fit() should return the same instance of the TVPreprocess object
    assert preprocess_fit is preprocess

    # Test transform method
    transformed_data = preprocess.transform(df)

    # Check if the columns are correctly mapped from the hierarchy and conversion dictionaries
    for value in transformed_data['column_c']:
        assert value in ['seven', 'eight', 'nine']

    # Check if the target col has NOT been filtered
    assert transformed_data.shape[0] == 3

def test_TMPreprocess():
    hierarchy = {
        "level_1": "column_a",
        "level_2": "column_b",
        "level_3": "column_c"
    }
    conversion = {
        "level_1": None,
        "level_2": None,
        "level_3": "{7: 'seven', 8: 'eight', 9: 'nine'}"
    }

    # Sample data for testing
    df = sample_data()

    preprocess = TMPreprocess(hierarchy, conversion)

    # Test fit method
    preprocess_fit = preprocess.fit()

    # fit() should return the same instance of the TMPreprocess object
    assert preprocess_fit is preprocess

    # Test transform method
    transformed_data = preprocess.transform(df)

   # Check if the columns are correctly mapped from the hierarchy and conversion dictionaries
    for value in transformed_data['column_c']:
        assert value in ['seven', 'eight', 'nine']

    # Check if the target col has been filtered
    assert transformed_data.shape[0] == 3

def test_TAPreprocess():
    hierarchy = {
        "level_1": "column_a",
        "level_2": "column_b",
        "level_3": "column_c"
    }
    conversion = {
        "level_1": None,
        "level_2": None,
        "level_3": "{7: 'seven', 8: 'eight', 9: 'nine'}"
    }

    # Sample data for testing
    df = sample_data()
    preprocess = TAPreprocess(hierarchy, conversion)

    # Test fit method
    preprocess_fit = preprocess.fit()

    # fit() should return the same instance of the TAPreprocess object
    assert preprocess_fit is preprocess

    # Test transform method
    transformed_data = preprocess.transform(df)

    # Check if the columns are correctly mapped from the hierarchy and conversion dictionaries
    for value in transformed_data['column_c']:
        assert value in ['seven', 'eight', 'nine']

    # Check if the target col has been filtered
    assert transformed_data.shape[0] == 3