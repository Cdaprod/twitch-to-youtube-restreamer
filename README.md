# Twitch to YouTube Restreamer

[![CI](https://github.com/Cdaprod/twitch-to-youtube-restreamer/actions/workflows/ci.yml/badge.svg)](https://github.com/Cdaprod/twitch-to-youtube-restreamer/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Cdaprod/twitch-to-youtube-restreamer/branch/main/graph/badge.svg)](https://codecov.io/gh/Cdaprod/twitch-to-youtube-restreamer)

A Python-based restreaming solution that takes your Twitch streams and automatically restreams them to YouTube.

## Features

- Command-line based configuration
- No magic variables
- Automatic reconnection
- Detailed logging
- Docker support

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Cdaprod/twitch-to-youtube-restreamer.git
cd repo
```

2. Create a `.env` file:
```bash
TWITCH_CHANNEL=your_channel
YOUTUBE_KEY=your_youtube_key
```

3. Run with Docker:
```bash
docker-compose up -d
```

## Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest
```

## License

MIT