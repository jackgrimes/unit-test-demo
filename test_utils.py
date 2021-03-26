import mock
import pandas as pd
import pytest

from utils import area_of_cirle, volume_of_cylinder, read_from_db


def test_area_of_cirle():
    assert round(area_of_cirle(1), 2) == 3.14


def test_volume_of_cylinder():
    assert round(volume_of_cylinder(1, 1), 2) == 3.14


@pytest.mark.parametrize("test_input, expected", [(2, 12.57), (3, 28.27), (4, 50.27)])
def test_area_of_cirle2(test_input, expected):
    print(1)
    rounded_result = round(area_of_cirle(test_input), 2)
    assert rounded_result == expected


def test_read_from_db():
    with mock.patch("sqlalchemy.engine.base.Engine") as mock_engine:
        mock_engine.engine.execute = mock.MagicMock(
            return_value=pd.util.testing.makeDataFrame()
        )

        data_read_from_database = read_from_db(mock_engine)

        assert type(data_read_from_database) == pd.DataFrame
