# GitHub Archive Analysis

A comprehensive Python toolkit for downloading, analyzing, and visualizing GitHub Archive data. This project provides tools to work with the public GitHub timeline data, which records all public GitHub events including commits, pull requests, issues, and more.

> 🚀 **New to this project?** Check out the [Quick Start Guide](QUICKSTART.md) to get up and running in minutes!

## About GitHub Archive

[GitHub Archive](https://www.gharchive.org/) is a project to record the public GitHub timeline, archive it, and make it easily accessible for further analysis. GitHub provides 15+ event types, which range from new commits and fork events, to opening new tickets, commenting, and adding members to a project.

## Features

- 📥 **Download GitHub Archive data** - Easily download hourly archives for any date or date range
- 📊 **Analyze events** - Get statistics and insights about GitHub events, repositories, and users
- 🔍 **BigQuery integration** - Examples and utilities for querying data directly from Google BigQuery
- 📈 **Event type analysis** - Detailed breakdown of different event types (pushes, issues, PRs, etc.)
- 💾 **Export results** - Save analysis results to JSON for further processing

## Quick Links

- 📖 [Quick Start Guide](QUICKSTART.md) - Get started in minutes
- 💡 [Examples](examples/) - Ready-to-run example scripts
- 🤝 [Contributing](CONTRIBUTING.md) - How to contribute to this project
- 🧪 [Tests](test_functionality.py) - Run tests to verify installation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pvksssss/GitHub-Archive-Analysis.git
cd GitHub-Archive-Analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Download GitHub Archive Data

Download data using the `download_gharchive.py` script:

```bash
# Download a specific hour
python download_gharchive.py --date 2015-01-01 --hour 15

# Download all hours for a specific day
python download_gharchive.py --date 2015-01-01

# Download a date range
python download_gharchive.py --start-date 2015-01-01 --end-date 2015-01-05

# Specify custom output directory
python download_gharchive.py --date 2015-01-01 --output-dir my_data
```

Data is downloaded from `https://data.gharchive.org/` in gzipped JSON format. Each line in the uncompressed file is a JSON object representing a GitHub event.

### 2. Analyze Events

Analyze downloaded data using the `analyze_events.py` script:

```bash
# Analyze a single file
python analyze_events.py --file data/2015-01-01-15.json.gz

# Analyze all files in a directory
python analyze_events.py --dir data

# Filter by specific event type
python analyze_events.py --dir data --event-type PushEvent

# Show top 20 items instead of default 10
python analyze_events.py --dir data --top 20

# Export results to JSON
python analyze_events.py --dir data --output results.json
```

The analyzer provides:
- Total event counts
- Distribution of event types
- Most active repositories
- Most active users
- Detailed analysis for specific event types (PushEvent, IssuesEvent, PullRequestEvent)

### 3. BigQuery Integration

For large-scale analysis, use Google BigQuery to query the entire GitHub Archive dataset:

```python
from bigquery_examples import GHArchiveBigQuery

# Initialize BigQuery client
bq = GHArchiveBigQuery(project_id="your-project-id")

# Count events by type for a specific date
events = bq.count_events_by_type("20190101")
print(events)

# Get top active repositories
repos = bq.top_active_repos("20190101", limit=10)
print(repos)

# Get programming language statistics
langs = bq.language_statistics("20190101")
print(langs)
```

View example queries:
```bash
python bigquery_examples.py
```

## GitHub Event Types

The following event types are available in GitHub Archive:

- **PushEvent** - Code pushed to a repository
- **PullRequestEvent** - Pull request opened, closed, or merged
- **IssuesEvent** - Issue opened, closed, or reopened
- **IssueCommentEvent** - Comment added to an issue
- **WatchEvent** - Repository starred
- **ForkEvent** - Repository forked
- **CreateEvent** - Branch or tag created
- **DeleteEvent** - Branch or tag deleted
- **PullRequestReviewCommentEvent** - Comment on pull request diff
- **CommitCommentEvent** - Comment on a commit
- **ReleaseEvent** - Release published
- **PublicEvent** - Repository made public
- **MemberEvent** - Collaborator added
- **GollumEvent** - Wiki page updated

## Data Structure

Each event in the GitHub Archive has the following structure:

```json
{
  "id": "event_id",
  "type": "PushEvent",
  "actor": {
    "id": 123456,
    "login": "username",
    "display_login": "username",
    "gravatar_id": "",
    "url": "https://api.github.com/users/username",
    "avatar_url": "https://avatars.githubusercontent.com/u/123456?"
  },
  "repo": {
    "id": 789012,
    "name": "owner/repository",
    "url": "https://api.github.com/repos/owner/repository"
  },
  "payload": {
    // Event-specific data (varies by event type)
  },
  "public": true,
  "created_at": "2015-01-01T15:00:00Z"
}
```

## BigQuery Dataset Information

The GitHub Archive is available as a public dataset on Google BigQuery:

- **Dataset**: `githubarchive`
- **Tables**:
  - `year.*` - Annual tables (e.g., `githubarchive.year.2015`)
  - `month.*` - Monthly tables (e.g., `githubarchive.month.201501`)
  - `day.*` - Daily tables (e.g., `githubarchive.day.20150101`)

### Example BigQuery Queries

Count events by type for a specific day:
```sql
SELECT 
    type,
    COUNT(*) as count
FROM `githubarchive.day.20190101`
GROUP BY type
ORDER BY count DESC;
```

Find most active repositories:
```sql
SELECT 
    repo.name,
    COUNT(*) as event_count
FROM `githubarchive.day.20190101`
GROUP BY repo.name
ORDER BY event_count DESC
LIMIT 10;
```

Count push events in a date range:
```sql
SELECT COUNT(*) 
FROM `githubarchive.day.2015*`
WHERE 
    type = 'PushEvent'
    AND (_TABLE_SUFFIX BETWEEN '0101' AND '0105');
```

## Project Structure

```
GitHub-Archive-Analysis/
├── download_gharchive.py    # Download GitHub Archive data
├── analyze_events.py        # Analyze downloaded events
├── bigquery_examples.py     # BigQuery integration and examples
├── test_functionality.py    # Test suite with mock data
├── requirements.txt         # Python dependencies
├── README.md               # Complete documentation (this file)
├── QUICKSTART.md           # Quick start guide for beginners
├── CONTRIBUTING.md         # Contribution guidelines
├── .gitignore             # Git ignore rules
├── examples/              # Example scripts
│   ├── README.md          # Examples documentation
│   ├── example1_basic_analysis.py
│   ├── example2_event_type_focus.py
│   └── example3_compare_days.py
└── data/                  # Downloaded data (not tracked in git)
```

## Requirements

- Python 3.7+
- requests
- google-cloud-bigquery (for BigQuery integration)
- pandas (for data analysis)
- python-dateutil

## Notes

- Data archives are available starting from February 12, 2011
- Archives from 2/12/2011 to 12/31/2014 use the deprecated Timeline API
- Archives from 1/1/2015 onwards use the Events API
- BigQuery provides 1 TB of data processing per month for free
- Downloaded data files are automatically excluded from git (see `.gitignore`)

## Resources

- [GitHub Archive Website](https://www.gharchive.org/)
- [GitHub Events API Documentation](https://docs.github.com/en/rest/activity/events)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [GitHub Archive on BigQuery](https://console.cloud.google.com/marketplace/product/github/github-repos)

## Use Cases

This toolkit can be used for various analyses:

- 📊 Track programming language trends
- 👥 Identify most active developers and organizations
- 🔍 Study open source contribution patterns
- 📈 Analyze repository growth over time
- 🐛 Research issue and PR management practices
## Getting Started

1. **First time here?** → Read the [Quick Start Guide](QUICKSTART.md)
2. **Want to see examples?** → Check out the [examples directory](examples/)
3. **Ready to contribute?** → See [Contributing Guidelines](CONTRIBUTING.md)
4. **Need help?** → Open an issue or discussion

## Use Cases

This toolkit can be used for various analyses:

- 📊 Track programming language trends
- 👥 Identify most active developers and organizations
- 🔍 Study open source contribution patterns
- 📈 Analyze repository growth over time
- 🐛 Research issue and PR management practices
- 🌍 Geographical distribution of contributions
- ⏰ Time-based activity patterns

## License

This project is open source and available for educational and research purposes.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## Acknowledgments

- [GitHub Archive](https://www.gharchive.org/) by Ilya Grigorik
- GitHub API for providing public event data
- Google BigQuery for hosting the public dataset

---

Made with ❤️ for BigData analysis and open source research