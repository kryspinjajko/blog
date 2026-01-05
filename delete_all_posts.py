"""
Delete all WordPress posts and clear published_posts.json
"""

import json
from wordpress_publisher import WordPressPublisher
from post_tracker import PostTracker


def main():
    print("=" * 60)
    print("Delete All WordPress Posts")
    print("=" * 60)
    
    # Initialize publisher
    try:
        publisher = WordPressPublisher()
        print("✓ WordPress publisher initialized\n")
    except Exception as e:
        print(f"✗ Failed to initialize WordPress publisher: {e}")
        return
    
    # Delete all posts from WordPress
    print("Deleting all posts from WordPress...")
    deleted_count = publisher.delete_all_posts()
    
    # Clear published_posts.json
    print("\nClearing published_posts.json...")
    tracker = PostTracker()
    tracker.posts = []
    tracker._save_posts()
    print("✓ published_posts.json cleared")
    
    print(f"\n{'='*60}")
    print(f"✓ Complete: Deleted {deleted_count} posts from WordPress")
    print(f"✓ Complete: Cleared published_posts.json")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

