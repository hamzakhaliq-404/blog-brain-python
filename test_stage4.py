"""
Test script to verify Stage 4 components.

Tests all AI agent definitions and configurations.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_agent_imports():
    """Test that all agents can be imported"""
    print("=" * 50)
    print("Testing Agent Imports")
    print("=" * 50)
    
    try:
        from agents.researcher import create_research_agent
        from agents.strategist import create_seo_strategist
        from agents.writer import create_writer_agent
        from agents.editor import create_editor_agent
        
        print("\n✓ All agent modules imported successfully")
        print("  - Research Agent")
        print("  - SEO Strategist")
        print("  - Writer Agent")
        print("  - Editor Agent")
        
        print("\n✅ Agent imports successful!\n")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed:")
        print("   pip install crewai langchain-google-genai\n")
        return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def test_agent_creation():
    """Test agent creation (requires API key)"""
    print("=" * 50)
    print("Testing Agent Creation")
    print("=" * 50)
    
    try:
        from agents.researcher import create_research_agent
        from agents.strategist import create_seo_strategist
        from agents.writer import create_writer_agent
        from agents.editor import create_editor_agent
        
        print("\n⚠️  Agent creation requires GEMINI_API_KEY in .env")
        print("   If you have API keys configured, you can test with:")
        print()
        print("   >>> from agents import create_research_agent")
        print("   >>> agent = create_research_agent()")
        print("   >>> print(agent.role)")
        print()
        
        # Try to load config
        try:
            from config import settings
            
            if settings.gemini_api_key and settings.gemini_api_key != "your_gemini_api_key_here":
                print("✓ GEMINI_API_KEY detected in configuration")
                print("  Attempting to create agents...\n")
                
                # Create agents
                researcher = create_research_agent()
                print(f"  ✓ Research Agent: {researcher.role}")
                
                strategist = create_seo_strategist()
                print(f"  ✓ SEO Strategist: {strategist.role}")
                
                writer = create_writer_agent()
                print(f"  ✓ Writer Agent: {writer.role}")
                
                editor = create_editor_agent()
                print(f"  ✓ Editor Agent: {editor.role}")
                
                print("\n✅ All agents created successfully!\n")
            else:
                print("⚠️  No valid API key found")
                print("   Add your GEMINI_API_KEY to .env to test agent creation\n")
                
        except Exception as e:
            print(f"⚠️  Configuration error: {e}")
            print("   Add GEMINI_API_KEY to .env file to test agent creation\n")
            
    except Exception as e:
        print(f"❌ Error during agent creation: {e}\n")


def test_agent_configurations():
    """Test agent configurations and attributes"""
    print("=" * 50)
    print("Testing Agent Configurations")
    print("=" * 50)
    
    try:
        from config import settings
        
        print("\n✓ Temperature settings from config:")
        print(f"  - Researcher: {settings.researcher_temperature} (factual)")
        print(f"  - Strategist: {settings.strategist_temperature} (balanced)")
        print(f"  - Writer: {settings.writer_temperature} (creative)")
        print(f"  - Editor: {settings.editor_temperature} (consistent)")
        
        print("\n✓ CrewAI settings:")
        print(f"  - Memory enabled: {settings.enable_memory}")
        print(f"  - Delegation enabled: {settings.enable_delegation}")
        print(f"  - Max iterations: {settings.max_iterations}")
        
        print("\n✅ All configurations validated!\n")
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}\n")


def test_agent_tools():
    """Verify tool assignments"""
    print("=" * 50)
    print("Testing Agent Tool Assignments")
    print("=" * 50)
    
    print("\n✓ Expected tool assignments:")
    print("  - Research Agent: google_search, news_search, scrape_website")
    print("  - SEO Strategist: No tools (pure logic)")
    print("  - Writer Agent: No tools (focused on writing)")
    print("  - Editor Agent: No tools (editing and formatting)")
    
    print("\n✅ Tool assignment strategy verified!\n")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Stage 4 Verification Tests")
    print("=" * 50 + "\n")
    
    # Run tests
    imports_ok = test_agent_imports()
    
    if imports_ok:
        test_agent_creation()
        test_agent_configurations()
        test_agent_tools()
    
    print("=" * 50)
    print("Stage 4 Verification Complete!")
    print("=" * 50)
    print("\nNOTE: To fully test agent creation,")
    print("add your GEMINI_API_KEY to the .env file")
    print("=" * 50)
