"""
Recipe Extractor
Extracts structured recipe data from TikTok videos using:
- Video captions
- Comments (creators often post recipes here!)
- Claude API to structure the data
"""

import os
import anthropic
from tiktok_scraper import get_video_comments


def extract_recipe_with_claude(caption, comments):
    """
    Uses Claude API to extract and structure recipe from captions and comments
    
    Args:
        caption: Video caption text
        comments: List of comment dictionaries
    
    Returns:
        Structured recipe dictionary
    """
    # Initialize Anthropic client with explicit parameters only
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("      Error: ANTHROPIC_API_KEY not found in environment")
        return None
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        print(f"      Error initializing Anthropic client: {e}")
        return None
    
    # Combine caption and top comments
    comment_text = "\n".join([f"- {c['text']}" for c in comments[:20]])
    
    prompt = f"""I have data from a TikTok recipe video. The creator often posts the full recipe in the caption or in the comments. Please extract a complete recipe from this information.

VIDEO CAPTION:
{caption}

COMMENTS (creators often post recipes here):
{comment_text}

Please extract and structure this into a recipe with the following JSON format:
{{
  "title": "Recipe name",
  "description": "Brief description",
  "prep_time": "e.g., 10 minutes (or null if not mentioned)",
  "cook_time": "e.g., 20 minutes (or null if not mentioned)",
  "servings": "e.g., 4 servings (or null if not mentioned)",
  "ingredients": [
    "1 cup flour",
    "2 eggs",
    etc.
  ],
  "instructions": [
    "Step 1: Do this",
    "Step 2: Do that",
    etc.
  ],
  "tips": ["Any helpful tips mentioned (or empty array)"]
}}

Important: Look carefully in the comments - creators often post the full recipe as a comment!

If you cannot find a complete recipe (at minimum title and ingredients), return null. Only return the JSON, no other text."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text.strip()
        
        # Parse JSON response
        import json
        try:
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            recipe = json.loads(response_text.strip())
            return recipe
        except json.JSONDecodeError:
            print("      Warning: Could not parse recipe from Claude response")
            return None
            
    except Exception as e:
        print(f"      Error calling Claude API: {e}")
        return None


def extract_recipe_from_video(video_data):
    """
    Main function to extract recipe from a TikTok video's caption and comments
    
    Args:
        video_data: Dictionary containing video information
    
    Returns:
        Structured recipe dictionary
    """
    recipe = None
    
    try:
        # Get comments (creators often post recipes here!)
        print(f"      Fetching comments...")
        comments = get_video_comments(video_data['id'], max_comments=50)
        
        # Extract recipe using Claude from caption + comments
        print(f"      Extracting recipe with Claude...")
        recipe = extract_recipe_with_claude(
            video_data['caption'],
            comments
        )
        
        if recipe:
            # Add metadata
            recipe['source'] = {
                'platform': 'TikTok',
                'author': video_data['author'],
                'url': video_data['video_url'],
                'likes': video_data['likes'],
                'views': video_data['views']
            }
    
    except Exception as e:
        print(f"      Error extracting recipe: {e}")
        recipe = None
    
    return recipe
