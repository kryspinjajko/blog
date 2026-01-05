"""
Main automation script
"""

import sys
import time
import schedule
from datetime import datetime
from blog_generator import BlogPostGenerator
from wordpress_publisher import WordPressPublisher
from config import POSTS_PER_DAY, POST_TIME


class AutoPublisher:
    """Main automation class for generating and publishing blog posts"""
    
    def __init__(self):
        print("=" * 60)
        print("Looksmaxing Blog Auto-Publisher")
        print("=" * 60)
        
        try:
            self.generator = BlogPostGenerator()
            print("✓ Blog generator initialized")
        except Exception as e:
            print(f"✗ Failed to initialize blog generator: {e}")
            sys.exit(1)
        
        try:
            self.publisher = WordPressPublisher()
            print("✓ WordPress publisher initialized")
        except Exception as e:
            print(f"✗ Failed to initialize WordPress publisher: {e}")
            sys.exit(1)
    
    def generate_and_publish(self, topic=None):
        """Generate a blog post and publish it"""
        print("\n" + "=" * 60)
        print(f"Starting blog post generation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # Generate post
            post_data = self.generator.generate_full_post(topic)
            
            # Publish to WordPress
            result = self.publisher.publish_post(post_data)
            
            if result.get('success'):
                print("\n✓ Blog post published successfully!")
                print(f"  Title: {post_data['title']}")
                print(f"  URL: {result.get('url', 'N/A')}")
                return True
            else:
                print(f"\n✗ Failed to publish blog post: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"\n✗ Error during generation/publishing: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_scheduled(self):
        """Run the scheduler"""
        print(f"\nScheduling {POSTS_PER_DAY} post(s) per day at {POST_TIME}")
        
        # Schedule posts
        for i in range(POSTS_PER_DAY):
            schedule.every().day.at(POST_TIME).do(self.generate_and_publish)
        
        print("\nScheduler started. Waiting for scheduled times...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\nScheduler stopped by user")
    
    def run_once(self, topic=None):
        """Generate and publish a single post immediately"""
        return self.generate_and_publish(topic)
    
    def run_loop(self, interval_hours=24, topic=None):
        """Run in continuous loop, generating posts at specified intervals"""
        print(f"\nStarting continuous loop mode")
        print(f"Will generate and publish posts every {interval_hours} hours")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                success = self.generate_and_publish(topic)
                
                if success:
                    print(f"\n✓ Post published. Waiting {interval_hours} hours until next post...")
                else:
                    print(f"\n✗ Post failed. Waiting {interval_hours} hours before retry...")
                
                # Wait for specified interval (convert hours to seconds)
                wait_seconds = interval_hours * 3600
                print(f"Next post in {interval_hours} hours ({wait_seconds} seconds)")
                
                time.sleep(wait_seconds)
                
        except KeyboardInterrupt:
            print("\n\nLoop stopped by user")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Looksmaxing Blog Auto-Publisher')
    parser.add_argument(
        '--mode',
        choices=['once', 'schedule', 'loop'],
        default='once',
        help='Run mode: "once" for single post, "schedule" for automated scheduling, "loop" for continuous loop'
    )
    parser.add_argument(
        '--interval',
        type=float,
        default=24.0,
        help='Interval in hours between posts (for loop mode, default: 24)'
    )
    parser.add_argument(
        '--topic',
        type=str,
        default=None,
        help='Specific topic for the blog post (optional)'
    )
    
    args = parser.parse_args()
    
    # Initialize publisher
    publisher = AutoPublisher()
    
    if args.mode == 'once':
        # Generate and publish once
        success = publisher.run_once(args.topic)
        sys.exit(0 if success else 1)
    elif args.mode == 'schedule':
        # Run scheduled
        publisher.run_scheduled()
    else:
        # Run in continuous loop
        publisher.run_loop(interval_hours=args.interval, topic=args.topic)


if __name__ == "__main__":
    main()

