"""
SEO Strategy Task Definition

Task specification for the SEO strategist to create content outlines
optimized for search rankings.
"""

from crewai import Task
from agents.strategist import create_seo_strategist
from typing import Optional


def create_strategy_task(
    topic: str,
    tone: str = "professional"
) -> Task:
    """
    Create an SEO strategy task for content planning.
    
    Args:
        topic: The blog topic to strategize for
        tone: Writing tone (professional, casual, technical, etc.)
        
    Returns:
        Configured Task instance
    """
    
    description = f"""Based on the research findings, create a comprehensive SEO-optimized 
content outline for the topic: "{topic}"

The tone should be: {tone}

Your strategy MUST include:

1. KEYWORD STRATEGY
   - Primary focus keyword (exact match from search intent)
   - 3-5 secondary keywords (semantic variations)
   - 5-10 LSI keywords (related terms Google associates with this topic)
   - Long-tail keyword opportunities

2. CONTENT STRUCTURE
   - Compelling H1 title (55-60 characters, includes focus keyword)
   - H2 and H3 heading hierarchy
   - Each section should target specific user questions
   - Logical flow from introduction to conclusion

3. FEATURED SNIPPET OPTIMIZATION
   - Identify snippet opportunities (definition, list, table, etc.)
   - Structure specific sections to win featured snippets
   - Include "what is [topic]" if applicable
   - Format content for easy extraction by Google

4. PEOPLE ALSO ASK (PAA) INTEGRATION
   - Identify 5-8 PAA questions to answer
   - Map each question to a specific section
   - Ensure concise, direct answers

5. CONTENT LENGTH & DEPTH
   - Recommended total word count (based on competitor analysis)
   - Word count per section
   - Topics that need deep coverage vs. brief mentions

6. SEO REQUIREMENTS
   - Where to place focus keyword (title, first 100 words, H2s, conclusion)
   - Internal linking opportunities (if applicable)
   - External linking strategy (authoritative sources)
   - Meta title template (55-60 chars)
   - Meta description template (150-160 chars)

7. USER ENGAGEMENT ELEMENTS
   - FAQ section structure
   - How-to steps or actionable takeaways
   - Examples or case studies to include
   - Visual content recommendations (if applicable)

STRATEGIC PRINCIPLES:
- Serve user intent FIRST, SEO optimization SECOND
- Every heading should promise value
- Structure for easy scanning (users skim before reading)
- Balance comprehensiveness with readability
- Optimize for both search engines and humans

Create an outline that the writer can follow to produce ranking content."""

    expected_output = """A complete SEO strategy document in JSON format:

{
  "seo_strategy": {
    "focus_keyword": "[primary keyword]",
    "secondary_keywords": ["keyword1", "keyword2", "keyword3"],
    "lsi_keywords": ["term1", "term2", "term3", "term4", "term5"],
    
    "meta_data": {
      "title_template": "[60-char SEO title with focus keyword]",
      "description_template": "[160-char meta description with CTA]",
      "slug": "[url-friendly-slug]"
    },
    
    "content_outline": {
      "h1": "[Main Title]",
      
      "introduction": {
        "purpose": "Hook + promise + focus keyword in first 100 words",
        "word_count": 150
      },
      
      "sections": [
        {
          "h2": "[Section Heading]",
          "purpose": "[What this section covers]",
          "target_keywords": ["keyword1", "keyword2"],
          "paa_questions": ["Question 1?"],
          "word_count": 300,
          "subsections": [
            {
              "h3": "[Subsection Heading]",
              "purpose": "[Specific point or question answered]"
            }
          ]
        }
      ],
      
      "faq_section": {
        "h2": "Frequently Asked Questions",
        "questions": [
          {
            "question": "[PAA Question]?",
            "snippet_optimization": "Format for featured snippet"
          }
        ]
      },
      
      "conclusion": {
        "h2": "Conclusion",
        "purpose": "Summarize key points + CTA + reinforce focus keyword",
        "word_count": 150
      }
    },
    
    "featured_snippet_targets": [
      {
        "type": "definition|list|table|steps",
        "section": "[Which H2 section]",
        "optimization_notes": "[How to structure for snippet]"
      }
    ],
    
    "recommended_word_count": {
      "total": 2000,
      "rationale": "[Why this length based on competitor analysis]"
    }
  }
}

The outline should be detailed enough that the writer knows exactly what to write
for each section."""

    # Create the SEO strategist agent
    agent = create_seo_strategist()
    
    # Create and return the task
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
    
    return task
