"""
End-to-end test for Blog Brain content generation.

This script tests the complete workflow:
1. Research Agent gathers information
2. SEO Strategist creates outline
3. Writer creates content
4. Editor reviews and finalizes
"""

import os
import sys
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n" + "=" * 70)
    print("BLOG BRAIN - END-TO-END CONTENT GENERATION TEST")
    print("=" * 70)
    
    # Setup environment
    print("\n📋 Setting up environment...")
    try:
        from config import settings
        
        # Set GOOGLE_API_KEY for Gemini
        os.environ['GOOGLE_API_KEY'] = settings.gemini_api_key
        
        print(f"✓ Gemini Model: {settings.gemini_model}")
        print(f"✓ API Keys configured")
        print(f"✓ Environment ready")
    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        return
    
    # Import crew
    print("\n🤖 Initializing AI Crew...")
    try:
        from crew import ContentGenerationCrew
        crew = ContentGenerationCrew()
        print("✓ Crew initialized with 4 agents")
        print("  - Research Analyst")
        print("  - SEO Strategist")
        print("  - Lead Content Writer")
        print("  - Managing Editor")
    except Exception as e:
        print(f"❌ Crew initialization failed: {e}")
        return
    
    # Define test parameters
    test_topic = "The Future of AI in Healthcare"
    test_audience = "Healthcare professionals and medical researchers"
    test_tone = "professional"
    
    print("\n" + "=" * 70)
    print("TEST PARAMETERS")
    print("=" * 70)
    print(f"📝 Topic: {test_topic}")
    print(f"👥 Audience: {test_audience}")
    print(f"🎨 Tone: {test_tone}")
    
    # Run content generation
    print("\n" + "=" * 70)
    print("STARTING CONTENT GENERATION")
    print("=" * 70)
    print("\nThis may take 2-5 minutes as agents research, strategize, write, and edit...")
    print("You'll see progress updates as each agent completes their work.\n")
    
    start_time = datetime.now()
    
    try:
        result = crew.generate_content(
            topic=test_topic,
            target_audience=test_audience,
            tone=test_tone,
            exclude_keywords=["game-changer", "revolutionary"]
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Display results
        print("\n" + "=" * 70)
        print("GENERATION RESULTS")
        print("=" * 70)
        
        if result.get('status') == 'success':
            print("✅ STATUS: SUCCESS")
            print(f"⏱️  Duration: {duration:.1f} seconds")
            
            # Extract data
            data = result.get('data', {})
            metadata = data.get('metadata', {})
            content = data.get('content', {})
            sources = data.get('sources', [])
            quality_checks = data.get('quality_checks', {})
            
            # Display metadata
            print("\n📊 METADATA:")
            print(f"  Title: {metadata.get('seo_title', 'N/A')}")
            print(f"  Description: {metadata.get('meta_description', 'N/A')[:80]}...")
            print(f"  Slug: {metadata.get('slug', 'N/A')}")
            print(f"  Word Count: {metadata.get('word_count', 0)}")
            print(f"  Read Time: {metadata.get('estimated_read_time', 'N/A')}")
            
            # Display content preview
            print("\n📝 CONTENT PREVIEW:")
            markdown = content.get('markdown_body', '')
            if markdown:
                preview = markdown[:500] + "..." if len(markdown) > 500 else markdown
                print(preview)
            
            # Display sources
            print(f"\n🔗 SOURCES: {len(sources)} citations")
            for i, source in enumerate(sources[:5], 1):
                print(f"  {i}. {source}")
            if len(sources) > 5:
                print(f"  ... and {len(sources) - 5} more")
            
            # Display quality checks
            print("\n✅ QUALITY CHECKS:")
            print(f"  AI-isms Removed: {quality_checks.get('ai_isms_removed', False)}")
            print(f"  Citations Count: {quality_checks.get('citations_count', 0)}")
            print(f"  Readability Score: {quality_checks.get('readability_score', 'N/A')}")
            print(f"  SEO Compliance: {quality_checks.get('seo_compliance', False)}")
            print(f"  Human Sounding: {quality_checks.get('human_sounding', False)}")
            
            # Save full output
            output_file = "test_output.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full output saved to: {output_file}")
            
            # Save markdown
            markdown_file = "test_output.md"
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"💾 Markdown saved to: {markdown_file}")
            
            print("\n" + "=" * 70)
            print("✅ END-TO-END TEST SUCCESSFUL!")
            print("=" * 70)
            
        else:
            print("❌ STATUS: FAILED")
            print(f"Error: {result.get('message', 'Unknown error')}")
            print(f"\nExecution time: {duration:.1f} seconds")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        
    except Exception as e:
        print(f"\n❌ ERROR DURING GENERATION:")
        print(f"   {type(e).__name__}: {str(e)}")
        
        import traceback
        print("\n📋 Full traceback:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
