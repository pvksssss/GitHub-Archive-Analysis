"""
BigQuery Integration Examples for GitHub Archive Analysis

This module provides examples and utilities for querying GitHub Archive
data directly from Google BigQuery.

To use these examples:
1. Set up a Google Cloud project and enable BigQuery API
2. Install google-cloud-bigquery: pip install google-cloud-bigquery
3. Set up authentication: https://cloud.google.com/docs/authentication/getting-started
"""

from typing import List, Dict

try:
    from google.cloud import bigquery
    BIGQUERY_AVAILABLE = True
except ImportError:
    BIGQUERY_AVAILABLE = False
    bigquery = None


class GHArchiveBigQuery:
    """Query GitHub Archive data from BigQuery."""
    
    def __init__(self, project_id: str = None):
        """Initialize BigQuery client.
        
        Args:
            project_id: Google Cloud project ID. If None, uses default from environment.
        """
        if not BIGQUERY_AVAILABLE:
            raise ImportError(
                "google-cloud-bigquery is not installed. "
                "Install it with: pip install google-cloud-bigquery"
            )
        self.client = bigquery.Client(project=project_id)
    
    def query(self, sql: str) -> List[Dict]:
        """Execute a BigQuery SQL query.
        
        Args:
            sql: SQL query string
            
        Returns:
            List of result rows as dictionaries
        """
        query_job = self.client.query(sql)
        results = query_job.result()
        
        rows = []
        for row in results:
            rows.append(dict(row.items()))
        
        return rows
    
    def count_events_by_type(self, date: str) -> List[Dict]:
        """Count events by type for a specific date.
        
        Args:
            date: Date in YYYYMMDD format (e.g., '20190101')
            
        Returns:
            List of event types with counts
        """
        sql = f"""
        SELECT 
            type,
            COUNT(*) as count
        FROM `githubarchive.day.{date}`
        GROUP BY type
        ORDER BY count DESC
        """
        return self.query(sql)
    
    def count_issue_actions(self, date: str) -> List[Dict]:
        """Count issue actions (opened, closed, reopened) for a date.
        
        Args:
            date: Date in YYYYMMDD format
            
        Returns:
            List of issue actions with counts
        """
        sql = f"""
        SELECT 
            JSON_EXTRACT(payload, '$.action') as issue_status, 
            COUNT(*) as cnt 
        FROM (
            SELECT 
                type, 
                repo.name, 
                actor.login,
                JSON_EXTRACT(payload, '$.action') as event, 
                payload
            FROM `githubarchive.day.{date}`
            WHERE type = 'IssuesEvent'
        )
        GROUP BY issue_status
        ORDER BY cnt DESC
        """
        return self.query(sql)
    
    def count_push_events_range(self, start_suffix: str, end_suffix: str) -> int:
        """Count push events in a date range.
        
        Args:
            start_suffix: Start date suffix (e.g., '0101' for Jan 1)
            end_suffix: End date suffix (e.g., '0105' for Jan 5)
            
        Returns:
            Total count of push events
        """
        sql = f"""
        SELECT COUNT(*) as count
        FROM `githubarchive.day.2015*`
        WHERE 
            type = 'PushEvent'
            AND (_TABLE_SUFFIX BETWEEN '{start_suffix}' AND '{end_suffix}')
        """
        results = self.query(sql)
        return results[0]['count'] if results else 0
    
    def top_active_repos(self, date: str, limit: int = 10) -> List[Dict]:
        """Get most active repositories for a date.
        
        Args:
            date: Date in YYYYMMDD format
            limit: Number of top repos to return
            
        Returns:
            List of repositories with event counts
        """
        sql = f"""
        SELECT 
            repo.name as repo_name,
            COUNT(*) as event_count
        FROM `githubarchive.day.{date}`
        GROUP BY repo_name
        ORDER BY event_count DESC
        LIMIT {limit}
        """
        return self.query(sql)
    
    def top_contributors(self, date: str, limit: int = 10) -> List[Dict]:
        """Get most active contributors for a date.
        
        Args:
            date: Date in YYYYMMDD format
            limit: Number of top contributors to return
            
        Returns:
            List of contributors with event counts
        """
        sql = f"""
        SELECT 
            actor.login as username,
            COUNT(*) as event_count
        FROM `githubarchive.day.{date}`
        GROUP BY username
        ORDER BY event_count DESC
        LIMIT {limit}
        """
        return self.query(sql)
    
    def language_statistics(self, date: str) -> List[Dict]:
        """Get programming language statistics for a date.
        
        Args:
            date: Date in YYYYMMDD format
            
        Returns:
            List of languages with event counts
        """
        sql = f"""
        SELECT 
            JSON_EXTRACT_SCALAR(payload, '$.pull_request.base.repo.language') as language,
            COUNT(*) as count
        FROM `githubarchive.day.{date}`
        WHERE 
            type = 'PullRequestEvent'
            AND JSON_EXTRACT_SCALAR(payload, '$.pull_request.base.repo.language') IS NOT NULL
        GROUP BY language
        ORDER BY count DESC
        """
        return self.query(sql)


# Example queries as standalone functions
def example_queries():
    """Print example BigQuery queries for GitHub Archive."""
    
    queries = {
        "Count events by type for a specific day": """
        SELECT 
            type,
            COUNT(*) as count
        FROM `githubarchive.day.20190101`
        GROUP BY type
        ORDER BY count DESC;
        """,
        
        "Count issue actions (opened, closed, reopened)": """
        SELECT 
            JSON_EXTRACT(payload, '$.action') as issue_status, 
            COUNT(*) as cnt 
        FROM (
            SELECT 
                type, 
                repo.name, 
                actor.login,
                JSON_EXTRACT(payload, '$.action') as event, 
                payload
            FROM `githubarchive.day.20190101`
            WHERE type = 'IssuesEvent'
        )
        GROUP BY issue_status;
        """,
        
        "Count push events in date range (Jan 1-5)": """
        SELECT COUNT(*) 
        FROM `githubarchive.day.2015*`
        WHERE 
            type = 'PushEvent'
            AND (_TABLE_SUFFIX BETWEEN '0101' AND '0105');
        """,
        
        "Count watch events in month range (Jan-Oct 2014)": """
        SELECT COUNT(*) 
        FROM `githubarchive.month.2014*`
        WHERE 
            type = 'WatchEvent'
            AND (_TABLE_SUFFIX BETWEEN '01' AND '10');
        """,
        
        "Count fork events across years (2012-2014)": """
        SELECT COUNT(*) 
        FROM `githubarchive.year.20*`
        WHERE 
            type = 'ForkEvent'
            AND (_TABLE_SUFFIX BETWEEN '12' AND '14');
        """,
        
        "Top 10 most active repositories": """
        SELECT 
            repo.name,
            COUNT(*) as event_count
        FROM `githubarchive.day.20190101`
        GROUP BY repo.name
        ORDER BY event_count DESC
        LIMIT 10;
        """,
        
        "Top 10 most active users": """
        SELECT 
            actor.login,
            COUNT(*) as event_count
        FROM `githubarchive.day.20190101`
        GROUP BY actor.login
        ORDER BY event_count DESC
        LIMIT 10;
        """,
        
        "Programming language statistics from PRs": """
        SELECT 
            JSON_EXTRACT_SCALAR(payload, '$.pull_request.base.repo.language') as language,
            COUNT(*) as pr_count
        FROM `githubarchive.day.20190101`
        WHERE 
            type = 'PullRequestEvent'
            AND JSON_EXTRACT_SCALAR(payload, '$.pull_request.base.repo.language') IS NOT NULL
        GROUP BY language
        ORDER BY pr_count DESC
        LIMIT 20;
        """
    }
    
    for title, query in queries.items():
        print(f"\n{'='*60}")
        print(f"{title}")
        print('='*60)
        print(query)


if __name__ == "__main__":
    print("GitHub Archive BigQuery Examples")
    print("="*60)
    print("\nThese are example queries you can run on BigQuery.")
    print("To use them, you need to:")
    print("1. Set up a Google Cloud project")
    print("2. Enable BigQuery API")
    print("3. Set up authentication")
    print("\nFor more info, visit: https://cloud.google.com/bigquery/docs/quickstarts")
    
    example_queries()
