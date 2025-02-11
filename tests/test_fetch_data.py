#!/usr/bin/env python3

import pytest
from imessage_reader import fetch_data


def test_fetch_data_basic():
    """Test basic initialization without contact filter"""
    data = fetch_data.FetchData("/Users/bodo/Documents")
    assert data.db_path == "/Users/bodo/Documents"
    assert data.contact_filter is None


def test_fetch_data_with_contact():
    """Test initialization with contact filter"""
    data = fetch_data.FetchData("/Users/bodo/Documents", contact_filter="+1234567890")
    assert data.db_path == "/Users/bodo/Documents"
    assert data.contact_filter == "+1234567890"


def test_read_database_sql_generation(mocker):
    """Test SQL query generation with and without contact filter"""
    # Mock the common.fetch_db_data to avoid actual database calls
    mock_fetch = mocker.patch('imessage_reader.common.fetch_db_data', return_value=[])
    
    # Test without contact filter
    data = fetch_data.FetchData("/Users/bodo/Documents")
    data._read_database()
    
    # Test with contact filter
    data_filtered = fetch_data.FetchData("/Users/bodo/Documents", contact_filter="+1234567890")
    data_filtered._read_database()
    
    # Get the calls made to the mocked function
    calls = mock_fetch.call_args_list
    
    # Verify the SQL queries
    assert "WHERE" not in calls[0][0][1]  # First call should not have WHERE clause
    assert "WHERE handle.id = '+1234567890'" in calls[1][0][1]  # Second call should have WHERE clause