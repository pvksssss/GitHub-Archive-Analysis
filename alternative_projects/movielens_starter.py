#!/usr/bin/env python3
"""
MovieLens Analysis - Starter Template
Phân tích dữ liệu phim MovieLens - Mẫu khởi đầu

This is a starter template for analyzing MovieLens dataset - a perfect 
student-friendly alternative that requires minimal resources.

Dataset: MovieLens 100K (5 MB)
Download: https://grouplens.org/datasets/movielens/100k/
"""

import pandas as pd
import numpy as np
from collections import Counter

# Optional: matplotlib for visualizations
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class MovieLensAnalyzer:
    """Analyze MovieLens dataset - perfect for students!"""
    
    def __init__(self, data_path='ml-100k'):
        """Initialize analyzer with dataset path.
        
        Args:
            data_path: Path to MovieLens 100K dataset folder
        """
        self.data_path = data_path
        self.ratings = None
        self.movies = None
        self.users = None
    
    def load_data(self):
        """Load MovieLens 100K dataset.
        
        Download from: https://grouplens.org/datasets/movielens/100k/
        """
        try:
            # Load ratings (u.data)
            self.ratings = pd.read_csv(
                f'{self.data_path}/u.data',
                sep='\t',
                names=['user_id', 'movie_id', 'rating', 'timestamp']
            )
            
            # Load movies (u.item)
            self.movies = pd.read_csv(
                f'{self.data_path}/u.item',
                sep='|',
                encoding='latin-1',
                names=['movie_id', 'title', 'release_date', 'video_release', 
                       'imdb_url'] + [f'genre_{i}' for i in range(19)]
            )
            
            # Load users (u.user)
            self.users = pd.read_csv(
                f'{self.data_path}/u.user',
                sep='|',
                names=['user_id', 'age', 'gender', 'occupation', 'zip_code']
            )
            
            print(f"✓ Loaded {len(self.ratings)} ratings")
            print(f"✓ Loaded {len(self.movies)} movies")
            print(f"✓ Loaded {len(self.users)} users")
            
            return True
            
        except FileNotFoundError:
            print("❌ Dataset not found!")
            print("\nPlease download MovieLens 100K:")
            print("1. Go to: https://grouplens.org/datasets/movielens/100k/")
            print("2. Download ml-100k.zip (5 MB)")
            print("3. Extract to current directory")
            return False
    
    def get_basic_stats(self):
        """Get basic statistics about the dataset."""
        
        if self.ratings is None:
            print("Please load data first!")
            return
        
        stats = {
            'total_ratings': len(self.ratings),
            'total_movies': len(self.movies),
            'total_users': len(self.users),
            'rating_range': f"{self.ratings['rating'].min()} - {self.ratings['rating'].max()}",
            'avg_rating': self.ratings['rating'].mean(),
            'ratings_per_user': len(self.ratings) / len(self.users),
            'ratings_per_movie': len(self.ratings) / len(self.movies),
        }
        
        print("\n" + "="*60)
        print("MOVIELENS DATASET STATISTICS")
        print("="*60)
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key:20s}: {value:.2f}")
            else:
                print(f"{key:20s}: {value}")
        
        return stats
    
    def top_rated_movies(self, min_ratings=50, top_n=10):
        """Get top rated movies (with minimum number of ratings).
        
        Args:
            min_ratings: Minimum number of ratings required
            top_n: Number of top movies to return
        """
        # Calculate average rating and count for each movie
        movie_stats = self.ratings.groupby('movie_id').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        
        movie_stats.columns = ['movie_id', 'avg_rating', 'rating_count']
        
        # Filter by minimum ratings
        popular_movies = movie_stats[movie_stats['rating_count'] >= min_ratings]
        
        # Sort by average rating
        top_movies = popular_movies.nlargest(top_n, 'avg_rating')
        
        # Merge with movie titles
        top_movies = top_movies.merge(
            self.movies[['movie_id', 'title']], 
            on='movie_id'
        )
        
        print(f"\n--- Top {top_n} Movies (min {min_ratings} ratings) ---")
        for idx, row in top_movies.iterrows():
            print(f"{row['title']:50s} | ⭐ {row['avg_rating']:.2f} ({int(row['rating_count'])} ratings)")
        
        return top_movies
    
    def most_rated_movies(self, top_n=10):
        """Get most rated movies."""
        
        movie_counts = self.ratings['movie_id'].value_counts().head(top_n)
        
        print(f"\n--- Top {top_n} Most Rated Movies ---")
        for movie_id, count in movie_counts.items():
            title = self.movies[self.movies['movie_id'] == movie_id]['title'].values[0]
            print(f"{title:50s} | {count} ratings")
    
    def rating_distribution(self):
        """Show distribution of ratings."""
        
        rating_counts = self.ratings['rating'].value_counts().sort_index()
        
        print("\n--- Rating Distribution ---")
        for rating, count in rating_counts.items():
            percentage = (count / len(self.ratings)) * 100
            bar = '█' * int(percentage / 2)
            print(f"{rating} stars: {bar} {percentage:.1f}% ({count})")
    
    def user_activity(self, top_n=10):
        """Analyze user activity."""
        
        user_counts = self.ratings['user_id'].value_counts().head(top_n)
        
        print(f"\n--- Top {top_n} Most Active Users ---")
        for user_id, count in user_counts.items():
            print(f"User {user_id:4d}: {count:4d} ratings")
        
        # Average ratings per user
        avg_ratings = len(self.ratings) / len(self.users)
        print(f"\nAverage ratings per user: {avg_ratings:.1f}")


def example_analysis():
    """Example analysis workflow."""
    
    print("="*60)
    print("MovieLens Analysis - Example Workflow")
    print("="*60)
    
    # Initialize analyzer
    analyzer = MovieLensAnalyzer('ml-100k')
    
    # Load data
    if not analyzer.load_data():
        return
    
    # Basic statistics
    analyzer.get_basic_stats()
    
    # Top rated movies
    analyzer.top_rated_movies(min_ratings=50, top_n=10)
    
    # Most rated movies
    analyzer.most_rated_movies(top_n=10)
    
    # Rating distribution
    analyzer.rating_distribution()
    
    # User activity
    analyzer.user_activity(top_n=10)


def main():
    """Main function with instructions."""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║          MovieLens Analysis - Student Guide                   ║
╚══════════════════════════════════════════════════════════════╝

Perfect student-friendly BigData project! 🎬

✅ ADVANTAGES:
  • Very small dataset (5 MB - MovieLens 100K)
  • Clean, structured data
  • No API needed - just download once
  • Fast analysis (seconds, not hours)
  • Well-documented dataset
  • Works on any laptop (2GB RAM is enough)

📋 QUICK START:

1. Download MovieLens 100K dataset:
   → https://grouplens.org/datasets/movielens/100k/
   → Click "ml-100k.zip" (5 MB)
   
2. Extract the zip file to current directory
   → You should have a folder named "ml-100k"
   
3. Install requirements:
   pip install pandas numpy matplotlib

4. Run this script:
   python movielens_starter.py

📊 DATASET INFO:
  • 100,000 ratings
  • 943 users
  • 1,682 movies
  • Released 1998
  • Perfect for learning!

💡 ANALYSIS IDEAS:
  • Top rated movies
  • Genre popularity trends
  • User rating patterns
  • Movie recommendation system
  • Rating prediction (Machine Learning)
  • User clustering
  • Genre preference by demographics

🎯 PROJECT TIMELINE:
  • Week 1: Data exploration, basic statistics
  • Week 2: Detailed analysis, visualizations
  • Week 3: Machine learning (optional)
  • Week 4: Report writing

⏱️ PROCESSING TIME:
  • Load data: < 1 second
  • Basic analysis: < 10 seconds
  • Complete analysis: < 1 minute
  → Much faster than GitHub Archive!

📝 REQUIRED RESOURCES:
  • Disk: 5 MB (dataset) + 50 MB (with code/results)
  • RAM: 2-4 GB
  • Time to analyze: Minutes
  → Perfect for students!
    """)
    
    response = input("\nRun example analysis? (requires ml-100k dataset) (y/n): ").lower()
    if response == 'y':
        example_analysis()
    else:
        print("\nTo use this template:")
        print("1. Download MovieLens 100K dataset")
        print("2. Extract to current directory")
        print("3. Run: python movielens_starter.py")


if __name__ == "__main__":
    main()
