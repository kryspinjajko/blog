"""
Post Tracker - Tracks published posts for internal linking
"""

import json
import os
from datetime import datetime


class PostTracker:
    """Tracks published posts for internal linking"""
    
    def __init__(self, tracker_file="published_posts.json"):
        self.tracker_file = tracker_file
        self.posts = self._load_posts()
    
    def _load_posts(self):
        """Load published posts from file"""
        if os.path.exists(self.tracker_file):
            try:
                with open(self.tracker_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading post tracker: {e}")
                return []
        return []
    
    def _save_posts(self):
        """Save published posts to file"""
        try:
            with open(self.tracker_file, 'w', encoding='utf-8') as f:
                json.dump(self.posts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving post tracker: {e}")
    
    def add_post(self, post_id, title, url, topic, tags=None):
        """Add a new published post to tracker"""
        post_data = {
            "id": post_id,
            "title": title,
            "url": url,
            "topic": topic or "auto-selected",
            "tags": tags or [],
            "published_date": datetime.now().isoformat()
        }
        
        # Check if post already exists (by ID)
        existing_index = None
        for i, post in enumerate(self.posts):
            if post.get('id') == post_id:
                existing_index = i
                break
        
        if existing_index is not None:
            # Update existing post
            self.posts[existing_index] = post_data
        else:
            # Add new post
            self.posts.append(post_data)
        
        self._save_posts()
        print(f"✓ Post tracked: {title}")
    
    def get_relevant_posts(self, current_topic, current_title, max_posts=3):
        """Get relevant previous posts based on topic and title"""
        if not self.posts:
            return []
        
        relevant_posts = []
        current_topic_lower = (current_topic or "").lower()
        current_title_lower = current_title.lower()
        
        # Extract keywords from current topic and title
        current_keywords = set()
        if current_topic_lower:
            current_keywords.update(current_topic_lower.split())
        if current_title_lower:
            current_keywords.update(current_title_lower.split())
        
        # Score posts by relevance
        scored_posts = []
        for post in self.posts:
            # Skip the current post if it exists
            if post.get('title', '').lower() == current_title_lower:
                continue
            
            score = 0
            post_topic = post.get('topic', '').lower()
            post_title = post.get('title', '').lower()
            post_tags = [tag.lower() for tag in post.get('tags', [])]
            
            # Check topic match
            if current_topic_lower and current_topic_lower in post_topic:
                score += 10
            if current_topic_lower and post_topic in current_topic_lower:
                score += 10
            
            # Check keyword matches in title
            for keyword in current_keywords:
                if len(keyword) > 3:  # Only meaningful keywords
                    if keyword in post_title:
                        score += 5
                    if keyword in post_topic:
                        score += 3
            
            # Check tag matches
            for keyword in current_keywords:
                if len(keyword) > 3:
                    for tag in post_tags:
                        if keyword in tag or tag in keyword:
                            score += 2
            
            if score > 0:
                scored_posts.append((score, post))
        
        # Sort by score and return top posts
        scored_posts.sort(key=lambda x: x[0], reverse=True)
        relevant_posts = [post for _, post in scored_posts[:max_posts]]
        
        return relevant_posts
    
    def get_all_posts(self):
        """Get all tracked posts"""
        return self.posts
    
    def get_post_count(self):
        """Get total number of tracked posts"""
        return len(self.posts)

