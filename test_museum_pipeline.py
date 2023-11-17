"""Unit Test's for all pythons files in kafka_museum folder."""
# pylint: disable=R0801, W0612, C0103
from unittest.mock import MagicMock, patch

from pipeline import insert_data_to_assistance_table, insert_data_to_emergencies_table
from pipeline import insert_data_to_visitor_ratings_table
from consumer import check_msg_valid


@patch("kafka_pipeline.get_db_connection")
def test_insert_data_to_assistance_table_calls_commit(mock_connection):
    """Test's that the insert_data_to_assistance_table function calls commit."""

    mock_connection = MagicMock()
    fake_commit = mock_connection.commit

    insert_data_to_assistance_table(
        {'at': "a_fake_time", 'site': 'some_site'}, mock_connection)

    assert fake_commit.call_count == 1


@patch("kafka_pipeline.get_db_connection")
def test_insert_data_to_emergencies_table_calls_commit(mock_connection):
    """Test's that the insert_data_to_emergencies_table function calls commit."""

    mock_connection = MagicMock()
    fake_commit = mock_connection.commit

    insert_data_to_emergencies_table(
        {'at': "a_fake_time", 'site': 'some_site'}, mock_connection)

    assert fake_commit.call_count == 1


@patch("kafka_pipeline.get_db_connection")
def test_insert_data_to_visitor_ratings_table_calls_commit(mock_connection):
    """Test's that the insert_data_to_visitor_ratings_table function calls commit."""

    mock_connection = MagicMock()
    fake_commit = mock_connection.commit

    insert_data_to_visitor_ratings_table({'at': "a_fake_time",
                                          'site': 'some_site',
                                          'val': 3},
                                         mock_connection)

    assert fake_commit.call_count == 1


@patch("kafka_pipeline.get_db_connection")
def test_insert_data_to_assistance_table_calls_execute(mock_connection):
    """Test's that the insert_data_to_assistance_table function calls execute."""

    mock_connection = MagicMock()
    mock_execute = mock_connection.cursor().execute

    insert_data_to_assistance_table(
        {'at': "a_fake_time", 'site': 'some_site'}, mock_connection)

    assert mock_execute.call_count == 1


@patch("kafka_pipeline.get_db_connection")
def test_insert_data_to_emergencies_table_calls_execute(mock_connection):
    """Test's that the insert_data_to_emergencies_table function calls execute."""

    mock_connection = MagicMock()
    mock_execute = mock_connection.cursor().execute

    insert_data_to_emergencies_table(
        {'at': "a_fake_time", 'site': 'some_site'}, mock_connection)

    assert mock_execute.call_count == 1


@patch("kafka_pipeline.get_db_connection")
def test_insert_data_to_visitor_ratings_table_calls_execute(mock_connection):
    """Test's that the insert_data_to_visitor_ratings_table function calls execute."""

    mock_connection = MagicMock()
    mock_execute = mock_connection.cursor().execute

    insert_data_to_visitor_ratings_table({'at': "a_fake_time",
                                          'site': 'some_site',
                                          'val': 3}, mock_connection)

    assert mock_execute.call_count == 1


def test_check_msg_valid_no_at():
    """Test's check msg valid function returns error if no at."""

    decoded_msg = {'site': 4, 'val': 3}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: at missing from message."


def test_check_msg_valid_no_site():
    """Test's check msg valid function returns error if no site."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00', 'val': 3}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: site missing from message."


def test_check_msg_valid_no_val():
    """Test's check msg valid function returns error if no val."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00', 'site': 3}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: val missing from message."


def test_check_msg_valid_site_num_out_of_range():
    """Test's check msg valid function returns error if site number out of range."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00',
                   'site': 2000, 'val': 3}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: site number does not exist."


def test_check_msg_valid_site_not_a_valid_integer():
    """Test's check msg valid function returns error if site not valid integer."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00',
                   'site': 'hello', 'val': 3}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: site is not a valid integer."


def test_check_msg_valid_val_is_none():
    """Test's check msg valid function returns error if val is none."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00',
                   'site': 3, 'val': None}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: val number cannot be none."


def test_check_msg_valid_val_is_out_of_range():
    """Test's check msg valid function returns error if val is out of range."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00', 'site': 3, 'val': 20}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: val number not within valid range."


def test_check_msg_valid_val_not_integer():
    """Test's check msg valid function returns error if val is out of range."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00',
                   'site': 3, 'val': 'hello'}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: val is not a valid integer."


def test_check_msg_valid_type_not_present():
    """Test's check msg valid function returns error if type not present with val of -1."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00', 'site': 3, 'val': -1}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: type is not present when it should be."


def test_check_msg_valid_type_is_none():
    """Test's check msg valid function returns error if type is none with val of -1."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00',
                   'site': 3, 'val': -1, 'type': None}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: type cannot be None (must be 0 or 1)."


def test_check_msg_valid_type_is_invalid_int():
    """Test's check msg valid function returns error if type invalid integer with val of -1."""

    decoded_msg = {'at': '2023-11-14 16:16:53.743853+00',
                   'site': 3, 'val': -1, 'type': 4}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: type is not a valid integer."


def test_check_msg_valid_at_after_18_15():
    """Test's check msg valid function returns error if after 6:45pm."""

    decoded_msg = {
        'at': '2023-11-14T18:15:53.743853+00:00', 'site': 3, 'val': 2}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: Must be between 8:45am and 6:15pm."


def test_check_msg_valid_at_after_8_45():
    """Test's check msg valid function returns error if before 8:45am."""

    decoded_msg = {
        'at': '2023-11-14T08:44:53.743853+00:00', 'site': 3, 'val': 2}

    result = check_msg_valid(decoded_msg)

    assert result["error"] is True
    assert result["message"] == "Invalid: Must be between 8:45am and 6:15pm."


def test_check_msg_valid_success():
    """Test's check msg valid function returns success if all detailed correct."""

    decoded_msg = {
        'at': '2023-11-14T08:46:53.743853+00:00', 'site': 3, 'val': 2}

    result = check_msg_valid(decoded_msg)

    assert result == {
        'at': '2023-11-14T08:46:53.743853+00:00', 'site': 3, 'val': 2}


def test_check_msg_valid_success_with_type_assistance():
    """Test's check msg valid function returns success 
    if all detailed correct with assistance type."""

    decoded_msg = {'at': '2023-11-14T08:46:53.743853+00:00',
                   'site': 3, 'val': -1, 'type': 0}

    result = check_msg_valid(decoded_msg)

    assert result == {'at': '2023-11-14T08:46:53.743853+00:00',
                      'site': 3, 'val': -1, 'type': 0}


def test_check_msg_valid_success_with_type_emergency():
    """Test's check msg valid function returns success 
    if all detailed correct with emergency type."""

    decoded_msg = {'at': '2023-11-14T08:46:53.743853+00:00',
                   'site': 3, 'val': -1, 'type': 1}

    result = check_msg_valid(decoded_msg)

    assert result == {'at': '2023-11-14T08:46:53.743853+00:00',
                      'site': 3, 'val': -1, 'type': 1}
