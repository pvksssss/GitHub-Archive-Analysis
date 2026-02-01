#!/usr/bin/env python3
"""
Example 2: Event Type Focus

This example demonstrates how to filter and analyze a specific event type
(PushEvent) to understand code push patterns on GitHub.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from download_gharchive import GHArchiveDownloader
from analyze_events import EventAnalyzer


def main():
    """Analyze push events specifically."""
    
    print("="*60)
    print("Example 2: Analyzing Push Events")
    print("="*60)
    print("\nThis example focuses on PushEvent data to understand")
    print("code push patterns, commit volumes, and active repositories.")
    print()
    
    # Download data for a full day (all 24 hours)
    print("Step 1: Downloading data for full day (2015-01-01)...")
    downloader = GHArchiveDownloader(output_dir="data")
    files = downloader.download_archive("2015-01-01")
    
    if not files:
        print("Failed to download data")
        return
    
    print(f"✓ Downloaded {len(files)} file(s)")
    
    # Analyze only PushEvents
    print("\nStep 2: Analyzing PushEvents only...")
    analyzer = EventAnalyzer()
    
    for filepath in files:
        analyzer.analyze_file(filepath, event_filter="PushEvent")
    
    # Display results
    print("\nStep 3: Results - Push Event Analysis")
    analyzer.print_summary(top_n=10)
    
    # Additional insights
    push_events = analyzer.events_by_type.get("PushEvent", [])
    if push_events:
        print("\n--- Additional Push Insights ---")
        
        # Count unique repositories with pushes
        unique_repos = len(analyzer.repos)
        print(f"Unique repositories with pushes: {unique_repos:,}")
        
        # Count unique contributors
        unique_users = len(analyzer.actors)
        print(f"Unique users who pushed code: {unique_users:,}")
        
        # Calculate average events per repo and user
        avg_per_repo = len(push_events) / unique_repos if unique_repos > 0 else 0
        avg_per_user = len(push_events) / unique_users if unique_users > 0 else 0
        print(f"Average pushes per repository: {avg_per_repo:.2f}")
        print(f"Average pushes per user: {avg_per_user:.2f}")


if __name__ == "__main__":
    main()
