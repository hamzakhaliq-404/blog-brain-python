"""
Unit tests for AI-focused search tools.

Tests the enhanced search functionality including:
- AI domain search with credible source filtering
- Multi-source research with diversity
- Claim verification with multiple sources
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from tools.search_tools import (
    ai_domain_search,
    multi_source_research,
    verify_ai_claim,
    extract_domain
)
from research_config.ai_credible_sources import (
    AI_CREDIBLE_SOURCES,
    SOURCE_PRIORITY,
    get_category_for_domain,
    get_priority_for_domain
)


class TestAICredibleSources:
    """Test AI credible sources configuration."""
    
    def test_all_categories_exist(self):
        """Verify all expected categories are defined."""
        expected_categories = ['academic', 'government', 'company_research', 'industry', 'ai_blogs']
        for category in expected_categories:
            assert category in AI_CREDIBLE_SOURCES
            assert len(AI_CREDIBLE_SOURCES[category]) > 0
    
    def test_source_priorities(self):
        """Verify source priorities are correctly ordered."""
        assert SOURCE_PRIORITY['academic'] == 1.0  # Highest
        assert SOURCE_PRIORITY['government'] == 0.9
        assert SOURCE_PRIORITY['company_research'] == 0.8
        assert SOURCE_PRIORITY['industry'] == 0.6
        assert SOURCE_PRIORITY['ai_blogs'] == 0.5  # Lowest
    
    def test_academic_sources_include_arxiv(self):
        """Verify academic sources include key AI repositories."""
        academic = AI_CREDIBLE_SOURCES['academic']
        assert 'arxiv.org' in academic
        assert any('nips' in domain or 'neurips' in domain for domain in academic)
    
    def test_company_research_includes_major_labs(self):
        """Verify company research includes major AI labs."""
        company = AI_CREDIBLE_SOURCES['company_research']
        assert any('openai' in domain for domain in company)
        assert any('deepmind' in domain for domain in company)
    
    def test_get_category_for_domain(self):
        """Test domain categorization."""
        assert get_category_for_domain('arxiv.org') == 'academic'
        assert get_category_for_domain('openai.com') == 'company_research'
        assert get_category_for_domain('nsf.gov') == 'government'
        assert get_category_for_domain('techcrunch.com') == 'industry'
        assert get_category_for_domain('unknown-domain.com') == ''
    
    def test_get_priority_for_domain(self):
        """Test priority scoring for domains."""
        assert get_priority_for_domain('arxiv.org') == 1.0
        assert get_priority_for_domain('openai.com') == 0.8
        assert get_priority_for_domain('unknown.com') == 0.3


class TestExtractDomain:
    """Test domain extraction helper."""
    
    def test_extract_domain_basic(self):
        """Test basic domain extraction."""
        assert extract_domain('https://arxiv.org/paper.pdf') == 'arxiv.org'
        assert extract_domain('http://www.openai.com/research') == 'openai.com'
    
    def test_extract_domain_removes_www(self):
        """Test that www prefix is removed."""
        assert extract_domain('https://www.techcrunch.com/article') == 'techcrunch.com'
    
    def test_extract_domain_handles_invalid(self):
        """Test handling of invalid URLs."""
        assert extract_domain('not-a-url') == ''
        assert extract_domain('') == ''


class TestAIDomainSearch:
    """Test AI domain search functionality."""
    
    @patch('tools.search_tools.google_search')
    def test_ai_domain_search_constructs_query(self, mock_google_search):
        """Test that AI domain search constructs proper site: operators."""
        mock_google_search.return_value = []
        
        ai_domain_search("transformer architecture", categories=["academic"])
        
        # Verify google_search was called
        assert mock_google_search.called
        call_args = mock_google_search.call_args[0]
        query = call_args[0]
        
        # Query should contain site: operators
        assert 'site:' in query
        assert 'transformer architecture' in query
    
    @patch('tools.search_tools.google_search')
    def test_ai_domain_search_filters_results(self, mock_google_search):
        """Test that results are filtered to credible domains only."""
        # Mock search results with mixed domains
        mock_google_search.return_value = [
            {'title': 'Academic Paper', 'link': 'https://arxiv.org/paper1', 'snippet': 'Test', 'position': 1},
            {'title': 'Spam Site', 'link': 'https://spam-site.com/article', 'snippet': 'Test', 'position': 2},
            {'title': 'Research Blog', 'link': 'https://openai.com/research1', 'snippet': 'Test', 'position': 3}
        ]
        
        results = ai_domain_search("AI research", categories=["academic", "company_research"])
        
        # Only credible domains should be in results
        domains = [extract_domain(r['link']) for r in results]
        assert 'arxiv.org' in domains
        assert 'openai.com' in domains
        assert 'spam-site.com' not in domains
    
    @patch('tools.search_tools.google_search')
    def test_ai_domain_search_adds_credibility_scores(self, mock_google_search):
        """Test that credibility scores are added to results."""
        mock_google_search.return_value = [
            {'title': 'Paper', 'link': 'https://arxiv.org/paper1', 'snippet': 'Test', 'position': 1}
        ]
        
        results = ai_domain_search("AI", categories=["academic"])
        
        assert len(results) > 0
        assert 'credibility_score' in results[0]
        assert 'source_category' in results[0]
        assert results[0]['credibility_score'] == 1.0  # Academic source
        assert results[0]['source_category'] == 'academic'
    
    @patch('tools.search_tools.google_search')
    def test_ai_domain_search_sorts_by_credibility(self, mock_google_search):
        """Test that results are sorted by credibility score."""
        mock_google_search.return_value = [
            {'title': 'Blog', 'link': 'https://towardsdatascience.com/article', 'snippet': 'Test', 'position': 1},
            {'title': 'Paper', 'link': 'https://arxiv.org/paper', 'snippet': 'Test', 'position': 2}
        ]
        
        results = ai_domain_search("AI", categories=["academic", "ai_blogs"])
        
        # Academic should come first (higher credibility)
        assert results[0]['source_category'] == 'academic'
        assert results[0]['credibility_score'] >= results[1]['credibility_score']


class TestMultiSourceResearch:
    """Test multi-source research functionality."""
    
    @patch('tools.search_tools.ai_domain_search')
    def test_multi_source_searches_all_categories(self, mock_ai_search):
        """Test that multi-source research queries all categories."""
        mock_ai_search.return_value = []
        
        multi_source_research("AI research", num_results=20)
        
        # Should call ai_domain_search for multiple categories
        assert mock_ai_search.call_count >= 3  # At least academic, company_research, government
    
    @patch('tools.search_tools.ai_domain_search')
    def test_multi_source_deduplicates_urls(self, mock_ai_search):
        """Test that duplicate URLs are removed."""
        # Return same URL from different category searches
        duplicate_result = {'title': 'Article', 'link': 'https://arxiv.org/same', 'snippet': 'Test', 
                           'credibility_score': 1.0, 'source_category': 'academic'}
        mock_ai_search.return_value = [duplicate_result]
        
        results = multi_source_research("AI", num_results=20)
        
        # Check no duplicate URLs
        urls = [r['link'] for r in results]
        assert len(urls) == len(set(urls))


class TestVerifyAIClaim:
    """Test AI claim verification functionality."""
    
    @patch('tools.search_tools.ai_domain_search')
    def test_verify_claim_checks_multiple_sources(self, mock_ai_search):
        """Test that claim verification checks minimum sources."""
        mock_ai_search.return_value = [
            {'title': 'Source 1', 'link': 'https://arxiv.org/1', 'snippet': 'Supporting evidence', 
             'credibility_score': 1.0, 'source_category': 'academic'},
            {'title': 'Source 2', 'link': 'https://openai.com/1', 'snippet': 'Supporting evidence',
             'credibility_score': 0.8, 'source_category': 'company_research'},
            {'title': 'Source 3', 'link': 'https://nsf.gov/1', 'snippet': 'Supporting evidence',
             'credibility_score': 0.9, 'source_category': 'government'}
        ]
        
        result = verify_ai_claim("AI claim to verify", min_sources=3)
        
        assert result['sources_checked'] >= 3
        assert result['verification_status'] in ['Verified', 'Partially Verified', 'Unverified', 'Contradicted']
    
    @patch('tools.search_tools.ai_domain_search')
    def test_verify_claim_returns_verified_status(self, mock_ai_search):
        """Test that high-quality sources return Verified status."""
        # High credibility sources
        mock_ai_search.return_value = [
            {'title': f'Source {i}', 'link': f'https://arxiv.org/{i}', 'snippet': 'Evidence', 
             'credibility_score': 1.0, 'source_category': 'academic'}
            for i in range(3)
        ]
        
        result = verify_ai_claim("Well-supported AI claim")
        
        assert result['verification_status'] == 'Verified'
        assert result['confidence'] == 'High'
    
    @patch('tools.search_tools.ai_domain_search')
    def test_verify_claim_returns_unverified_insufficient_sources(self, mock_ai_search):
        """Test that insufficient sources return Unverified."""
        mock_ai_search.return_value = [
            {'title': 'Only Source', 'link': 'https://arxiv.org/1', 'snippet': 'Evidence',
             'credibility_score': 1.0, 'source_category': 'academic'}
        ]
        
        result = verify_ai_claim("Claim with few sources", min_sources=3)
        
        assert result['verification_status'] == 'Unverified'
        assert result['confidence'] == 'Low'
    
    @patch('tools.search_tools.ai_domain_search')
    def test_verify_claim_includes_evidence(self, mock_ai_search):
        """Test that evidence is included in verification result."""
        mock_ai_search.return_value = [
            {'title': 'Source', 'link': 'https://arxiv.org/1', 'snippet': 'Test evidence',
             'credibility_score': 1.0, 'source_category': 'academic'}
        ]
        
        result = verify_ai_claim("Test claim")
        
        assert 'evidence' in result
        assert len(result['evidence']) > 0
        assert 'title' in result['evidence'][0]
        assert 'url' in result['evidence'][0]
        assert 'snippet' in result['evidence'][0]


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
