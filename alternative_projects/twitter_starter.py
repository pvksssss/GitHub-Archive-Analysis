#!/usr/bin/env python3
"""
Twitter Sentiment Analysis - Starter Template
Phân tích cảm xúc Twitter - Mẫu khởi đầu

This is a starter template for analyzing Twitter data - a student-friendly 
alternative to GitHub Archive Analysis that requires much less resources.

Đây là mẫu khởi đầu để phân tích dữ liệu Twitter - một lựa chọn thay thế
phù hợp với sinh viên, yêu cầu ít tài nguyên hơn nhiều so với GitHub Archive.

Requirements:
    pip install tweepy pandas textblob matplotlib
    
Note: You need Twitter API credentials (free at developer.twitter.com)
"""

import pandas as pd
from datetime import datetime, timedelta
import json

# Uncomment when you have API credentials
# import tweepy
# from textblob import TextBlob


class TwitterAnalyzer:
    """Simple Twitter data analyzer for students."""
    
    def __init__(self, api_key=None, api_secret=None):
        """Initialize Twitter API connection.
        
        Get free API keys from: https://developer.twitter.com/
        """
        self.api_key = api_key
        self.api_secret = api_secret
        # Uncomment when you have credentials:
        # auth = tweepy.OAuthHandler(api_key, api_secret)
        # self.api = tweepy.API(auth)
    
    def search_tweets(self, query, count=100):
        """Search for tweets about a topic.
        
        Args:
            query: Search term (e.g., "Python", "#BigData")
            count: Number of tweets to fetch (max 100 for free tier)
            
        Returns:
            List of tweet data
        """
        # Example structure - replace with actual API call
        tweets = []
        
        # Uncomment when you have API access:
        # for tweet in tweepy.Cursor(self.api.search_tweets, 
        #                            q=query, 
        #                            lang="en",
        #                            count=count).items(count):
        #     tweets.append({
        #         'text': tweet.text,
        #         'created_at': tweet.created_at,
        #         'user': tweet.user.screen_name,
        #         'likes': tweet.favorite_count,
        #         'retweets': tweet.retweet_count
        #     })
        
        return tweets
    
    def analyze_sentiment(self, tweets):
        """Analyze sentiment of tweets.
        
        Args:
            tweets: List of tweet dictionaries
            
        Returns:
            DataFrame with sentiment analysis
        """
        df = pd.DataFrame(tweets)
        
        # Uncomment for sentiment analysis:
        # df['sentiment'] = df['text'].apply(
        #     lambda x: TextBlob(x).sentiment.polarity
        # )
        # df['sentiment_label'] = df['sentiment'].apply(
        #     lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral')
        # )
        
        return df
    
    def get_statistics(self, df):
        """Get basic statistics from tweet data.
        
        Args:
            df: DataFrame with tweet data
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_tweets': len(df),
            'total_likes': df['likes'].sum() if 'likes' in df else 0,
            'total_retweets': df['retweets'].sum() if 'retweets' in df else 0,
            'avg_likes': df['likes'].mean() if 'likes' in df else 0,
            'avg_retweets': df['retweets'].mean() if 'retweets' in df else 0,
        }
        
        # if 'sentiment_label' in df:
        #     stats['sentiment_distribution'] = df['sentiment_label'].value_counts().to_dict()
        
        return stats


def example_with_sample_data():
    """Example using sample data (no API needed)."""
    
    print("="*60)
    print("Twitter Analysis - Sample Data Example")
    print("="*60)
    
    # Sample data for demonstration
    sample_tweets = [
        {
            'text': 'I love learning Python! #BigData',
            'created_at': datetime.now(),
            'user': 'user1',
            'likes': 10,
            'retweets': 5
        },
        {
            'text': 'Data analysis is difficult but rewarding',
            'created_at': datetime.now(),
            'user': 'user2',
            'likes': 15,
            'retweets': 3
        },
        {
            'text': 'Working on my BigData project today!',
            'created_at': datetime.now(),
            'user': 'user3',
            'likes': 20,
            'retweets': 8
        }
    ]
    
    # Create analyzer
    analyzer = TwitterAnalyzer()
    
    # Analyze sample data
    df = pd.DataFrame(sample_tweets)
    
    print(f"\nAnalyzed {len(df)} tweets")
    print("\nSample tweets:")
    print(df[['user', 'text', 'likes', 'retweets']].head())
    
    # Get statistics
    stats = analyzer.get_statistics(df)
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Save to CSV
    output_file = "sample_twitter_analysis.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✓ Results saved to {output_file}")


def main():
    """Main function with instructions."""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║          Twitter Sentiment Analysis - Starter Guide          ║
╚══════════════════════════════════════════════════════════════╝

This is a STUDENT-FRIENDLY alternative to GitHub Archive Analysis.

✅ ADVANTAGES:
  • Much smaller data (MB instead of GB)
  • Free API access available
  • Quick to collect and analyze
  • Interesting and relevant topics
  
📋 STEPS TO GET STARTED:

1. Get Twitter API credentials (FREE):
   → Go to: https://developer.twitter.com/
   → Sign up for a developer account
   → Create an app and get API keys
   
2. Install required packages:
   pip install tweepy pandas textblob matplotlib
   
3. Modify this script with your API credentials

4. Choose a topic to analyze:
   • "#Python" - Python programming discussions
   • "#BigData" - BigData conversations
   • "#COVID19" - COVID-19 discussions
   • Any hashtag or keyword you're interested in!

5. Collect 100-1000 tweets (takes 1-5 minutes)

6. Analyze sentiment, engagement, trends

📊 TYPICAL DATA SIZE:
  • 100 tweets = ~0.5 MB
  • 1000 tweets = ~5 MB
  • 10000 tweets = ~50 MB
  → Much smaller than GitHub Archive (10-30 GB)!

💡 ANALYSIS IDEAS:
  • Sentiment over time
  • Most engaging tweets
  • User activity patterns
  • Hashtag trends
  • Topic modeling

🎯 PERFECT FOR:
  • Students with limited resources
  • Quick BigData projects (2-3 weeks)
  • Learning data analysis basics
  • Creating visualizations

Run the example with sample data:
    python twitter_starter.py
    """)
    
    # Run example with sample data
    response = input("\nRun example with sample data? (y/n): ").lower()
    if response == 'y':
        example_with_sample_data()
    else:
        print("\nTo use this template:")
        print("1. Get Twitter API credentials")
        print("2. Uncomment the API-related code")
        print("3. Add your credentials")
        print("4. Run your analysis!")


if __name__ == "__main__":
    main()
