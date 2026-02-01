#!/usr/bin/env python3
"""
Test script to verify GitHub Archive Analysis functionality with mock data.
"""

import json
import gzip
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyze_events import EventAnalyzer


def create_mock_data():
    """Create mock GitHub Archive data for testing."""
    
    # Create test data directory
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    
    # Sample events
    events = [
        {
            "id": "1",
            "type": "PushEvent",
            "actor": {"login": "user1"},
            "repo": {"name": "owner1/repo1"},
            "payload": {"commits": [{"sha": "abc123"}]},
            "created_at": "2015-01-01T15:00:00Z"
        },
        {
            "id": "2",
            "type": "PushEvent",
            "actor": {"login": "user2"},
            "repo": {"name": "owner1/repo1"},
            "payload": {"commits": [{"sha": "def456"}, {"sha": "ghi789"}]},
            "created_at": "2015-01-01T15:01:00Z"
        },
        {
            "id": "3",
            "type": "IssuesEvent",
            "actor": {"login": "user1"},
            "repo": {"name": "owner2/repo2"},
            "payload": {"action": "opened"},
            "created_at": "2015-01-01T15:02:00Z"
        },
        {
            "id": "4",
            "type": "PullRequestEvent",
            "actor": {"login": "user3"},
            "repo": {"name": "owner2/repo2"},
            "payload": {"action": "opened"},
            "created_at": "2015-01-01T15:03:00Z"
        },
        {
            "id": "5",
            "type": "PushEvent",
            "actor": {"login": "user1"},
            "repo": {"name": "owner3/repo3"},
            "payload": {"commits": [{"sha": "jkl012"}]},
            "created_at": "2015-01-01T15:04:00Z"
        },
        {
            "id": "6",
            "type": "IssuesEvent",
            "actor": {"login": "user2"},
            "repo": {"name": "owner1/repo1"},
            "payload": {"action": "closed"},
            "created_at": "2015-01-01T15:05:00Z"
        },
        {
            "id": "7",
            "type": "WatchEvent",
            "actor": {"login": "user4"},
            "repo": {"name": "owner1/repo1"},
            "payload": {},
            "created_at": "2015-01-01T15:06:00Z"
        },
        {
            "id": "8",
            "type": "ForkEvent",
            "actor": {"login": "user4"},
            "repo": {"name": "owner1/repo1"},
            "payload": {},
            "created_at": "2015-01-01T15:07:00Z"
        }
    ]
    
    # Write to gzipped JSON file
    filepath = test_dir / "test-2015-01-01-15.json.gz"
    with gzip.open(filepath, 'wt', encoding='utf-8') as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
    
    print(f"✓ Created mock data file: {filepath}")
    return str(filepath)


def test_analysis(filepath):
    """Test the event analyzer with mock data."""
    
    print("\n" + "="*60)
    print("Testing Event Analysis")
    print("="*60)
    
    analyzer = EventAnalyzer()
    analyzer.analyze_file(filepath)
    
    print(f"\n✓ Successfully analyzed {analyzer.total_events} events")
    
    # Verify results
    assert analyzer.total_events == 8, f"Expected 8 events, got {analyzer.total_events}"
    assert analyzer.event_types["PushEvent"] == 3, "Expected 3 PushEvents"
    assert analyzer.event_types["IssuesEvent"] == 2, "Expected 2 IssuesEvents"
    assert analyzer.repos["owner1/repo1"] == 5, "Expected 5 events for owner1/repo1"
    assert analyzer.actors["user1"] == 3, "Expected 3 events from user1"
    
    print("✓ All assertions passed!")
    
    # Print summary
    analyzer.print_summary(top_n=5)
    
    # Test JSON export
    output_file = "test_data/test_results.json"
    analyzer.export_to_json(output_file)
    
    # Verify JSON export
    with open(output_file, 'r') as f:
        results = json.load(f)
    
    assert results["total_events"] == 8
    assert "event_types" in results
    assert "top_repos" in results
    assert "top_actors" in results
    
    print("✓ JSON export verified!")


def test_event_filtering(filepath):
    """Test filtering by event type."""
    
    print("\n" + "="*60)
    print("Testing Event Filtering")
    print("="*60)
    
    analyzer = EventAnalyzer()
    analyzer.analyze_file(filepath, event_filter="PushEvent")
    
    print(f"\n✓ Filtered to {analyzer.total_events} PushEvents")
    
    # Verify filtering
    assert analyzer.total_events == 3, f"Expected 3 PushEvents, got {analyzer.total_events}"
    assert len(analyzer.event_types) == 1, "Should only have one event type"
    assert "PushEvent" in analyzer.event_types
    
    print("✓ Event filtering works correctly!")


def main():
    """Run all tests."""
    
    print("="*60)
    print("GitHub Archive Analysis - Functional Test")
    print("="*60)
    
    try:
        # Create mock data
        print("\nStep 1: Creating mock data...")
        filepath = create_mock_data()
        
        # Test analysis
        print("\nStep 2: Testing event analysis...")
        test_analysis(filepath)
        
        # Test filtering
        print("\nStep 3: Testing event filtering...")
        test_event_filtering(filepath)
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\nThe GitHub Archive Analysis toolkit is working correctly.")
        print("You can now use it to analyze real GitHub Archive data.")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
