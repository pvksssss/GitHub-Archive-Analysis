#!/usr/bin/env python3
"""
GitHub Archive Downloader

This script downloads GitHub Archive data for specified date ranges.
The data is downloaded from https://data.gharchive.org/ in gzipped JSON format.

Usage:
    python download_gharchive.py --date 2015-01-01 --hour 15
    python download_gharchive.py --date 2015-01-01  # Downloads all hours for the day
    python download_gharchive.py --start-date 2015-01-01 --end-date 2015-01-05
"""

import argparse
import gzip
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator, List

import requests


class GHArchiveDownloader:
    """Download and process GitHub Archive data."""
    
    BASE_URL = "https://data.gharchive.org"
    
    def __init__(self, output_dir: str = "data"):
        """Initialize the downloader.
        
        Args:
            output_dir: Directory to save downloaded files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def download_archive(self, date: str, hour: int = None) -> List[str]:
        """Download archive(s) for a specific date and optionally hour.
        
        Args:
            date: Date in YYYY-MM-DD format
            hour: Optional hour (0-23). If None, downloads all hours.
            
        Returns:
            List of downloaded file paths
        """
        downloaded_files = []
        
        if hour is not None:
            # Download single hour
            url = f"{self.BASE_URL}/{date}-{hour}.json.gz"
            filepath = self._download_file(url, date, hour)
            if filepath:
                downloaded_files.append(filepath)
        else:
            # Download all hours for the day
            for h in range(24):
                url = f"{self.BASE_URL}/{date}-{h}.json.gz"
                filepath = self._download_file(url, date, h)
                if filepath:
                    downloaded_files.append(filepath)
        
        return downloaded_files
    
    def download_date_range(self, start_date: str, end_date: str) -> List[str]:
        """Download archives for a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of downloaded file paths
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        downloaded_files = []
        current = start
        
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            print(f"\nDownloading archives for {date_str}...")
            files = self.download_archive(date_str)
            downloaded_files.extend(files)
            current += timedelta(days=1)
        
        return downloaded_files
    
    def _download_file(self, url: str, date: str, hour: int) -> str:
        """Download a single archive file.
        
        Args:
            url: URL to download from
            date: Date string
            hour: Hour of the day
            
        Returns:
            Path to downloaded file, or None if failed
        """
        filename = f"{date}-{hour}.json.gz"
        filepath = self.output_dir / filename
        
        # Skip if already downloaded
        if filepath.exists():
            print(f"✓ {filename} already exists, skipping...")
            return str(filepath)
        
        try:
            print(f"Downloading {filename}...", end=" ")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = filepath.stat().st_size / (1024 * 1024)  # MB
            print(f"✓ Downloaded ({file_size:.2f} MB)")
            return str(filepath)
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed: {e}")
            return None
    
    def read_events(self, filepath: str) -> Generator[dict, None, None]:
        """Read and parse events from a downloaded archive.
        
        Args:
            filepath: Path to the gzipped JSON file
            
        Yields:
            Individual event dictionaries
        """
        with gzip.open(filepath, 'rt', encoding='utf-8') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    yield event
                except json.JSONDecodeError:
                    continue


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Download GitHub Archive data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download a specific hour
  python download_gharchive.py --date 2015-01-01 --hour 15
  
  # Download all hours for a day
  python download_gharchive.py --date 2015-01-01
  
  # Download a date range
  python download_gharchive.py --start-date 2015-01-01 --end-date 2015-01-05
        """
    )
    
    parser.add_argument(
        "--date",
        help="Date to download (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--hour",
        type=int,
        choices=range(24),
        help="Specific hour to download (0-23)"
    )
    parser.add_argument(
        "--start-date",
        help="Start date for range download (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date",
        help="End date for range download (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Output directory for downloaded files (default: data)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.start_date and args.end_date:
        if args.date or args.hour:
            print("Error: Cannot use --date/--hour with --start-date/--end-date")
            sys.exit(1)
    elif not args.date:
        print("Error: Must specify --date or --start-date/--end-date")
        sys.exit(1)
    
    downloader = GHArchiveDownloader(args.output_dir)
    
    try:
        if args.start_date and args.end_date:
            files = downloader.download_date_range(args.start_date, args.end_date)
        else:
            files = downloader.download_archive(args.date, args.hour)
        
        print(f"\n✓ Successfully downloaded {len(files)} file(s)")
        
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
