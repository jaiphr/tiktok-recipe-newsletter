"""
Simplified TikTok Scraper - Manual URL Version
Instead of automatically finding trending videos, you manually specify which videos to use.
This is more reliable and gives you control over recipe quality!
"""

import requests
import re
import json


def get_video_data_from_url(video_url):
    """
    Extract video data from a TikTok URL by scraping the page
    
    Args:
        video_url: Full TikTok video URL (e.g., https://www.tiktok.com/@username/video/1234567890)
    
    Returns:
        Dictionary with video data
    """
    try:
        # Extract username and video ID from URL
        username_match = re.search(r'@([^/]+)', video_url)
        video_id_match = re.search(r'/video/(\d+)', video_url)
        
        if not username_match or not video_id_match:
            print(f"   Warning: Could not parse URL: {video_url}")
            return None
        
        username = username_match.group(1)
        video_id = video_id_match.group(1)
        
        # Fetch the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(video_url, headers=headers)
        response.raise_for_status()
        
        # Try to extract caption from the page HTML
        caption_match = re.search(r'"desc":"([^"]+)"', response.text)
        caption = caption_match.group(1) if caption_match else "No caption found"
        
        # Decode unicode escapes in caption
        caption = caption.encode().decode('unicode_escape')
        
        # Try to extract stats
        likes_match = re.search(r'"diggCount":(\d+)', response.text)
        views_match = re.search(r'"playCount":(\d+)', response.text)
        
        video_data = {
            'id': video_id,
            'title': caption[:100] if caption else "Recipe Video",
            'author': username,
            'video_url': video_url,
            'likes': int(likes_match.group(1)) if likes_match else 0,
            'views': int(views_match.group(1)) if views_match else 0,
            'shares': 0,
            'caption': caption,
            'hashtags': [],
            'music': None,
        }
        
        return video_data
        
    except Exception as e:
        print(f"   Error fetching {video_url}: {e}")
        return None


def get_video_comments_simple(video_id):
    """
    Simplified comment fetching - returns empty list for now
    You can add comments manually in recipe_urls.json if needed
    
    Args:
        video_id: TikTok video ID
    
    Returns:
        List of comment dictionaries
    """
    # TikTok's comment API requires authentication, so we'll skip this
    # The recipe is usually in the caption anyway!
    return []


def load_recipe_urls():
    """
    Load TikTok video URLs from recipe_urls.json
    
    Returns:
        List of video URLs
    """
    try:
        with open('recipe_urls.json', 'r') as f:
            data = json.load(f)
            return data.get('urls', [])
    except FileNotFoundError:
        print("   Warning: recipe_urls.json not found. Creating example file...")
        
        # Create example file
        example_data = {
            "urls": [
                "https://www.tiktok.com/@feelgoodfoodie/video/7234567890123456789",
                "https://www.tiktok.com/@brunchwithbabs/video/7234567890123456790",
                "https://www.tiktok.com/@cookingwithshereen/video/7234567890123456791",
            ],
            "instructions": "Add TikTok recipe video URLs here. Find them by browsing TikTok and copying the video link!"
        }
        
        with open('recipe_urls.json', 'w') as f:
            json.dump(example_data, f, indent=2)
        
        return example_data['urls']


def get_trending_recipe_videos(count=5):
    """
    Get recipe videos from manually specified URLs
    
    Args:
        count: Maximum number of videos to return
    
    Returns:
        List of video data dictionaries
    """
    print("   Loading TikTok URLs from recipe_urls.json...")
    
    urls = load_recipe_urls()
    
    if not urls:
        print("   Warning: No URLs found in recipe_urls.json")
        return []
    
    videos = []
    for url in urls[:count]:
        print(f"   Fetching: {url}")
        video_data = get_video_data_from_url(url)
        if video_data:
            videos.append(video_data)
    
    return videos


# Keep this for backwards compatibility
def get_video_comments(video_id, max_comments=50):
    """Wrapper for backwards compatibility"""
    return get_video_comments_simple(video_id)


### Step 2: Make Sure requirements.txt is Updated


# TikTok Recipe Newsletter Dependencies (Simplified)

# AI for recipe extraction
anthropic==0.39.0

# Email service
resend==2.0.0

# Web requests
requests==2.31.0

# Utilities
python-dotenv==1.0.0
