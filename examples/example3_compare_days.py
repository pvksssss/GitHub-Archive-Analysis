#!/usr/bin/env python3
"""
Example 3: Comparing Multiple Days

This example demonstrates how to download and compare GitHub activity
across multiple days to identify trends.
"""

import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from download_gharchive import GHArchiveDownloader
from analyze_events import EventAnalyzer


def analyze_day(date_str, hour=None):
    """Analyze events for a specific day.
    
    Args:
        date_str: Date in YYYY-MM-DD format
        hour: Optional specific hour to analyze
        
    Returns:
        EventAnalyzer instance with results
    """
    downloader = GHArchiveDownloader(output_dir="data")
    analyzer = EventAnalyzer()
    
    files = downloader.download_archive(date_str, hour=hour)
    
    for filepath in files:
        analyzer.analyze_file(filepath)
    
    return analyzer


def main():
    """Compare GitHub activity across multiple days."""
    
    print("="*60)
    print("Example 3: Comparing Multiple Days")
    print("="*60)
    print("\nThis example analyzes GitHub activity for the first")
    print("3 days of January 2015 and compares the results.")
    print()
    
    dates = ["2015-01-01", "2015-01-02", "2015-01-03"]
    results = {}
    
    # Analyze each day (using just one hour per day for faster processing)
    for date in dates:
        print(f"\nAnalyzing {date} (hour 12 only for speed)...")
        analyzer = analyze_day(date, hour=12)
        results[date] = analyzer
        print(f"✓ Found {analyzer.total_events:,} events")
    
    # Compare results
    print("\n" + "="*60)
    print("COMPARISON RESULTS")
    print("="*60)
    
    # Total events per day
    print("\n--- Total Events ---")
    for date in dates:
        print(f"  {date}: {results[date].total_events:,} events")
    
    # Most common event type each day
    print("\n--- Most Common Event Type ---")
    for date in dates:
        if results[date].event_types:
            top_event = results[date].event_types.most_common(1)[0]
            print(f"  {date}: {top_event[0]} ({top_event[1]:,} occurrences)")
    
    # Most active repository across all days
    print("\n--- Most Active Repository (across all days) ---")
    all_repos = defaultdict(int)
    for analyzer in results.values():
        for repo, count in analyzer.repos.items():
            all_repos[repo] += count
    
    top_repos = sorted(all_repos.items(), key=lambda x: x[1], reverse=True)[:5]
    for repo, count in top_repos:
        print(f"  {repo}: {count:,} events")
    
    # Growth/decline analysis
    print("\n--- Day-over-Day Change ---")
    for i in range(1, len(dates)):
        prev_date = dates[i-1]
        curr_date = dates[i]
        prev_count = results[prev_date].total_events
        curr_count = results[curr_date].total_events
        
        change = curr_count - prev_count
        change_pct = (change / prev_count * 100) if prev_count > 0 else 0
        
        direction = "↑" if change > 0 else "↓"
        print(f"  {prev_date} → {curr_date}: {direction} {abs(change):,} ({change_pct:+.1f}%)")


if __name__ == "__main__":
    main()
