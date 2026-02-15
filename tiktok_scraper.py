"""
TikTok Video Scraper
Finds trending recipe videos using TikTok's unofficial API
"""

from TikTokApi import TikTokApi
import asyncio


def get_trending_recipe_videos(count=5):
    """
    Fetches trending recipe videos from TikTok
    
    Args:
        count: Number of videos to fetch (default 5)
    
    Returns:
        List of video data dictionaries
    """
    
    async def fetch_videos():
        # Initialize TikTok API (no authentication needed for public videos)
        async with TikTokApi() as api:
            await api.create_sessions(num_sessions=1, sleep_after=3)
            
            videos = []
            
            # Search for recipe-related hashtags
            # We'll try multiple popular recipe hashtags to get variety
            hashtags = ['recipe', 'cooking', 'foodtok', 'easyrecipe', 'recipetiktok']
            
            for hashtag in hashtags:
                try:
                    # Get videos for this hashtag
                    tag = api.hashtag(name=hashtag)
                    
                    async for video in tag.videos(count=count):
                        video_data = {
                            'id': video.id,
                            'title': video.desc if video.desc else "Untitled Recipe",
                            'author': video.author.username,
                            'video_url': f"https://www.tiktok.com/@{video.author.username}/video/{video.id}",
                            'likes': video.stats.digg_count,
                            'views': video.stats.play_count,
                            'shares': video.stats.share_count,
                            'download_url': video.video.download_addr,
                            'caption': video.desc,
                            'hashtags': [tag.get('name', '') for tag in (video.challenges or [])],
                            'music': video.music.title if video.music else None,
                        }
                        
                        videos.append(video_data)
                        
                        # Stop if we have enough videos
                        if len(videos) >= count:
                            break
                    
                    if len(videos) >= count:
                        break
                        
                except Exception as e:
                    print(f"   Warning: Could not fetch from #{hashtag}: {e}")
                    continue
            
            # Sort by engagement (likes + shares)
            videos.sort(
                key=lambda v: v['likes'] + v['shares'], 
                reverse=True
            )
            
            return videos[:count]
    
    # Run the async function
    return asyncio.run(fetch_videos())


def download_video(video_url, save_path):
    """
    Downloads a TikTok video to local storage
    
    Args:
        video_url: URL of the video to download
        save_path: Path where video should be saved
    """
    import requests
    
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return save_path


def get_video_comments(video_id, max_comments=50):
    """
    Fetches comments from a TikTok video
    
    Args:
        video_id: TikTok video ID
        max_comments: Maximum number of comments to fetch
    
    Returns:
        List of comment dictionaries
    """
    
    async def fetch_comments():
        async with TikTokApi() as api:
            await api.create_sessions(num_sessions=1, sleep_after=3)
            
            video = api.video(id=video_id)
            comments = []
            
            async for comment in video.comments(count=max_comments):
                comments.append({
                    'text': comment.text,
                    'author': comment.user.username,
                    'likes': comment.digg_count,
                })
            
            return comments
    
    return asyncio.run(fetch_comments())
