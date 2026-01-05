"""
Image Finder - Finds and downloads relevant images for blog posts
Uses Pexels API first, then Unsplash, then fallback
"""

import requests
import re
from urllib.parse import quote
from config import PEXELS_API_KEY


class ImageFinder:
    """Finds relevant images for blog posts"""
    
    def __init__(self):
        # Pexels API
        self.pexels_api_key = PEXELS_API_KEY
        self.pexels_api_url = "https://api.pexels.com/v1"
        
        # Unsplash Source API - free, no authentication needed (fallback)
        self.unsplash_source = "https://source.unsplash.com"
        
        # Final fallback - use Unsplash direct image URLs (no API needed)
        self.placeholder_fallbacks = {
            "Facial Aesthetics": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&h=630&fit=crop",
            "Body Aesthetics": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1200&h=630&fit=crop",
            "Lifestyle": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1200&h=630&fit=crop",
            "Grooming": "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?w=1200&h=630&fit=crop",
            "Surgery": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1200&h=630&fit=crop"
        }
        self.default_fallback = "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1200&h=630&fit=crop"  # Generic fitness/health image
    
    def translate_looksmaxing_terms(self, text, category):
        """Translate looksmaxing-specific terms to specific, contextual, image-searchable terms"""
        if not text:
            return []
        
        text_lower = text.lower()
        translated_terms = []
        processed_text = text_lower
        
        # Context-aware translation mapping: looksmaxing term -> specific, contextual searchable terms
        # Keep context and make terms more specific to the actual topic
        translations = [
            # Multi-word looksmaxing terms (check these first) - very specific, contextual
            ("bonesmashing", ["strong jawline male", "defined jaw", "facial bone structure"]),
            ("jawline development", ["strong jawline male", "defined jaw", "facial structure development"]),
            ("facial symmetry", ["symmetric male face", "balanced facial features", "male portrait"]),
            ("mouth widening", ["wide smile male", "confident smile", "facial expression"]),
            ("eye area enhancement", ["attractive male eyes", "eye area", "facial features"]),
            ("nose optimization", ["male nose profile", "nose shape", "facial profile"]),
            ("physique development", ["athletic male body", "muscular physique", "fitness transformation male"]),
            ("posture correction", ["good posture male", "standing straight", "confident posture"]),
            ("height optimization", ["tall athletic male", "height advantage", "tall man"]),
            ("shoulder width", ["broad shoulders male", "athletic shoulders", "V-shaped physique"]),
            ("waist-to-hip ratio", ["athletic male body", "fitness physique", "muscular build"]),
            ("sleep optimization", ["healthy sleep", "sleeping well", "rest recovery"]),
            ("diet for aesthetics", ["healthy nutrition", "fitness diet", "athletic nutrition"]),
            ("hormone optimization", ["male health", "fitness wellness", "health optimization"]),
            ("stress management", ["relaxation techniques", "meditation wellness", "stress relief"]),
            ("hair styling", ["male hairstyle", "groomed hair", "professional haircut"]),
            ("skincare routine", ["male skincare", "face care routine", "grooming routine"]),
            ("fashion sense", ["male fashion style", "professional style", "well-dressed man"]),
            ("dental care", ["white teeth smile", "dental health", "perfect smile"]),
            ("cosmetic surgery", ["cosmetic procedure", "plastic surgery", "medical enhancement"]),
            ("hair transplants", ["hair restoration", "hair transplant procedure", "medical hair"]),
            ("filler procedures", ["cosmetic fillers", "facial enhancement", "medical aesthetics"]),
            ("jaw surgery", ["orthognathic surgery", "jaw correction", "facial surgery"]),
            
            # Single-word looksmaxing terms - very specific
            ("mewing", ["jawline exercise", "tongue posture technique", "facial development exercise"]),
            ("softmaxxing", ["male grooming routine", "skincare fitness", "lifestyle improvement"]),
            ("hardmaxxing", ["cosmetic surgery", "surgical enhancement", "medical procedure"]),
            ("mogging", ["attractive confident male", "fitness model", "athletic attractive man"]),
            ("chad", ["attractive athletic male", "confident portrait", "ideal male physique"]),
            ("looksmaxing", ["male self improvement", "fitness transformation", "aesthetic enhancement male"]),
            ("looksmax", ["male improvement", "fitness aesthetics", "self enhancement"]),
            ("maxxing", ["improvement", "enhancement"]),
            ("maxxed", ["improved", "enhanced"]),
            ("supplementation", ["health supplements", "fitness vitamins", "nutrition supplements"]),
            ("orthodontics", ["dental braces", "teeth alignment", "orthodontic treatment"]),
        ]
        
        # Category-specific context to add
        category_context = {
            "Facial Aesthetics": ["male", "facial", "face", "portrait"],
            "Body Aesthetics": ["athletic", "fitness", "muscular", "male"],
            "Lifestyle": ["health", "wellness", "lifestyle", "routine"],
            "Grooming": ["male", "grooming", "style", "fashion"],
            "Surgery": ["medical", "surgery", "procedure", "cosmetic"]
        }
        
        # Process multi-word terms first, then single words
        for looksmax_term, generic_terms in translations:
            if looksmax_term in processed_text:
                # Add specific, contextual terms
                translated_terms.extend(generic_terms[:2])  # Add first 2 specific terms
                # Remove the looksmax term from processed text to avoid double matching
                processed_text = processed_text.replace(looksmax_term, " ")
        
        # Extract remaining meaningful words that are already generic and searchable
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "your", "you", "how", "what", "when", "where", "why", "this", "that", "these", "those", "proven", "techniques", "appliances", "guide", "complete", "ultimate", "improve", "enhance", "transform", "achieve", "become", "with", "these", "and"}
        
        # Extract meaningful words from remaining text
        remaining_words = re.findall(r'\b\w+\b', processed_text)
        meaningful_words = []
        for word in remaining_words:
            if word not in common_words and len(word) > 3:
                # Keep words that are already generic and searchable
                searchable_words = ["fitness", "health", "facial", "face", "body", "muscle", "athletic", "grooming", "style", "fashion", "hair", "skincare", "dental", "medical", "surgery", "posture", "diet", "nutrition", "sleep", "wellness", "lifestyle", "portrait", "jaw", "chin", "eyes", "nose", "mouth", "teeth", "shoulders", "back", "spine", "male", "man", "attractive", "confident", "strong", "defined", "symmetric", "wide", "broad", "tall", "white", "good", "healthy"]
                if word in searchable_words:
                    meaningful_words.append(word)
        
        # Combine translated terms with meaningful words, add category context
        all_terms = translated_terms + meaningful_words
        
        # Add category-specific context if we have space
        if category in category_context and len(all_terms) < 4:
            context_words = category_context[category]
            for ctx_word in context_words:
                if ctx_word not in all_terms:
                    all_terms.append(ctx_word)
                    if len(all_terms) >= 5:
                        break
        
        return all_terms[:5]  # Return up to 5 terms
    
    def generate_search_terms(self, title, topic, category):
        """Generate specific, contextual search terms for image search"""
        # Translate looksmaxing terms to specific, contextual terms
        combined_text = f"{title} {topic or ''}".strip()
        translated_terms = self.translate_looksmaxing_terms(combined_text, category)
        
        # Prioritize multi-word, specific phrases (they're already contextual)
        search_terms = []
        
        # First, add all multi-word terms (most specific)
        multi_word_terms = [t for t in translated_terms if " " in t]
        single_word_terms = [t for t in translated_terms if " " not in t]
        
        search_terms.extend(multi_word_terms)
        
        # Then combine single words into specific phrases
        if single_word_terms:
            # Combine first 2 single words if we have space
            if len(search_terms) < 2 and len(single_word_terms) >= 2:
                combined = f"{single_word_terms[0]} {single_word_terms[1]}"
                search_terms.append(combined)
            elif len(search_terms) < 3:
                # Add single words as-is if they're specific enough
                search_terms.extend(single_word_terms[:2])
        
        # Remove duplicates and partial matches (keep longer, more specific terms)
        unique_terms = []
        seen_lower = set()
        for term in search_terms:
            term_lower = term.lower().strip()
            # Skip exact duplicates
            if term_lower in seen_lower:
                continue
            
            is_duplicate = False
            for existing in unique_terms:
                existing_lower = existing.lower().strip()
                # If one contains the other, keep the longer/more specific one
                if term_lower in existing_lower and term_lower != existing_lower:
                    is_duplicate = True
                    break
                if existing_lower in term_lower and term_lower != existing_lower:
                    # Replace with more specific term
                    unique_terms.remove(existing)
                    seen_lower.discard(existing_lower)
                    break
            if not is_duplicate:
                unique_terms.append(term)
                seen_lower.add(term_lower)
        
        # Limit to 2-3 most specific terms for better image matching
        final_terms = unique_terms[:3]
        
        # If we still don't have enough, add category-specific defaults
        if len(final_terms) < 2:
            category_defaults = {
                "Facial Aesthetics": ["male portrait", "facial features"],
                "Body Aesthetics": ["athletic male", "fitness"],
                "Lifestyle": ["healthy lifestyle", "wellness"],
                "Grooming": ["male grooming", "style"],
                "Surgery": ["medical procedure", "cosmetic surgery"]
            }
            if category in category_defaults:
                for default in category_defaults[category]:
                    if not any(default.lower() in term.lower() or term.lower() in default.lower() for term in final_terms):
                        final_terms.append(default)
                        if len(final_terms) >= 3:
                            break
        
        return final_terms[:3]  # Return 2-3 most specific terms
    
    def find_image_url_pexels(self, search_query):
        """Find image URL using Pexels API"""
        try:
            headers = {
                "Authorization": self.pexels_api_key
            }
            
            response = requests.get(
                f"{self.pexels_api_url}/search",
                headers=headers,
                params={
                    "query": search_query,
                    "per_page": 1,
                    "orientation": "landscape",
                    "size": "large"
                },
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            photos = data.get('photos', [])
            
            if photos and len(photos) > 0:
                # Get the largest available size
                photo = photos[0]
                src = photo.get('src', {})
                
                # Prefer original (highest quality), then large, then medium
                image_url = src.get('original') or src.get('large') or src.get('medium') or src.get('small')
                if image_url:
                    return image_url
            
            return None
            
        except Exception as e:
            print(f"  ⚠ Pexels API error: {e}")
            return None
    
    def find_image_url_unsplash(self, search_query):
        """Find image URL using Unsplash Source API (fallback)"""
        try:
            # Use Unsplash Source API (free, no auth needed)
            # Format: https://source.unsplash.com/WIDTHxHEIGHT/?QUERY
            # We'll use 1200x630 (optimal for WordPress featured images/OG images)
            image_url = f"{self.unsplash_source}/1200x630/?{quote(search_query)}"
            return image_url
        except Exception as e:
            print(f"  ⚠ Unsplash error: {e}")
            return None
    
    def find_image_url(self, title, topic=None, category="Lifestyle"):
        """Find a relevant image URL - tries Pexels first, then Unsplash, then fallback"""
        try:
            search_terms = self.generate_search_terms(title, topic, category)
            
            if not search_terms:
                # Fallback to generic looksmaxing/self-improvement image
                search_query = "self improvement male fitness"
            else:
                # Combine search terms
                search_query = " ".join(search_terms[:3])  # Use top 3 terms
            
            # Try Pexels first
            print(f"  Trying Pexels API...")
            image_url = self.find_image_url_pexels(search_query)
            if image_url:
                print(f"  ✓ Found image via Pexels")
                return image_url
            
            # Fallback to Unsplash
            print(f"  Trying Unsplash...")
            image_url = self.find_image_url_unsplash(search_query)
            if image_url:
                print(f"  ✓ Found image via Unsplash")
                return image_url
            
            # Final fallback - use category-specific placeholder or default
            print(f"  Using fallback image")
            fallback = self.placeholder_fallbacks.get(category, self.default_fallback)
            return fallback
            
        except Exception as e:
            print(f"⚠ Error finding image: {e}")
            # Return category-specific fallback or default
            fallback = self.placeholder_fallbacks.get(category, self.default_fallback)
            return fallback
    
    def download_image(self, image_url, filename=None):
        """Download image from URL"""
        try:
            response = requests.get(image_url, timeout=10, stream=True)
            response.raise_for_status()
            
            if filename is None:
                # Generate filename from URL
                filename = f"thumbnail_{hash(image_url) % 10000}.jpg"
            
            image_data = response.content
            return image_data, filename
            
        except Exception as e:
            print(f"⚠ Error downloading image: {e}")
            return None, None

