import argparse
import subprocess
import logging
import sys
import time

def setup_logging(log_file):
    """Configure logging to both file and console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def get_twitch_url(channel, quality):
    """Get the Twitch stream URL using streamlink."""
    cmd = ["streamlink", "--stream-url", f"https://twitch.tv/{channel}", quality]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get Twitch URL: {e.stderr}")
        return None

def stream(twitch_url, youtube_key, video_bitrate, audio_bitrate):
    """Start FFmpeg process to restream from Twitch to YouTube."""
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", twitch_url,
        "-c:v", "copy",
        "-c:a", "copy",
        "-b:v", video_bitrate,
        "-b:a", audio_bitrate,
        "-f", "flv",
        f"rtmp://a.rtmp.youtube.com/live2/{youtube_key}"
    ]
    
    try:
        process = subprocess.Popen(ffmpeg_cmd)
        return process
    except subprocess.SubprocessError as e:
        logging.error(f"Failed to start FFmpeg: {e}")
        return None

def main():
    """Main function to handle command line arguments and run the restreamer."""
    parser = argparse.ArgumentParser(description='Restream from Twitch to YouTube')
    parser.add_argument('--twitch-channel', required=True, help='Twitch channel name')
    parser.add_argument('--youtube-key', required=True, help='YouTube stream key')
    parser.add_argument('--quality', default='best', help='Stream quality (default: best)')
    parser.add_argument('--video-bitrate', default='4500k', help='Video bitrate (default: 4500k)')
    parser.add_argument('--audio-bitrate', default='160k', help='Audio bitrate (default: 160k)')
    parser.add_argument('--log-file', default='restream.log', help='Log file path')
    parser.add_argument('--check-interval', type=int, default=60, help='Seconds between checking stream status')
    
    args = parser.parse_args()
    setup_logging(args.log_file)
    
    while True:
        try:
            logging.info(f"Checking stream for channel: {args.twitch_channel}")
            twitch_url = get_twitch_url(args.twitch_channel, args.quality)
            
            if twitch_url:
                logging.info("Stream is live, starting restream")
                process = stream(twitch_url, args.youtube_key, args.video_bitrate, args.audio_bitrate)
                
                if process:
                    process.wait()
                    logging.info("Stream ended")
            
            time.sleep(args.check_interval)
            
        except KeyboardInterrupt:
            logging.info("Shutting down")
            sys.exit(0)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(args.check_interval)

if __name__ == "__main__":
    main()