"""
Newsletter Builder
Creates beautiful HTML email newsletters from recipe data
"""

from datetime import datetime


def create_html_newsletter(recipes):
    """
    Creates an HTML email newsletter from recipe data
    
    Args:
        recipes: List of recipe dictionaries
    
    Returns:
        HTML string
    """
    
    # Generate recipe cards HTML
    recipe_cards = ""
    for i, recipe in enumerate(recipes, 1):
        source = recipe.get('source', {})
        
        # Create ingredients list
        ingredients_html = "".join([
            f"<li>{ing}</li>" for ing in recipe.get('ingredients', [])
        ])
        
        # Create instructions list
        instructions_html = "".join([
            f"<li>{inst}</li>" for inst in recipe.get('instructions', [])
        ])
        
        # Create tips if available
        tips_html = ""
        if recipe.get('tips'):
            tips_list = "".join([f"<li>{tip}</li>" for tip in recipe['tips']])
            tips_html = f"""
            <div style="background-color: #fff9e6; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <h4 style="margin-top: 0; color: #f59e0b;">💡 Tips</h4>
                <ul style="margin: 0; padding-left: 20px;">
                    {tips_list}
                </ul>
            </div>
            """
        
        # Creator's TikTok profile URL
        creator_username = source.get('author', 'Unknown')
        creator_url = f"https://www.tiktok.com/@{creator_username}"
        
        recipe_card = f"""
        <div style="background-color: white; border-radius: 12px; padding: 25px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="border-left: 4px solid #10b981; padding-left: 15px; margin-bottom: 20px;">
                <h2 style="margin: 0 0 10px 0; color: #1f2937;">#{i} {recipe.get('title', 'Untitled Recipe')}</h2>
                <div style="display: flex; align-items: center; gap: 10px; margin: 10px 0;">
                    <div style="background: linear-gradient(45deg, #ff0050, #00f2ea); padding: 8px 12px; border-radius: 20px;">
                        <a href="{creator_url}" style="color: white; text-decoration: none; font-weight: 600; font-size: 14px;">
                            📱 @{creator_username}
                        </a>
                    </div>
                    <span style="color: #6b7280; font-size: 14px;">
                        ❤️ {source.get('likes', 0):,} likes • 👁️ {source.get('views', 0):,} views
                    </span>
                </div>
            </div>
            
            <p style="color: #4b5563; line-height: 1.6; font-size: 16px;">{recipe.get('description', '')}</p>
            
            <div style="display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap;">
                <div style="background-color: #f3f4f6; padding: 10px 15px; border-radius: 6px;">
                    <span style="color: #6b7280; font-size: 13px;">⏱️ Prep:</span>
                    <strong style="color: #1f2937;">{recipe.get('prep_time', 'N/A')}</strong>
                </div>
                <div style="background-color: #f3f4f6; padding: 10px 15px; border-radius: 6px;">
                    <span style="color: #6b7280; font-size: 13px;">🍳 Cook:</span>
                    <strong style="color: #1f2937;">{recipe.get('cook_time', 'N/A')}</strong>
                </div>
                <div style="background-color: #f3f4f6; padding: 10px 15px; border-radius: 6px;">
                    <span style="color: #6b7280; font-size: 13px;">🍽️ Serves:</span>
                    <strong style="color: #1f2937;">{recipe.get('servings', 'N/A')}</strong>
                </div>
            </div>
            
            <div style="margin: 25px 0;">
                <h3 style="color: #1f2937; margin-bottom: 15px;">🛒 Ingredients</h3>
                <ul style="color: #4b5563; line-height: 1.8; padding-left: 20px;">
                    {ingredients_html}
                </ul>
            </div>
            
            <div style="margin: 25px 0;">
                <h3 style="color: #1f2937; margin-bottom: 15px;">👨‍🍳 Instructions</h3>
                <ol style="color: #4b5563; line-height: 1.8; padding-left: 20px;">
                    {instructions_html}
                </ol>
            </div>
            
            {tips_html}
            
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                <a href="{source.get('url', '#')}" 
                   style="display: inline-block; background-color: #10b981; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 6px; font-weight: 600;">
                    Watch Original Video by @{creator_username} →
                </a>
                <p style="color: #9ca3af; font-size: 12px; margin-top: 10px;">
                    ❤️ Support the creator by liking and following on TikTok!
                </p>
            </div>
        </div>
        """
        
        recipe_cards += recipe_card
    
    # Complete HTML template
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Top TikTok Recipes</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f9fafb; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <!-- Header -->
            <div style="text-align: center; padding: 40px 20px;">
                <h1 style="color: #1f2937; margin: 0; font-size: 36px;">🍳 TikTok Recipe Roundup</h1>
                <p style="color: #6b7280; margin: 10px 0 0 0; font-size: 18px;">
                    Top 5 Trending Recipes • {datetime.now().strftime('%B %d, %Y')}
                </p>
            </div>
            
            <!-- Recipes -->
            {recipe_cards}
            
            <!-- Footer -->
            <div style="text-align: center; padding: 40px 20px; color: #9ca3af; font-size: 14px;">
                <p style="margin-bottom: 15px;">
                    ⭐ All recipes are credited to their original TikTok creators.<br>
                    Please support them by watching, liking, and following!
                </p>
                <p>You're receiving this because you subscribed to TikTok Recipe Newsletter</p>
                <p style="margin-top: 10px;">
                    Made with ❤️ by your friendly recipe bot
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html
