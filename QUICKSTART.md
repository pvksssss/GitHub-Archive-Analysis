# Quick Start Guide

This guide will help you get started with GitHub Archive Analysis in just a few minutes.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Basic understanding of command line

## Installation (3 minutes)

1. **Clone the repository**
   ```bash
   git clone https://github.com/pvksssss/GitHub-Archive-Analysis.git
   cd GitHub-Archive-Analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python test_functionality.py
   ```
   
   You should see "✓ ALL TESTS PASSED!"

## Your First Analysis (5 minutes)

Let's download and analyze GitHub activity from January 1, 2015.

### Step 1: Download Data

Download data for a specific hour:
```bash
python download_gharchive.py --date 2015-01-01 --hour 15
```

This downloads about 10-20 MB of data into the `data/` directory.

### Step 2: Analyze the Data

Run basic analysis:
```bash
python analyze_events.py --file data/2015-01-01-15.json.gz
```

You'll see:
- Total number of events
- Distribution of event types
- Most active repositories
- Most active users
- Detailed breakdowns for common event types

### Step 3: Export Results

To save results for later use:
```bash
python analyze_events.py --file data/2015-01-01-15.json.gz --output results.json
```

## Common Use Cases

### 1. Analyze a Full Day

Download and analyze all 24 hours of a day:
```bash
# Download full day
python download_gharchive.py --date 2015-01-01

# Analyze all files
python analyze_events.py --dir data
```

### 2. Focus on Specific Event Types

Analyze only push events:
```bash
python analyze_events.py --dir data --event-type PushEvent
```

Other event types:
- `PullRequestEvent` - Pull requests
- `IssuesEvent` - Issues
- `WatchEvent` - Repository stars
- `ForkEvent` - Repository forks

### 3. Run Example Scripts

We provide ready-to-run examples:

```bash
# Basic analysis example
python examples/example1_basic_analysis.py

# Focus on push events
python examples/example2_event_type_focus.py

# Compare multiple days
python examples/example3_compare_days.py
```

## Tips for Success

1. **Start Small**: Begin with a single hour of data to understand the structure
2. **Use Filters**: Filter by event type to focus your analysis
3. **Export Results**: Save your analysis results to JSON for further processing
4. **Check File Sizes**: Each hour is typically 10-30 MB compressed
5. **Be Patient**: Downloading and analyzing can take time for large date ranges

## Next Steps

- Read the [full README](README.md) for complete documentation
- Explore the [examples directory](examples/) for more use cases
- Try [BigQuery integration](bigquery_examples.py) for large-scale analysis
- Create your own analysis scripts using the provided modules

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "No such file or directory" error
Make sure you're in the project root directory:
```bash
cd GitHub-Archive-Analysis
```

### BigQuery errors
BigQuery is optional. To use it:
```bash
pip install google-cloud-bigquery
```
Then set up authentication: https://cloud.google.com/docs/authentication

### Download fails
GitHub Archive data is large. Ensure you have:
- Stable internet connection
- Sufficient disk space (1 GB minimum recommended)

## Getting Help

If you encounter issues:
1. Check the error message carefully
2. Review the [README](README.md) documentation
3. Open an issue on GitHub with details about your problem

## What's Next?

Now that you're up and running, you can:
- Analyze trends in open source development
- Study programming language popularity
- Identify most active projects and contributors
- Research contribution patterns
- Build visualizations from the data
- Create your own research project

Happy analyzing! 🎉
