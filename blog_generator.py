"""
Blog Post Generator - Single Request High-Quality Generation
Focus: SEO optimization + Authentic looksmaxing tone
"""

import re
import requests
from looksmaxing_research import LooksmaxingResearch
from post_tracker import PostTracker
from config import OLLAMA_BASE_URL, OLLAMA_MODEL


class BlogPostGenerator:
    """Generates high-quality blog posts with SEO and authentic tone"""
    
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL.rstrip('/')
        self.model_name = OLLAMA_MODEL
        self.research = LooksmaxingResearch()
        self.post_tracker = PostTracker()
        
        # Test connection
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to connect to Ollama at {self.base_url}. Make sure Ollama is running: {e}")
    
    def _generate_text(self, system_prompt, user_prompt, temperature=0.7, max_tokens=4000):
        """Generate text using Ollama API"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": user_prompt,
                    "system": system_prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        "top_p": 0.95,
                        "top_k": 40
                    }
                },
                timeout=300
            )
            response.raise_for_status()
            
            result = response.json()
            if 'response' in result:
                return result['response'].strip()
            else:
                raise ValueError("Empty response from model")
                
        except requests.exceptions.RequestException as e:
            print(f"Error generating text: {e}")
            raise
    
    def _get_research_data(self):
        """Get all research data for prompts"""
        terminology_list = list(self.research.TERMINOLOGY.keys())
        common_phrases = self.research.LANGUAGE_PATTERNS.get("common_phrases", [])
        maxxing_categories = self.research.MAXXING_CATEGORIES[:12]
        language_guidelines = self.research.get_language_guidelines()
        
        return {
            "terminology": terminology_list,
            "common_phrases": common_phrases,
            "maxxing_categories": maxxing_categories,
            "language_guidelines": language_guidelines
        }
    
    def generate_title(self, topic=None):
        """Generate an SEO-optimized title"""
        if not topic:
            topic = self.research.get_topic_suggestion()
        
        system_prompt = "You are an expert SEO content creator specializing in looksmaxing and male self-improvement."
        
        title_prompt = f"""Generate ONLY a blog post title about: {topic}

Return ONLY the title text. No prefixes, labels, or explanations.

Requirements:
- 60-70 characters (SEO-optimized length)
- Include primary keyword naturally
- Engaging and click-worthy
- Uses looksmaxing terminology
- Title case

Title:"""
        
        try:
            title = self._generate_text(system_prompt, title_prompt, temperature=0.8, max_tokens=100)
            title = title.strip('"').strip("'").strip()
            title = title.replace("Title:", "").replace("Title", "").strip()
            if '\n' in title:
                title = title.split('\n')[0].strip()
            if len(title) > 70:
                title = title[:67] + "..."
            return title if title else f"Complete Guide to {topic}"
        except Exception as e:
            print(f"Error generating title: {e}")
            return f"Complete Guide to {topic}"
    
    def generate_content(self, title, topic=None):
        """Generate full blog post content - single request with SEO and authentic tone"""
        if not topic:
            topic = self.research.get_topic_suggestion()
        
        keywords = self.research.get_keywords_for_topic(topic)
        research_data = self._get_research_data()
        language_guidelines = research_data['language_guidelines']
        
        # Get relevant posts for internal linking
        relevant_posts = self.post_tracker.get_relevant_posts(topic, title, max_posts=4)
        relevant_posts = [p for p in relevant_posts if p.get('id') and p.get('url') and p.get('title')]
        
        internal_links_info = ""
        if relevant_posts:
            internal_links_info = "\n\nINTERNAL LINKS (add 2-4 natural links to these posts):\n"
            for post in relevant_posts:
                internal_links_info += f"- {post.get('title')} - {post.get('url')}\n"
        else:
            internal_links_info = "\n\nNO INTERNAL LINKS: Do NOT create any links or 'Related Posts' sections.\n"
        
        system_prompt = f"""You are a veteran looksmaxer writing for the looksmax.org community. You write with the authentic, edgy, direct tone of the best-of-the-best subforum. This is NOT a generic self-help blog - this is looksmaxing content for the community.

CRITICAL TERMINOLOGY (MUST use naturally throughout - this is non-negotiable):
{', '.join(research_data['terminology'][:15])}

COMMON PHRASES (use these naturally):
{', '.join(research_data['common_phrases'][:8])}

AUTHENTIC TONE (MANDATORY - NO NORMIE LANGUAGE):
- Edgy, direct, no-bullshit approach
- Use community slang naturally: mog, chad, based, cope, ascend, maxxing, blackpill
- Call out normie advice and generic self-help BS
- Be brutally honest about what works vs what doesn't
- Use "-maxxing" suffix liberally (skincaremaxxing, fitnessmaxxing, sleepmaxxing, etc.)
- Write like you're on looksmax.org, not a corporate blog
- Use specific numbers and timeframes: "30-60 days", "3-6 months", "mogged 80% of guys"
- Before/after focus, transformation mindset
- Acknowledge genetic reality but focus on what CAN be changed
- Use phrases like "real talk", "let's be honest", "most guys don't know this"

AVOID NORMIE LANGUAGE (DO NOT USE):
- Generic self-help phrases: "self-improvement journey", "personal growth", "be your best self"
- Corporate speak: "optimize your potential", "unlock your best version"
- Soft language: "feel good about yourself", "build confidence"
- Generic fitness terms without looksmaxing context
- Academic or overly formal tone

USE AUTHENTIC LOOKSMAXING LANGUAGE:
- "If you're serious about looksmaxing..."
- "Most guys are doing this wrong..."
- "Real talk: this is what actually works..."
- "You'll mog most guys who aren't maxxing..."
- "The chad aesthetic requires..."
- "Softmaxxing vs hardmaxxing - here's the real difference..."
- "This is based, that's cope..." """
        
        content_prompt = f"""Write a complete, SEO-optimized looksmaxing blog post in proper WordPress HTML format.

TITLE: {title}
TOPIC: {topic}
{internal_links_info}

CRITICAL REQUIREMENTS:

1. WORD COUNT: Write exactly 2500-3000 words total (comprehensive, detailed content)

2. SEO OPTIMIZATION (CRUCIAL):
   - Primary keyword: {keywords[0] if keywords else topic}
   - Secondary keywords: {', '.join(keywords[1:8])}
   - Use primary keyword in first paragraph, H2 headings, and naturally throughout
   - Include long-tail keywords naturally
   - Optimize heading structure (H1 in title, H2 for main sections, H3 for subsections)
   - Use semantic keywords related to the topic

3. HTML FORMAT (WordPress ready):
   - Use <h2> for main sections (6-8 sections)
   - Use <h3> for subsections (2-3 per main section)
   - Use <p> for all paragraphs
   - Use <ul><li> for bullet lists (include 3-4 lists)
   - Use <ol><li> for numbered lists (include 1-2 lists)
   - Use <table><thead><tr><th>Header</th></tr></thead><tbody><tr><td>Data</td></tr></tbody></table> for tables (include 1-2 tables)
   - Use <strong> for important terms and keywords
   - Proper spacing between elements

4. TERMINOLOGY (AUTHENTIC TONE - CRUCIAL - NO NORMIE LANGUAGE):
   - MUST use looksmaxing terms constantly: looksmaxing, softmaxxing, hardmaxxing, mewing, mogging, chad, blackpill
   - Use "-maxxing" suffix liberally (skincaremaxxing, fitnessmaxxing, sleepmaxxing, dietmaxxing, etc.)
   - Include community phrases naturally: based, cope, ascend, maxxing, mog, "real talk", "let's be honest"
   - Write like you're on looksmax.org best-of-the-best subforum - edgy, direct, no-bullshit
   - Call out normie advice: "Most normies think X, but real looksmaxers know Y"
   - Use phrases like "if you're serious about looksmaxing", "most guys don't know this", "this will mog X% of guys"
   - AVOID: generic self-help language, corporate speak, soft motivational phrases

5. CONTENT STRUCTURE:
   - Strong introduction (hook + primary keyword)
   - 6-8 main sections with H2 headings
   - Each section: 300-500 words with 2-3 H3 subsections
   - Include practical, actionable advice
   - Use specific numbers, timeframes, and results
   - Include comparison tables where relevant
   - Strong conclusion summarizing key points

6. INTERNAL LINKS: {internal_links_info.split(chr(10))[1] if internal_links_info and 'INTERNAL LINKS' in internal_links_info else "No internal links needed"}

EXAMPLES OF AUTHENTIC TONE (USE THIS STYLE):

❌ NORMIE (DON'T WRITE LIKE THIS):
"Self-improvement is important for personal growth. Here are some tips to help you feel better about yourself and build confidence through exercise and skincare."

✅ AUTHENTIC LOOKSMAXING (WRITE LIKE THIS):
"Real talk: if you're serious about looksmaxing, you need to understand the difference between softmaxxing and hardmaxxing. Most normies think it's just about 'self-improvement' - that's cope. Real looksmaxers know that softmaxxing (mewing, skincaremaxxing, fitnessmaxxing) is where you start, but the chad aesthetic requires optimizing everything. This isn't about feeling good - it's about mogging 80% of guys who aren't maxxing."

❌ NORMIE:
"Exercise can improve your appearance and help you feel more confident."

✅ AUTHENTIC:
"Fitnessmaxxing is non-negotiable if you want to ascend. The chad physique isn't about 'feeling confident' - it's about the right proportions, shoulder-to-waist ratio, and aesthetic goals. Most guys are doing this wrong with generic gym routines. Real looksmaxers focus on what actually matters for the aesthetic."

❌ NORMIE:
"A strong jawline is considered attractive. Here's how to improve it."

✅ AUTHENTIC:
"A defined jawline is essential for that chad aesthetic. Mewing combined with proper softmaxxing can mog most guys who aren't maxxing. Let's be honest - most normies don't even know what mewing is. Here's the real talk on what actually works."

HTML STRUCTURE EXAMPLE:
<h2>What Is {keywords[0] if keywords else topic}?</h2>
<p>Opening paragraph with primary keyword naturally integrated. This is where you hook the reader and establish the topic's importance in looksmaxing.</p>

<h3>Understanding the Basics</h3>
<p>Detailed explanation with looksmaxing terminology naturally used.</p>

<ul>
<li>Key point one with detailed explanation</li>
<li>Key point two with specifics</li>
<li>Key point three with actionable advice</li>
</ul>

<table>
<thead>
<tr>
<th>Method</th>
<th>Timeframe</th>
<th>Results</th>
</tr>
</thead>
<tbody>
<tr>
<td>Method A</td>
<td>30-60 days</td>
<td>Initial improvements</td>
</tr>
<tr>
<td>Method B</td>
<td>3-6 months</td>
<td>Significant progress</td>
</tr>
</tbody>
</table>

CRITICAL: This is NOT a generic self-help blog. This is looksmaxing content for the community.
- Use looksmaxing terminology CONSTANTLY throughout
- Write with edge and directness - no soft language
- Call out normie advice when relevant
- Use community phrases naturally
- Be brutally honest about what works vs what doesn't
- Write like you're on looksmax.org, not a corporate blog

If the content sounds generic, bland, or like a normie self-help article, it's WRONG. 
It should sound like authentic looksmaxing community content.

Now write the complete blog post. Write 2500-3000 words in proper WordPress HTML format with SEO optimization and AUTHENTIC looksmaxing tone (NOT normie language):"""
        
        try:
            content = self._generate_text(system_prompt, content_prompt, temperature=0.7, max_tokens=12000)
            
            if not content or len(content.strip()) < 500:
                raise ValueError("Generated content is too short")
            
            # Clean content
            content = self._clean_html_content(content)
            content = self._remove_related_posts(content)
            content = self._validate_links(content, relevant_posts)
            
            # Final validation
            text_content = re.sub(r'<[^>]+>', '', content)
            word_count = len(text_content.split())
            
            h2_count = len(re.findall(r'<h2[^>]*>', content, re.IGNORECASE))
            h3_count = len(re.findall(r'<h3[^>]*>', content, re.IGNORECASE))
            ul_count = len(re.findall(r'<ul[^>]*>', content, re.IGNORECASE))
            ol_count = len(re.findall(r'<ol[^>]*>', content, re.IGNORECASE))
            table_count = len(re.findall(r'<table[^>]*>', content, re.IGNORECASE))
            p_count = len(re.findall(r'<p[^>]*>', content, re.IGNORECASE))
            
            print(f"✓ Content generated: {word_count} words, H2={h2_count}, H3={h3_count}, UL={ul_count}, OL={ol_count}, Tables={table_count}, P={p_count}")
            
            # Validate word count
            if word_count < 2500:
                print(f"⚠ Warning: Content is {word_count} words (target: 2500-3000)")
            elif word_count > 3000:
                print(f"⚠ Warning: Content is {word_count} words (target: 2500-3000)")
            
            # Validate terminology and check for normie language
            content_lower = content.lower()
            required_terms = ['looksmax', 'softmaxx', 'hardmaxx', 'mewing', 'mog', 'chad', 'maxxing']
            found_terms = [term for term in required_terms if term in content_lower]
            
            # Check for normie language patterns
            normie_patterns = [
                'self-improvement journey', 'personal growth', 'be your best self',
                'unlock your potential', 'optimize your potential', 'feel good about yourself',
                'build confidence', 'self-care', 'wellness journey'
            ]
            found_normie = [pattern for pattern in normie_patterns if pattern in content_lower]
            
            if len(found_terms) < 4:
                print(f"⚠ Warning: May lack looksmaxing terminology. Found: {found_terms}")
                print(f"  Content should use more looksmaxing terms: mog, chad, maxxing, based, cope, etc.")
            
            if found_normie:
                print(f"⚠ Warning: Found normie language patterns: {found_normie}")
                print(f"  Content should use authentic looksmaxing language, not generic self-help terms")
            
            # Validate SEO - check primary keyword usage
            primary_keyword = keywords[0].lower() if keywords else topic.lower()
            keyword_count = content_lower.count(primary_keyword)
            if keyword_count < 5:
                print(f"⚠ Warning: Primary keyword '{primary_keyword}' appears only {keyword_count} times (should be 5-10 times)")
            
            # Add disclaimer
            disclaimer = '\n\n<hr />\n\n<p><em>Disclaimer: This article is for informational purposes only and does not constitute medical advice. Always consult with qualified healthcare professionals before making significant changes to your health, fitness, or appearance routines. Individual results may vary.</em></p>'
            
            return content + disclaimer
            
        except Exception as e:
            print(f"Error generating content: {e}")
            raise
    
    def _clean_html_content(self, content):
        """Clean HTML content - remove markdown, fix formatting"""
        if not content:
            return content
        
        # Remove markdown headers if still present
        content = re.sub(r'^#{1,6}\s+(.+)$', lambda m: f'<h2>{m.group(1)}</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^###\s+(.+)$', lambda m: f'<h3>{m.group(1)}</h3>', content, flags=re.MULTILINE)
        
        # Convert markdown bold to HTML
        content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', content)
        
        # Remove markdown code
        content = re.sub(r'`([^`]+)`', r'\1', content)
        
        # Ensure proper spacing
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content
    
    def _remove_related_posts(self, content):
        """Remove any 'Related Posts' sections"""
        if not content:
            return content
        patterns = [
            r'<h[2-6][^>]*>.*?[Rr]elated\s+[Pp]osts?.*?</h[2-6]>.*?</(?:ul|ol|p)>',
            r'##?\s*[Rr]elated\s+[Pp]osts?.*?\n(?:.*?\n)*?(?=\n##|\Z)',
        ]
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
        return content
    
    def _validate_links(self, content, relevant_posts):
        """Validate and remove links to non-existent posts"""
        if not relevant_posts:
            content = self._remove_related_posts(content)
            def remove_link(match):
                link_text = re.search(r'>([^<]+)</a>', match.group(0))
                return link_text.group(1) if link_text else ''
            content = re.sub(r'<a\s+href="https?://(?:www\.)?lookizm\.com[^"]*"[^>]*>.*?</a>', remove_link, content, flags=re.IGNORECASE | re.DOTALL)
            return content
        
        valid_urls = {post.get('url', '').lower().rstrip('/') for post in relevant_posts if post.get('url')}
        
        def replace_invalid_link(match):
            link_url = match.group(1).lower().rstrip('/')
            link_text = match.group(2)
            if 'lookizm.com' in link_url and link_url not in valid_urls:
                return link_text
            return match.group(0)
        
        content = re.sub(r'<a\s+href="([^"]+)"[^>]*>(.*?)</a>', replace_invalid_link, content, flags=re.IGNORECASE | re.DOTALL)
        return content
    
    def generate_excerpt(self, content, max_length=160):
        """Generate a short excerpt"""
        text_content = re.sub(r'<[^>]+>', '', content)
        sentences = text_content.split('.')
        excerpt = sentences[0] if sentences else text_content[:max_length]
        excerpt = excerpt.strip()
        if len(excerpt) > max_length:
            excerpt = excerpt[:max_length-3] + "..."
        return excerpt
    
    def generate_tags(self, title, content):
        """Generate relevant tags"""
        topic_keywords = self.research.get_keywords_for_topic(title)
        
        system_prompt = "You are an SEO expert specializing in looksmaxing content."
        tag_prompt = f"""Generate 8-10 relevant SEO tags for this blog post.

Title: {title}
Content preview: {content[:500]}...

Return ONLY the tags, comma-separated. No prefixes or labels."""
        
        try:
            tags_str = self._generate_text(system_prompt, tag_prompt, temperature=0.5, max_tokens=100)
            tags = [tag.strip().strip('"').strip("'") for tag in tags_str.split(',') if tag.strip()]
            tags = [tag for tag in tags if len(tag) > 0][:10]
            return tags if tags else topic_keywords[:10]
        except Exception as e:
            print(f"Error generating tags: {e}")
            return topic_keywords[:10]
    
    def determine_category(self, topic, title, content):
        """Determine category based on topic, title, and content"""
        topic_lower = (topic or "").lower()
        title_lower = title.lower()
        content_lower = (content[:500] if content else "").lower()
        
        category_keywords = {
            "Facial Aesthetics": ["jawline", "mewing", "facial", "nose", "mouth", "skincare", "teeth", "jaw", "chin"],
            "Body Aesthetics": ["physique", "posture", "height", "shoulder", "waist", "muscle", "body"],
            "Lifestyle": ["sleep", "diet", "supplement", "hormone", "stress", "nutrition", "lifestyle"],
            "Grooming": ["hair", "fashion", "fragrance", "dental", "grooming", "style", "wardrobe"],
            "Surgery": ["surgery", "orthodontics", "steroids", "peptide", "hair transplant", "filler", "hardmaxxing"]
        }
        
        category_scores = {}
        for category, keywords in category_keywords.items():
            score = 0
            for kw in keywords:
                if kw in topic_lower:
                    score += 3
                if kw in title_lower:
                    score += 2
                if kw in content_lower:
                    score += 1
            category_scores[category] = score
        
        return max(category_scores.items(), key=lambda x: x[1])[0] if max(category_scores.values()) > 0 else "Lifestyle"
    
    def generate_full_post(self, topic=None):
        """Generate a complete blog post with all components"""
        print(f"\n{'='*60}")
        print(f"Generating blog post")
        print(f"{'='*60}")
        print(f"Topic: {topic or 'auto-selected'}")
        print(f"Model: {self.model_name}")
        print(f"{'='*60}\n")
        
        title = self.generate_title(topic)
        print(f"Generated title: {title}\n")
        
        content = self.generate_content(title, topic)
        print(f"\nGenerated content ({len(content)} characters)\n")
        
        excerpt = self.generate_excerpt(content)
        tags = self.generate_tags(title, content)
        print(f"Tags: {', '.join(tags[:8])}")
        
        category = self.determine_category(topic, title, content)
        print(f"Category: {category}\n")
        
        return {
            "title": title,
            "content": content,
            "excerpt": excerpt,
            "tags": tags,
            "topic": topic or "auto-selected",
            "category": category
        }
