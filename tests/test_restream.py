import pytest
from unittest.mock import patch, MagicMock
import subprocess
import sys
import os

# Add the parent directory to Python path to import restream.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from restream import get_twitch_url, stream

def test_get_twitch_url_success():
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'http://fake.stream.url\n'
        mock_run.return_value = mock_result
        
        url = get_twitch_url('test_channel', 'best')
        assert url == 'http://fake.stream.url'

def test_get_twitch_url_failure():
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd', stderr='error')
        url = get_twitch_url('test_channel', 'best')
        assert url is None

def test_stream_setup():
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        process = stream(
            'http://fake.stream.url',
            'youtube-key',
            '4500k',
            '160k'
        )
        
        assert process == mock_process

def test_stream_failure():
    with patch('subprocess.Popen') as mock_popen:
        mock_popen.side_effect = subprocess.SubprocessError()
        process = stream(
            'http://fake.stream.url',
            'youtube-key',
            '4500k',
            '160k'
        )
        assert process is None