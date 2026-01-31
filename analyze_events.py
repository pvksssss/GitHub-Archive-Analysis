#!/usr/bin/env python3
"""
GitHub Archive Event Analyzer

This script analyzes downloaded GitHub Archive data and provides
various statistics and insights about GitHub events.

Usage:
    python analyze_events.py --file data/2015-01-01-15.json.gz
    python analyze_events.py --dir data --event-type PushEvent
"""

import argparse
import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Set

from download_gharchive import GHArchiveDownloader


class EventAnalyzer:
    """Analyze GitHub Archive events."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.event_types = Counter()
        self.repos = Counter()
        self.actors = Counter()
        self.events_by_type = defaultdict(list)
        self.total_events = 0
    
    def analyze_file(self, filepath: str, event_filter: str = None):
        """Analyze events from a single file.
        
        Args:
            filepath: Path to the gzipped JSON file
            event_filter: Optional event type to filter for
        """
        downloader = GHArchiveDownloader()
        
        for event in downloader.read_events(filepath):
            self.total_events += 1
            
            event_type = event.get('type', 'Unknown')
            
            # Apply filter if specified
            if event_filter and event_type != event_filter:
                continue
            
            # Collect statistics
            self.event_types[event_type] += 1
            
            if 'repo' in event and 'name' in event['repo']:
                self.repos[event['repo']['name']] += 1
            
            if 'actor' in event and 'login' in event['actor']:
                self.actors[event['actor']['login']] += 1
            
            # Store event for detailed analysis
            self.events_by_type[event_type].append(event)
    
    def analyze_directory(self, dirpath: str, event_filter: str = None):
        """Analyze all archive files in a directory.
        
        Args:
            dirpath: Path to directory containing archive files
            event_filter: Optional event type to filter for
        """
        dir_path = Path(dirpath)
        files = sorted(dir_path.glob("*.json.gz"))
        
        if not files:
            print(f"No archive files found in {dirpath}")
            return
        
        print(f"Analyzing {len(files)} file(s)...")
        for filepath in files:
            print(f"Processing {filepath.name}...", end=" ")
            self.analyze_file(str(filepath), event_filter)
            print("✓")
    
    def print_summary(self, top_n: int = 10):
        """Print analysis summary.
        
        Args:
            top_n: Number of top items to show in rankings
        """
        print("\n" + "="*60)
        print("GITHUB ARCHIVE ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\nTotal events analyzed: {self.total_events:,}")
        
        # Event types distribution
        print(f"\n--- Event Types (Top {top_n}) ---")
        for event_type, count in self.event_types.most_common(top_n):
            percentage = (count / self.total_events) * 100 if self.total_events > 0 else 0
            print(f"  {event_type:30s}: {count:8,} ({percentage:5.2f}%)")
        
        # Most active repositories
        print(f"\n--- Most Active Repositories (Top {top_n}) ---")
        for repo, count in self.repos.most_common(top_n):
            print(f"  {repo:40s}: {count:6,} events")
        
        # Most active users
        print(f"\n--- Most Active Users (Top {top_n}) ---")
        for actor, count in self.actors.most_common(top_n):
            print(f"  {actor:30s}: {count:6,} events")
        
        # Detailed event type analysis
        print(f"\n--- Event Type Details ---")
        for event_type in sorted(self.event_types.keys()):
            count = self.event_types[event_type]
            print(f"  {event_type}: {count:,} events")
            
            # Additional details for specific event types
            if event_type == "PushEvent":
                self._analyze_push_events()
            elif event_type == "IssuesEvent":
                self._analyze_issue_events()
            elif event_type == "PullRequestEvent":
                self._analyze_pr_events()
    
    def _analyze_push_events(self):
        """Analyze PushEvent details."""
        push_events = self.events_by_type.get("PushEvent", [])
        if not push_events:
            return
        
        total_commits = 0
        for event in push_events:
            payload = event.get('payload', {})
            if 'commits' in payload:
                total_commits += len(payload['commits'])
        
        avg_commits = total_commits / len(push_events) if push_events else 0
        print(f"    → Total commits: {total_commits:,}")
        print(f"    → Average commits per push: {avg_commits:.2f}")
    
    def _analyze_issue_events(self):
        """Analyze IssuesEvent details."""
        issue_events = self.events_by_type.get("IssuesEvent", [])
        if not issue_events:
            return
        
        actions = Counter()
        for event in issue_events:
            payload = event.get('payload', {})
            action = payload.get('action', 'unknown')
            actions[action] += 1
        
        for action, count in actions.most_common():
            print(f"    → {action}: {count:,}")
    
    def _analyze_pr_events(self):
        """Analyze PullRequestEvent details."""
        pr_events = self.events_by_type.get("PullRequestEvent", [])
        if not pr_events:
            return
        
        actions = Counter()
        for event in pr_events:
            payload = event.get('payload', {})
            action = payload.get('action', 'unknown')
            actions[action] += 1
        
        for action, count in actions.most_common():
            print(f"    → {action}: {count:,}")
    
    def export_to_json(self, output_file: str):
        """Export analysis results to JSON.
        
        Args:
            output_file: Path to output JSON file
        """
        results = {
            "total_events": self.total_events,
            "event_types": dict(self.event_types),
            "top_repos": dict(self.repos.most_common(100)),
            "top_actors": dict(self.actors.most_common(100))
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Results exported to {output_file}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Analyze GitHub Archive events",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single file
  python analyze_events.py --file data/2015-01-01-15.json.gz
  
  # Analyze all files in a directory
  python analyze_events.py --dir data
  
  # Filter by event type
  python analyze_events.py --dir data --event-type PushEvent
  
  # Export results to JSON
  python analyze_events.py --dir data --output results.json
        """
    )
    
    parser.add_argument(
        "--file",
        help="Single archive file to analyze"
    )
    parser.add_argument(
        "--dir",
        help="Directory containing archive files to analyze"
    )
    parser.add_argument(
        "--event-type",
        help="Filter for specific event type (e.g., PushEvent, IssuesEvent)"
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top items to show (default: 10)"
    )
    parser.add_argument(
        "--output",
        help="Export results to JSON file"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.file and not args.dir:
        print("Error: Must specify --file or --dir")
        sys.exit(1)
    
    if args.file and args.dir:
        print("Error: Cannot specify both --file and --dir")
        sys.exit(1)
    
    analyzer = EventAnalyzer()
    
    try:
        if args.file:
            print(f"Analyzing {args.file}...")
            analyzer.analyze_file(args.file, args.event_type)
        else:
            analyzer.analyze_directory(args.dir, args.event_type)
        
        analyzer.print_summary(args.top)
        
        if args.output:
            analyzer.export_to_json(args.output)
        
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
