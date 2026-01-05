"""
Deep Research Module for Looksmaxing Niche
Based on analysis of looksmax.org and best-of-the-best subforum
"""

class LooksmaxingResearch:
    """
    Comprehensive research data for looksmaxing niche including:
    - Terminology and slang
    - Keywords and SEO terms
    - Content themes and topics
    - Language patterns and style
    - Audience preferences
    """
    
    # Core Terminology (from looksmax.org analysis)
    TERMINOLOGY = {
        "softmaxxing": "Non-invasive methods like skincare, fitness, grooming, and styling to improve appearance",
        "hardmaxxing": "Invasive procedures including cosmetic surgeries, orthodontics, and medical treatments",
        "mewing": "Technique involving proper tongue posture to enhance jawline definition and facial structure",
        "mogging": "Act of surpassing someone else in physical attractiveness",
        "blackpill": "Belief system emphasizing the deterministic role of genetics and physical appearance in social success",
        "chad": "Idealized attractive male archetype with strong jawline, good bone structure, and high social status",
        "looksmaxxing": "The practice of maximizing one's physical appearance through various methods",
        "looksmax": "Short form of looksmaxing",
        "pill": "Conceptual framework or worldview (blackpill, redpill, bluepill, moneypill)",
        "gtfih": "Get the f*** in here - forum slang for calling attention",
        "botb": "Best of the Best - highest quality content subforum",
    }
    
    # Maxxing Categories (from forum analysis)
    MAXXING_CATEGORIES = [
        "looksmaxxing", "softmaxxing", "hardmaxxing", "mewing", "skincaremaxxing",
        "fitnessmaxxing", "hairmaxxing", "stylemaxxing", "dietmaxxing", "sleepmaxxing",
        "makeupmaxxing", "penismaxxing", "heightmaxxing", "jawmaxxing", "eyemaxxing",
        "teethmaxxing", "collagenmaxxing", "hormonemaxxing", "posturemaxxing", "voicemaxxing"
    ]
    
    # High-Value Keywords (SEO and engagement)
    # Based on research: looksmaxing has 15.58B+ TikTok views, high search volume
    KEYWORDS = {
        "primary": [
            # Core looksmaxing terms (high volume)
            "looksmaxing", "looksmax", "looksmaxxing", "looksmaxing guide",
            "softmaxxing", "softmaxing", "hardmaxxing", "hardmaxing",
            "mewing", "mewing technique", "jawline", "jawline exercises",
            "facial aesthetics", "male grooming", "self-improvement",
            "aesthetic enhancement", "physical appearance", "facial structure",
            "glow up", "face maxxing", "body maxxing"
        ],
        "secondary": [
            # Medium volume, specific topics
            "skincare routine", "skincare routine for men", "fitness transformation",
            "chad physique", "facial symmetry", "bone structure", "height increase",
            "jaw development", "jawline development", "teeth whitening",
            "hair styling", "fashion tips", "posture correction", "voice training",
            "sleep optimization", "sleepmaxxing", "diet for aesthetics",
            "height optimization", "shoulder width", "waist to hip ratio",
            "eye area enhancement", "nose optimization", "mouth widening"
        ],
        "long_tail": [
            # High intent, lower competition long-tail keywords
            "how to looksmax", "how to start looksmaxing", "looksmaxing for men",
            "looksmaxing for beginners", "looksmaxing tips for men",
            "how to improve jawline naturally", "best skincare routine for men",
            "mewing technique guide", "how to mew correctly",
            "softmaxxing vs hardmaxxing", "facial aesthetics improvement",
            "male appearance enhancement", "natural looksmaxing methods",
            "looksmaxing without surgery", "cosmetic surgery for men",
            "fitness routine for aesthetics", "grooming tips for better looks",
            "looksmaxing before and after", "looksmaxing transformation",
            "looksmaxing routine", "looksmaxing skincare routine",
            "looksmaxing exercises", "looksmaxing jawline exercises",
            "looksmaxing diet plan", "looksmaxing hair growth tips",
            "how to get a better jawline", "how to improve facial symmetry",
            "best mewing exercises", "mewing results timeline",
            "posture correction exercises", "how to fix posture",
            "height increase exercises", "how to look taller",
            "skincare routine for clear skin", "best supplements for looksmaxing",
            "looksmaxing success stories", "looksmaxing community",
            "looksmaxing product reviews", "looksmaxing guide for beginners"
        ],
        "topic_specific": {
            "mewing": [
                "how to mew", "mewing technique", "mewing exercises",
                "mewing results", "mewing before and after", "proper tongue posture",
                "mewing guide", "how to mew correctly", "mewing timeline",
                "mewing for jawline", "mewing transformation"
            ],
            "jawline": [
                "how to get a better jawline", "jawline exercises",
                "jawline development", "strong jawline", "defined jawline",
                "jawline workout", "how to improve jawline", "jawline transformation",
                "jawline exercises for men", "best jawline exercises"
            ],
            "skincare": [
                "skincare routine for men", "best skincare routine",
                "male skincare", "skincare for clear skin", "skincare products for men",
                "skincare routine for acne", "anti-aging skincare", "skincaremaxxing"
            ],
            "posture": [
                "posture correction", "how to fix posture", "posture exercises",
                "good posture", "posture correction exercises", "improve posture",
                "posture for height", "posture correction guide"
            ],
            "fitness": [
                "aesthetic physique", "fitness transformation", "workout for aesthetics",
                "chad physique workout", "fitness routine", "bodybuilding for aesthetics",
                "physique development", "aesthetic body"
            ],
            "height": [
                "height increase", "how to get taller", "height optimization",
                "height increase exercises", "how to look taller", "height maxxing",
                "posture for height", "height growth"
            ],
            "hair": [
                "hair styling for men", "best hairstyles", "hairstyle for face shape",
                "hair grooming", "hairmaxxing", "hair styling tips",
                "best haircut for face shape"
            ],
            "supplements": [
                "best supplements for looksmaxing", "supplements for aesthetics",
                "supplements for skin", "supplements for hair growth",
                "looksmaxing supplements", "aesthetic supplements"
            ],
            "sleep": [
                "sleep optimization", "sleepmaxxing", "how to sleep better",
                "sleep for appearance", "sleep for skin", "quality sleep",
                "sleep routine for better looks"
            ]
        }
    }
    
    # Content Themes (from best-of-the-best analysis)
    CONTENT_THEMES = {
        "guides": [
            "Complete Skincare Routine for Maximum Results",
            "Mewing: The Ultimate Jawline Enhancement Guide",
            "How to Achieve a Chad Physique Naturally",
            "Softmaxxing vs Hardmaxxing: Complete Breakdown",
            "The Sleepmaxxing Playbook: Optimize Your Rest",
            "Mouth Widening Techniques and Appliances",
            "Teeth Whitening Methods That Actually Work",
            "First Steroid Cycle: A Comprehensive Guide",
            "Collagen Maximization for Skin Health",
            "Posture Correction for Better Appearance"
        ],
        "transformations": [
            "How I Achieved [X] in [Time Period]",
            "Before and After: My Looksmaxing Journey",
            "My Natural Transformation Story",
            "Results After [X] Months of Consistent Looksmaxing"
        ],
        "product_reviews": [
            "Best Skincare Products for Men",
            "Top Supplements for Aesthetic Enhancement",
            "Recommended Tools for Mewing",
            "Fashion Essentials for Better Appearance"
        ],
        "advanced_topics": [
            "The Truth About Steroids and Peptides",
            "Surgical Options for Facial Enhancement",
            "Hormone Optimization for Aesthetics",
            "Genetic Limitations and What You Can Change"
        ]
    }
    
    # Language Patterns (from forum analysis)
    LANGUAGE_PATTERNS = {
        "tone": "direct, no-nonsense, results-focused, evidence-based",
        "style": "detailed guides, step-by-step instructions, personal experiences",
        "common_phrases": [
            "GTFIH", "mog", "chad", "blackpill", "based", "cope", "cope harder",
            "it's over", "just looksmax bro", "maxxing", "pill", "ascend"
        ],
        "title_patterns": [
            "How I [Achieved X] [Method]",
            "[Topic] Guide: [Subtitle]",
            "The [Topic] Playbook",
            "[Topic] Megathread",
            "Complete [Topic] Breakdown"
        ],
        "emphasis_style": "Uses ALL CAPS for emphasis, numbers for results, before/after focus"
    }
    
    # Topic Categories (from best-of-the-best threads)
    TOPIC_CATEGORIES = {
        "facial_aesthetics": [
            "jawline development", "mewing", "facial symmetry", "bone structure",
            "eye area enhancement", "nose optimization", "mouth widening",
            "facial hair styling", "skincare", "teeth whitening"
        ],
        "body_aesthetics": [
            "physique development", "posture correction", "height optimization",
            "shoulder width", "waist-to-hip ratio", "muscle definition"
        ],
        "lifestyle": [
            "sleep optimization", "diet for aesthetics", "supplementation",
            "hormone optimization", "stress management", "recovery"
        ],
        "grooming": [
            "hair styling", "skincare routine", "fashion sense", "fragrance",
            "dental care", "nail care", "body hair management"
        ],
        "advanced": [
            "cosmetic surgery", "orthodontics", "steroids and PEDs", "peptides",
            "hair transplants", "filler procedures", "jaw surgery"
        ]
    }
    
    # Audience Insights
    AUDIENCE_INSIGHTS = {
        "demographics": "Primarily men aged 18-35 interested in self-improvement",
        "values": [
            "Evidence-based information", "Detailed guides", "Before/after proof",
            "Measurable results", "Honest assessments", "Practical advice"
        ],
        "content_preferences": [
            "Step-by-step guides", "Personal transformation stories",
            "Product reviews with results", "Scientific explanations",
            "Visual content (before/after)", "Detailed routines"
        ],
        "engagement_triggers": [
            "Results-focused titles", "Specific timeframes", "Measurable outcomes",
            "Personal success stories", "Comprehensive guides", "Controversial topics"
        ]
    }
    
    # SEO Optimization Terms (Comprehensive Research-Based)
    SEO_TERMS = {
        "high_volume": [
            # Primary high-volume keywords (10K+ monthly searches)
            "looksmaxing", "looksmax", "looksmaxxing", "mewing", "jawline",
            "male grooming", "self improvement", "skincare routine",
            "facial aesthetics", "posture correction", "height increase",
            "glow up", "face maxxing"
        ],
        "medium_volume": [
            # Medium volume keywords (1K-10K monthly searches)
            "softmaxxing", "hardmaxxing", "jawline exercises", "mewing technique",
            "skincare routine for men", "facial symmetry", "bone structure",
            "teeth whitening", "hair styling", "fitness transformation",
            "sleep optimization", "diet for aesthetics", "voice training",
            "height optimization", "posture exercises"
        ],
        "long_tail_high_intent": [
            # Long-tail keywords with high commercial/intent value (lower competition)
            "how to looksmax", "looksmaxing guide for beginners",
            "how to improve jawline naturally", "best skincare routine for men",
            "mewing technique guide", "softmaxxing vs hardmaxxing",
            "looksmaxing without surgery", "looksmaxing before and after",
            "looksmaxing transformation", "looksmaxing routine",
            "how to get a better jawline", "how to fix posture",
            "height increase exercises", "best supplements for looksmaxing",
            "looksmaxing success stories", "looksmaxing product reviews",
            "how to start looksmaxing", "looksmaxing tips for men",
            "looksmaxing skincare routine", "looksmaxing exercises",
            "looksmaxing jawline exercises", "looksmaxing diet plan",
            "looksmaxing hair growth tips", "how to improve facial symmetry",
            "best mewing exercises", "mewing results timeline",
            "posture correction exercises", "how to look taller",
            "skincare routine for clear skin", "looksmaxing community"
        ],
        "question_keywords": [
            # Question-based keywords (high search intent)
            "what is looksmaxing", "how to start looksmaxing",
            "how does mewing work", "how to improve jawline",
            "how to fix posture", "how to get taller",
            "what is softmaxxing", "what is hardmaxxing",
            "how long does mewing take", "does mewing work",
            "how to improve facial symmetry", "best skincare for men",
            "how to look more attractive", "how to improve appearance",
            "what is looksmax", "how to looksmax for beginners"
        ],
        "comparison_keywords": [
            # Comparison keywords (high research intent)
            "softmaxxing vs hardmaxxing", "mewing vs jaw surgery",
            "natural vs surgical looksmaxing", "skincare routine comparison",
            "best jawline exercises comparison", "height increase methods",
            "looksmaxing methods comparison"
        ]
    }
    
    @classmethod
    def get_topic_suggestion(cls):
        """Generate a random topic suggestion based on research data"""
        import random
        
        theme_type = random.choice(list(cls.CONTENT_THEMES.keys()))
        topics = cls.CONTENT_THEMES[theme_type]
        return random.choice(topics)
    
    @classmethod
    def get_keywords_for_topic(cls, topic):
        """Extract relevant SEO keywords for a given topic"""
        keywords = []
        topic_lower = topic.lower()
        
        # Add primary keywords (always include core terms)
        keywords.extend(cls.KEYWORDS["primary"][:2])  # looksmaxing, mewing/jawline
        
        # Add topic-specific keywords if available
        for topic_key, topic_keywords in cls.KEYWORDS.get("topic_specific", {}).items():
            if topic_key in topic_lower:
                keywords.extend(topic_keywords[:3])
                break
        
        # Add relevant maxxing categories
        for category in cls.MAXXING_CATEGORIES:
            category_base = category.replace("maxxing", "").replace("maxing", "")
            if category_base in topic_lower:
                keywords.append(category)
        
        # Add secondary keywords based on topic match
        for keyword in cls.KEYWORDS["secondary"]:
            if any(word in topic_lower for word in keyword.split()):
                keywords.append(keyword)
        
        # Add relevant long-tail keywords
        for long_tail in cls.KEYWORDS["long_tail"]:
            if any(word in topic_lower for word in long_tail.split()[:3]):  # Check first 3 words
                keywords.append(long_tail)
                if len(keywords) >= 12:  # Limit total keywords
                    break
        
        # Add question keywords if relevant
        for q_keyword in cls.SEO_TERMS.get("question_keywords", []):
            if any(word in topic_lower for word in q_keyword.split()[:2]):
                keywords.append(q_keyword)
                break
        
        return list(set(keywords))[:15]  # Return up to 15 unique keywords for better SEO
    
    @classmethod
    def get_language_guidelines(cls):
        """Get comprehensive language guidelines for content generation"""
        return {
            "tone": cls.LANGUAGE_PATTERNS["tone"],
            "style": cls.LANGUAGE_PATTERNS["style"],
            "avoid": [
                "overly casual language", "excessive slang", "unprofessional tone",
                "medical claims without evidence", "promises of unrealistic results"
            ],
            "include": [
                "Evidence-based information", "Step-by-step instructions",
                "Measurable outcomes", "Honest assessments", "Practical advice"
            ]
        }

