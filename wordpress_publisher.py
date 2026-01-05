"""
WordPress REST API Publisher
"""

import requests
import base64
from post_tracker import PostTracker
from image_finder import ImageFinder
from config import WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD, BLOG_CATEGORY_ID, AUTHOR_ID, POST_STATUS


class WordPressPublisher:
    """Publishes blog posts to WordPress via REST API"""
    
    def __init__(self):
        if not WORDPRESS_URL:
            raise ValueError("WORDPRESS_URL not set in config")
        if not WORDPRESS_USERNAME or not WORDPRESS_APP_PASSWORD:
            raise ValueError("WordPress credentials not set. Please set WORDPRESS_USERNAME and WORDPRESS_APP_PASSWORD")
        
        self.base_url = WORDPRESS_URL.rstrip('/')
        # Try standard REST API path first, fallback to query string format
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        self.api_url_alt = f"{self.base_url}/?rest_route=/wp/v2"
        self.username = WORDPRESS_USERNAME
        self.app_password = WORDPRESS_APP_PASSWORD
        
        # Create authentication header
        credentials = f"{self.username}:{self.app_password}"
        token = base64.b64encode(credentials.encode()).decode('utf-8')
        self.headers = {
            'Authorization': f'Basic {token}',
            'Content-Type': 'application/json'
        }
        
        # Detect which API URL works
        self._detect_api_url()
        
        # Initialize post tracker
        self.post_tracker = PostTracker()
        
        # Initialize image finder
        self.image_finder = ImageFinder()
        
        # Cache category IDs
        self._category_cache = {}
        self._load_category_ids()
    
    def _detect_api_url(self):
        """Detect which REST API URL format works"""
        # Try standard format first
        try:
            response = requests.get(f"{self.api_url}/", headers=self.headers, timeout=5)
            if response.status_code == 200:
                return  # Standard format works
        except:
            pass
        
        # Try alternative format
        try:
            response = requests.get(f"{self.api_url_alt}/", headers=self.headers, timeout=5)
            if response.status_code == 200:
                self.api_url = self.api_url_alt
                print(f"Using alternative REST API path: {self.api_url}")
                return
        except:
            pass
        
        # If both fail, keep standard and let error handling deal with it
        print(f"Warning: Could not verify REST API endpoint. Using: {self.api_url}")
    
    def _load_category_ids(self):
        """Load category IDs for the 5 looksmaxing categories"""
        category_names = [
            "Facial Aesthetics",
            "Body Aesthetics",
            "Lifestyle",
            "Grooming",
            "Surgery"
        ]
        
        try:
            categories = self.get_categories()
            for cat in categories:
                cat_name = cat.get('name', '')
                if cat_name in category_names:
                    self._category_cache[cat_name] = cat.get('id')
        except Exception as e:
            print(f"Warning: Could not load category IDs: {e}")
    
    def get_category_id(self, category_name):
        """Get category ID by name, create if doesn't exist"""
        if category_name in self._category_cache:
            return self._category_cache[category_name]
        
        # Try to find it
        try:
            categories = self.get_categories()
            for cat in categories:
                if cat.get('name', '').lower() == category_name.lower():
                    cat_id = cat.get('id')
                    self._category_cache[category_name] = cat_id
                    return cat_id
        except:
            pass
        
        # Create if doesn't exist
        category_descriptions = {
            "Facial Aesthetics": "Comprehensive guides on facial enhancement, jawline development, mewing, and facial symmetry optimization.",
            "Body Aesthetics": "Physique development, posture correction, height optimization, and body composition strategies.",
            "Lifestyle": "Sleep optimization, diet for aesthetics, supplementation, hormone optimization, and recovery strategies.",
            "Grooming": "Hair styling, skincare routines, fashion sense, fragrance, dental care, and personal grooming tips.",
            "Surgery": "Cosmetic surgery, orthodontics, advanced procedures, and surgical enhancement options."
        }
        
        description = category_descriptions.get(category_name, "")
        cat_id = self.create_category(category_name, description=description)
        if cat_id:
            self._category_cache[category_name] = cat_id
        return cat_id
    
    def test_connection(self):
        """Test WordPress API connection"""
        try:
            response = requests.get(
                f"{self.api_url}/users/me",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            user_data = response.json()
            print(f"✓ Connected to WordPress as: {user_data.get('name', 'Unknown')}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def get_categories(self):
        """Get available categories"""
        try:
            response = requests.get(
                f"{self.api_url}/categories",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []
    
    def create_category(self, name, slug=None, description=""):
        """Create a category if it doesn't exist, return category ID"""
        try:
            # Generate slug if not provided
            if not slug:
                slug = name.lower().replace(' ', '-').replace('_', '-')
            
            # Check if category exists
            response = requests.get(
                f"{self.api_url}/categories",
                params={"search": name, "per_page": 1},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            categories = response.json()
            
            # Check by name (case-insensitive)
            for cat in categories:
                if cat.get('name', '').lower() == name.lower():
                    return cat['id']
            
            # Create new category
            category_data = {
                "name": name,
                "slug": slug,
            }
            if description:
                category_data["description"] = description
            
            response = requests.post(
                f"{self.api_url}/categories",
                headers=self.headers,
                json=category_data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()['id']
            
        except Exception as e:
            print(f"Error creating category '{name}': {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"  Error details: {error_data}")
                except:
                    print(f"  Response: {e.response.text}")
            return None
    
    def create_tag(self, tag_name):
        """Create a tag if it doesn't exist, return tag ID"""
        try:
            # Check if tag exists
            response = requests.get(
                f"{self.api_url}/tags",
                params={"search": tag_name, "per_page": 1},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            tags = response.json()
            
            if tags and tags[0].get('name', '').lower() == tag_name.lower():
                return tags[0]['id']
            
            # Create new tag
            response = requests.post(
                f"{self.api_url}/tags",
                headers=self.headers,
                json={"name": tag_name},
                timeout=10
            )
            response.raise_for_status()
            return response.json()['id']
            
        except Exception as e:
            print(f"Error creating tag '{tag_name}': {e}")
            return None
    
    def upload_media(self, image_data, filename, title=""):
        """Upload image to WordPress media library, return media ID"""
        try:
            # WordPress media upload requires multipart/form-data
            files = {
                'file': (filename, image_data, 'image/jpeg')
            }
            
            data = {}
            if title:
                data['title'] = title
            
            # Use different headers for file upload
            upload_headers = {
                'Authorization': self.headers['Authorization']
                # Don't set Content-Type - let requests set it with boundary
            }
            
            response = requests.post(
                f"{self.api_url}/media",
                headers=upload_headers,
                files=files,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            media_data = response.json()
            media_id = media_data.get('id')
            print(f"  ✓ Uploaded thumbnail: {filename} (Media ID: {media_id})")
            return media_id
            
        except Exception as e:
            print(f"  ⚠ Error uploading thumbnail: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"    Error details: {error_data}")
                except:
                    print(f"    Response: {e.response.text[:200]}")
            return None
    
    def set_featured_image(self, post_id, media_id):
        """Set featured image for a post"""
        try:
            response = requests.post(
                f"{self.api_url}/posts/{post_id}",
                headers=self.headers,
                json={"featured_media": media_id},
                timeout=10
            )
            response.raise_for_status()
            print(f"  ✓ Set featured image (Media ID: {media_id})")
            return True
        except Exception as e:
            print(f"  ⚠ Error setting featured image: {e}")
            return False
    
    def publish_post(self, post_data):
        """
        Publish a blog post to WordPress
        
        Args:
            post_data: Dict with keys: title, content, excerpt, tags, topic
        
        Returns:
            Post ID if successful, None otherwise
        """
        try:
            # Validate content before publishing
            content = post_data.get('content', '').strip()
            title = post_data.get('title', '').strip()
            
            if not content or len(content) < 100:
                error_msg = f"Content is empty or too short ({len(content)} chars). Cannot publish."
                print(f"✗ {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
            
            if not title:
                error_msg = "Title is empty. Cannot publish."
                print(f"✗ {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
            
            # Prepare tags - create/get tag IDs
            tag_ids = []
            for tag_name in post_data.get('tags', []):
                tag_id = self.create_tag(tag_name)
                if tag_id:
                    tag_ids.append(tag_id)
            
            # Determine category ID
            category_name = post_data.get('category', 'Lifestyle')  # Default to Lifestyle
            category_id = self.get_category_id(category_name)
            
            if not category_id:
                print(f"⚠ Warning: Could not find/create category '{category_name}', using default category")
                category_id = BLOG_CATEGORY_ID
            
            # Prepare post payload
            post_payload = {
                "title": title,
                "content": content,
                "excerpt": post_data.get('excerpt', ''),
                "status": POST_STATUS,
                "categories": [category_id],
                "tags": tag_ids,
                "author": AUTHOR_ID
            }
            
            print(f"  Category: {category_name} (ID: {category_id})")
            
            # Create post
            print(f"Publishing post: {title}")
            response = requests.post(
                f"{self.api_url}/posts",
                headers=self.headers,
                json=post_payload,
                timeout=30
            )
            response.raise_for_status()
            
            created_post = response.json()
            post_id = created_post['id']
            post_url = created_post.get('link', f"{self.base_url}/?p={post_id}")
            
            # Find and upload thumbnail
            print(f"  Finding thumbnail...")
            category_name = post_data.get('category', 'Lifestyle')
            topic = post_data.get('topic', '')
            title = post_data.get('title', '')
            
            try:
                # Find image URL
                image_url = self.image_finder.find_image_url(
                    title=title,
                    topic=topic,
                    category=category_name
                )
                
                if image_url:
                    # Download image
                    image_data, filename = self.image_finder.download_image(image_url)
                    
                    if image_data:
                        # Upload to WordPress
                        media_id = self.upload_media(
                            image_data=image_data,
                            filename=filename,
                            title=f"Featured image for: {title}"
                        )
                        
                        if media_id:
                            # Set as featured image
                            self.set_featured_image(post_id, media_id)
                    else:
                        print(f"  ⚠ Could not download thumbnail from {image_url}")
                else:
                    print(f"  ⚠ Could not find thumbnail URL")
            except Exception as e:
                print(f"  ⚠ Error processing thumbnail: {e}")
                # Continue without thumbnail - post is already published
            
            # Track the published post
            self.post_tracker.add_post(
                post_id=post_id,
                title=post_data['title'],
                url=post_url,
                topic=post_data.get('topic', 'auto-selected'),
                tags=post_data.get('tags', [])
            )
            
            print(f"✓ Post published successfully!")
            print(f"  Post ID: {post_id}")
            print(f"  URL: {post_url}")
            print(f"  Status: {created_post.get('status', 'unknown')}")
            
            return {
                "success": True,
                "post_id": post_id,
                "url": post_url,
                "status": created_post.get('status')
            }
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error publishing post: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"  Error details: {error_data}")
                except:
                    print(f"  Response: {e.response.text}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_post(self, post_id, force=True):
        """Delete a WordPress post"""
        try:
            response = requests.delete(
                f"{self.api_url}/posts/{post_id}",
                headers=self.headers,
                params={"force": force},
                timeout=10
            )
            response.raise_for_status()
            print(f"✓ Post {post_id} deleted successfully")
            return True
        except Exception as e:
            print(f"✗ Error deleting post {post_id}: {e}")
            return False
    
    def delete_all_posts(self):
        """Delete all posts from WordPress"""
        try:
            # Get all posts
            response = requests.get(
                f"{self.api_url}/posts",
                headers=self.headers,
                params={"per_page": 100, "status": "any"},
                timeout=30
            )
            response.raise_for_status()
            posts = response.json()
            
            print(f"Found {len(posts)} posts to delete")
            
            deleted_count = 0
            for post in posts:
                post_id = post.get('id')
                post_title = post.get('title', {}).get('rendered', 'Unknown')
                if self.delete_post(post_id):
                    deleted_count += 1
                    print(f"  Deleted: {post_title}")
            
            print(f"\n✓ Deleted {deleted_count} out of {len(posts)} posts")
            return deleted_count
            
        except Exception as e:
            print(f"✗ Error deleting posts: {e}")
            return 0
    
    def update_post(self, post_id, post_data):
        """Update an existing post"""
        try:
            post_payload = {
                "title": post_data.get('title'),
                "content": post_data.get('content'),
                "excerpt": post_data.get('excerpt', ''),
            }
            
            # Remove None values
            post_payload = {k: v for k, v in post_payload.items() if v is not None}
            
            response = requests.post(
                f"{self.api_url}/posts/{post_id}",
                headers=self.headers,
                json=post_payload,
                timeout=30
            )
            response.raise_for_status()
            
            print(f"✓ Post {post_id} updated successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error updating post: {e}")
            return False

