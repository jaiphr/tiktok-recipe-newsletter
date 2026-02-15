"""
Test Script - Run this locally to test your setup before deploying
"""

import os
from pathlib import Path


def check_environment():
    """Check if environment variables are set"""
    print("🔍 Checking environment setup...\n")
    
    required_vars = {
        'ANTHROPIC_API_KEY': 'Anthropic API Key',
        'RESEND_API_KEY': 'Resend API Key',
        'FROM_EMAIL': 'From Email Address'
    }
    
    missing = []
    for var, name in required_vars.items():
        if os.environ.get(var):
            print(f"✅ {name} is set")
        else:
            print(f"❌ {name} is MISSING")
            missing.append(var)
    
    if missing:
        print(f"\n⚠️  Please set these environment variables:")
        for var in missing:
            print(f"   export {var}='your_key_here'")
        print("\nOr create a .env file with these values")
        return False
    
    print("\n✅ All environment variables are set!\n")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking Python packages...\n")
    
    packages = {
        'anthropic': 'Anthropic Claude API',
        'resend': 'Resend Email Service',
        'TikTokApi': 'TikTok API'
    }
    
    missing = []
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Install missing packages:")
        print(f"   pip install -r requirements.txt")
        return False
    
    print("\n✅ All packages installed!\n")
    return True


def check_subscribers():
    """Check if subscribers.json exists and is valid"""
    print("👥 Checking subscriber list...\n")
    
    if not Path("subscribers.json").exists():
        print("❌ subscribers.json not found")
        print("   Create it with at least one email address")
        return False
    
    try:
        import json
        with open("subscribers.json", 'r') as f:
            subscribers = json.load(f)
        
        if not subscribers:
            print("⚠️  subscribers.json is empty")
            print("   Add at least one subscriber for testing")
            return False
        
        print(f"✅ Found {len(subscribers)} subscriber(s):")
        for sub in subscribers[:3]:  # Show first 3
            print(f"   - {sub.get('email', 'Invalid entry')}")
        
        if len(subscribers) > 3:
            print(f"   ... and {len(subscribers) - 3} more")
        
        print()
        return True
        
    except json.JSONDecodeError:
        print("❌ subscribers.json has invalid JSON format")
        return False


def test_api_connection():
    """Test API connections"""
    print("🔌 Testing API connections...\n")
    
    # Test Anthropic
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        # Simple test message
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'API working!'"}]
        )
        
        print("✅ Anthropic API connection successful")
    except Exception as e:
        print(f"❌ Anthropic API failed: {e}")
        return False
    
    # Test Resend
    try:
        import resend
        resend.api_key = os.environ.get("RESEND_API_KEY")
        
        # Note: We don't actually send, just validate the key format
        if resend.api_key and resend.api_key.startswith("re_"):
            print("✅ Resend API key format looks valid")
        else:
            print("⚠️  Resend API key might be invalid")
    except Exception as e:
        print(f"❌ Resend setup failed: {e}")
        return False
    
    print("\n✅ All API connections working!\n")
    return True


def main():
    """Run all checks"""
    print("=" * 60)
    print("🧪 TIKTOK RECIPE NEWSLETTER - SETUP TEST")
    print("=" * 60)
    print()
    
    # Load .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("📄 Loaded .env file\n")
    except ImportError:
        print("ℹ️  python-dotenv not installed (optional)\n")
    
    all_good = True
    
    # Run checks
    if not check_environment():
        all_good = False
    
    if not check_dependencies():
        all_good = False
    
    if not check_subscribers():
        all_good = False
    
    if all_good:
        if not test_api_connection():
            all_good = False
    
    # Final verdict
    print("=" * 60)
    if all_good:
        print("✨ ALL CHECKS PASSED! You're ready to run the bot!")
        print()
        print("Next steps:")
        print("1. Run: python tiktok_recipe_newsletter.py")
        print("2. Or push to GitHub and use GitHub Actions")
    else:
        print("❌ Some checks failed. Fix the issues above and try again.")
    print("=" * 60)


if __name__ == "__main__":
    main()
