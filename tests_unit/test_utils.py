from unittest.mock import patch

import mock
import pandas as pd
import pytest

from utils.utils import area_of_cirle, volume_of_cylinder
from utils.utils_io import DataReader, long_function_involving_reading_data


# Basic test - check output of a function with given input is the expected output
def test_area_of_cirle():
    expected_output = 3.14

    output = area_of_cirle(1)

    assert round(output, 2) == expected_output


# Basic test - check output of a function with given input is the expected output
def test_volume_of_cylinder():

    expected_output = 6.28

    output = volume_of_cylinder(1, 2)

    assert round(output, 2) == expected_output


# pytest.mark.parametrize - shorter way of testing lots of inputs and corresponding expected outputs
@pytest.mark.parametrize("input, expected_output", [(2, 12.57), (3, 28.27), (4, 50.27)])
def test_area_of_cirle_2(input, expected_output):

    output = area_of_cirle(input)

    assert round(output, 2) == expected_output


# MagicMock - sets up a sort of dummy object (mock_engine below), with a set return_value
# we patch the object sqlalchemy.engine.base.Engine with the mock_engine object
# this means that when the test below is run, a call to sqlalchemy.engine.base.Engine gets diverted to
# so the database engine would be created and passed in to a function to read and return the data mock_engine
# and mock_engine's return value (set here to be a pandas testing dataframe) gets returned
# this means that a function calling data out of the db (and therefore needing authentication, db connection etc) can
# be run even if we don't have that database connection, authentication etc
def test_read_from_db():
    with mock.patch("sqlalchemy.engine.base.Engine") as mock_engine:
        mock_engine.engine.execute = mock.MagicMock(return_value=pd.util.testing.makeDataFrame())

        data_read_from_database = DataReader.read_from_db(mock_engine)

        assert type(data_read_from_database) == pd.DataFrame


# Similar idea, using the patch decorator: used to patch a method (read_data_from_a_file) of a class (DataReader) with a MagicMock (mock_read_data)
# the patch is set up then DataReader.read_data_from_a_file is called with some unused input
# since the return_value of the mock is set to 1, at the end we assert that output was 1
# (bit of a useless test but shows the idea)
@patch.object(DataReader, "read_data_from_a_file")
def test_read_data_from_a_file(mock_read_data):
    mock_read_data.return_value = 1
    output = DataReader.read_data_from_a_file("/data/path")
    assert output == 1


# Same idea as above, but in a more realistic context). We want to test the long_function_involving_reading_data function,
# which calls the DataReader.read_data_from_a_file method, which reads data using pd.read_csv().
# At test time we don't have access to the file being read by that function, so we patch DataReader.read_data_from_a_file
# with the mock_read_data MagicMock, and set its return value to be 'data'
# We then call long_function_involving_reading_data, which goes to call DataReader.read_data_from_a_file but gets diverted
# to mock_read_data, it calls mock_read_data, gets the output 'data', which gets passed back to long_function_involving_reading_data,
# then back to the test as output
# At the end we assert the output was indeed 'data'
# In this way we have tested a function that included a call to pd.read_csv, without actually calling pd.read_csv
# So we can test that the function is continuing to work in the expected way, without providing the testing environment access to the files.
@patch.object(DataReader, "read_data_from_a_file")
def test_long_function_involving_reading_data(mock_read_data):
    mock_read_data.return_value = "data"
    output = long_function_involving_reading_data()
    assert output == "data"
