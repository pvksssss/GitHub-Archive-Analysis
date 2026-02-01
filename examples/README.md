# GitHub Archive Analysis Examples

This directory contains example scripts demonstrating how to use the GitHub Archive Analysis toolkit.

## Examples

### Example 1: Basic Event Analysis
**File:** `example1_basic_analysis.py`

Downloads and analyzes GitHub Archive data for a single hour, showing:
- Total event counts
- Distribution of event types
- Most active repositories
- Most active users

**Run:**
```bash
python examples/example1_basic_analysis.py
```

### Example 2: Event Type Focus
**File:** `example2_event_type_focus.py`

Focuses on a specific event type (PushEvent) to analyze:
- Code push patterns
- Commit volumes
- Most active repositories for pushes
- Unique contributors

**Run:**
```bash
python examples/example2_event_type_focus.py
```

### Example 3: Comparing Multiple Days
**File:** `example3_compare_days.py`

Compares GitHub activity across multiple days:
- Total events per day
- Most common event types
- Day-over-day growth/decline
- Most active repositories across days

**Run:**
```bash
python examples/example3_compare_days.py
```

## Running Examples

All examples are self-contained and can be run directly:

```bash
# Run from project root
cd GitHub-Archive-Analysis
python examples/example1_basic_analysis.py
python examples/example2_event_type_focus.py
python examples/example3_compare_days.py
```

## What Each Example Teaches

### Example 1
- How to use `GHArchiveDownloader` to download data
- How to use `EventAnalyzer` for basic analysis
- How to export results to JSON

### Example 2
- How to filter events by type
- How to analyze specific event types in detail
- How to extract additional insights from event data

### Example 3
- How to compare data across multiple time periods
- How to aggregate statistics across multiple files
- How to identify trends over time

## Customization

You can modify these examples to:
- Change the dates being analyzed
- Focus on different event types
- Analyze longer time periods
- Add custom visualizations
- Export data in different formats

## Data Downloaded

Downloaded data will be stored in the `data/` directory (automatically created).
This directory is excluded from git via `.gitignore`.
