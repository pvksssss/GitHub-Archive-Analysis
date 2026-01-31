#!/usr/bin/env python3
"""
Example 1: Basic Event Analysis

This example demonstrates how to download and analyze GitHub Archive data
for a single day, showing basic statistics about events, repositories, and users.
"""

import sys
import os

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from download_gharchive import GHArchiveDownloader
from analyze_events import EventAnalyzer


def main():
    """Run basic event analysis example."""
    
    print("="*60)
    print("Example 1: Basic Event Analysis")
    print("="*60)
    print("\nThis example will:")
    print("1. Download GitHub Archive data for January 1, 2015, 3PM UTC")
    print("2. Analyze the events in that archive")
    print("3. Display statistics about event types, repos, and users")
    print()
    
    # Step 1: Download data
    print("Step 1: Downloading data...")
    downloader = GHArchiveDownloader(output_dir="data")
    files = downloader.download_archive("2015-01-01", hour=15)
    
    if not files:
        print("Failed to download data")
        return
    
    print(f"✓ Downloaded {len(files)} file(s)")
    
    # Step 2: Analyze events
    print("\nStep 2: Analyzing events...")
    analyzer = EventAnalyzer()
    analyzer.analyze_file(files[0])
    
    # Step 3: Display results
    print("\nStep 3: Results")
    analyzer.print_summary(top_n=5)
    
    # Export to JSON
    output_file = "example1_results.json"
    analyzer.export_to_json(output_file)
    print(f"\n✓ Analysis complete! Results saved to {output_file}")


if __name__ == "__main__":
    main()
