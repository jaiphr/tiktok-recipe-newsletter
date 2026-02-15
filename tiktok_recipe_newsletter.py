"""
TikTok Recipe Newsletter Generator
Finds trending recipe videos, extracts recipes from captions/comments, and emails them to subscribers
"""

import os
import json
from datetime import datetime
from pathlib import Path
import anthropic
import resend

# Import our helper modules
from tiktok_scraper import get_trending_recipe_videos
from recipe_extractor import extract_recipe_from_video
from newsletter_builder import create_html_newsletter


def load_subscribers():
    """Load email subscribers from JSON file"""
    subscriber_file = Path("subscribers.json")
    if subscriber_file.exists():
        with open(subscriber_file, 'r') as f:
            return json.load(f)
    return []


def save_recipes_archive(recipes):
    """Save recipes to archive for record keeping"""
    archive_dir = Path("archive")
    archive_dir.mkdir(exist_ok=True)
    
    filename = f"recipes_{datetime.now().strftime('%Y%m%d')}.json"
    with open(archive_dir / filename, 'w') as f:
        json.dump(recipes, f, indent=2)


def send_newsletter(html_content, subscribers):
    """Send the newsletter via Resend"""
    resend.api_key = os.environ["RESEND_API_KEY"]
    
    subject = f"🍳 Top 5 TikTok Recipes - {datetime.now().strftime('%B %d, %Y')}"
    
    sent_count = 0
    failed = []
    
    for subscriber in subscribers:
        try:
            params = {
                "from": os.environ.get("FROM_EMAIL", "recipes@yourdomain.com"),
                "to": [subscriber["email"]],
                "subject": subject,
                "html": html_content
            }
            
            resend.Emails.send(params)
            sent_count += 1
            print(f"✓ Sent to {subscriber['email']}")
            
        except Exception as e:
            print(f"✗ Failed to send to {subscriber['email']}: {e}")
            failed.append(subscriber["email"])
    
    print(f"\n📧 Newsletter sent to {sent_count} subscribers")
    if failed:
        print(f"⚠️  Failed: {', '.join(failed)}")
    
    return sent_count


def main():
    """Main function to run the entire workflow"""
    print("🚀 Starting TikTok Recipe Newsletter Generator\n")
    
    # Step 1: Get trending recipe videos from TikTok
    print("📱 Step 1: Finding trending recipe videos on TikTok...")
    videos = get_trending_recipe_videos(count=5)
    print(f"   Found {len(videos)} videos\n")
    
    # Step 2: Extract recipes from each video
    print("🔍 Step 2: Extracting recipes from videos...")
    recipes = []
    for i, video in enumerate(videos, 1):
        print(f"   Processing video {i}/{len(videos)}: {video['title'][:50]}...")
        try:
            recipe = extract_recipe_from_video(video)
            if recipe:
                recipes.append(recipe)
                print(f"   ✓ Recipe extracted")
        except Exception as e:
            print(f"   ✗ Failed: {e}")
    
    print(f"\n   Successfully extracted {len(recipes)} recipes\n")
    
    if not recipes:
        print("❌ No recipes extracted. Exiting.")
        return
    
    # Step 3: Save to archive
    save_recipes_archive(recipes)
    
    # Step 4: Create HTML newsletter
    print("📰 Step 3: Building newsletter...")
    html_content = create_html_newsletter(recipes)
    
    # Save a local copy
    with open("latest_newsletter.html", "w") as f:
        f.write(html_content)
    print("   ✓ Newsletter created (saved as latest_newsletter.html)\n")
    
    # Step 5: Send to subscribers
    print("📧 Step 4: Sending emails...")
    subscribers = load_subscribers()
    
    if not subscribers:
        print("⚠️  No subscribers found. Add emails to subscribers.json")
        print("   Newsletter saved locally for preview.\n")
        return
    
    send_newsletter(html_content, subscribers)
    
    print("\n✨ Done! Newsletter sent successfully.")


if __name__ == "__main__":
    main()
