"""
Knowledge Base Loader
Loads and searches the Islamic finance knowledge base
"""
import json
import re
from typing import List, Dict, Any, Optional
import requests

from config import GITHUB_REPO, KNOWLEDGE_FILE


class KnowledgeLoader:
    """Loads and manages the knowledge base."""
    
    def __init__(self):
        self.knowledge: Dict[str, Any] = {}
        self.glossary: Dict[str, Dict] = {}
        self.sections: Dict[str, str] = {}
        
    def load(self) -> None:
        """Load knowledge base from GitHub or local file."""
        try:
            # Try to load from GitHub first
            self._load_from_github()
        except Exception as e:
            print(f"Could not load from GitHub: {e}")
            # Fallback: create basic structure
            self._create_basic_structure()
    
    def _load_from_github(self) -> None:
        """Load knowledge base from GitHub repository."""
        base_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/"
        
        files = [
            "01-fundamentals/01-core-principles.md",
            "02-contracts/01-contract-types.md",
            "03-schools-of-fiqh/01-madhabs-overview.md",
            "04-regulatory-standards/01-standards-overview.md",
            "05-modern-products/01-products-overview.md",
            "06-scholars-fatwas/01-key-scholars.md",
            "07-case-studies/01-global-cases.md",
            "08-russia-specific/01-russia-context.md",
            "09-glossary/01-glossary-3lang.md",
            "10-comparative/01-islamic-vs-conventional.md",
            "README.md"
        ]
        
        for file_path in files:
            try:
                url = base_url + file_path
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    content = response.text
                    section_name = file_path.split('/')[-1].replace('.md', '')
                    self.sections[section_name] = content
                    
                    # Parse glossary if it's the glossary file
                    if 'glossary' in file_path:
                        self._parse_glossary(content)
                        
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    def _create_basic_structure(self) -> None:
        """Create basic structure if GitHub is not available."""
        self.sections = {
            "core_principles": "Fundamentals of Islamic finance",
            "contracts": "Islamic finance contracts",
            # Add more as needed
        }
    
    def _parse_glossary(self, content: str) -> None:
        """Parse glossary from markdown content."""
        # Simple parsing - can be improved
        lines = content.split('\n')
        current_entry = None
        
        for line in lines:
            # Look for term entries (| Term | English | Arabic |)
            if line.startswith('|') and not line.startswith('|---'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 4:
                    term_ru = parts[0]
                    term_en = parts[1]
                    term_ar = parts[2]
                    definition = parts[3] if len(parts) > 3 else ""
                    
                    if term_ru and term_ru not in ['Русский', 'Термин']:
                        self.glossary[term_ru.lower()] = {
                            'term': term_ru,
                            'english': term_en,
                            'arabic': term_ar,
                            'definition': definition
                        }
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """Search knowledge base for query."""
        results = []
        query_lower = query.lower()
        
        for section_name, content in self.sections.items():
            if query_lower in content.lower():
                # Find relevant snippet
                idx = content.lower().find(query_lower)
                start = max(0, idx - 100)
                end = min(len(content), idx + 200)
                snippet = content[start:end]
                
                results.append({
                    'title': section_name.replace('_', ' ').title(),
                    'snippet': snippet,
                    'source': section_name
                })
        
        return results
    
    def get_glossary_entry(self, term: str) -> Optional[Dict]:
        """Get glossary entry for term."""
        term_lower = term.lower()
        
        # Exact match
        if term_lower in self.glossary:
            return self.glossary[term_lower]
        
        # Partial match
        for key, entry in self.glossary.items():
            if term_lower in key or key in term_lower:
                return entry
        
        return None
    
    def get_relevant_context(self, query: str, max_length: int = 2000) -> str:
        """Get relevant context for AI based on query."""
        context_parts = []
        query_lower = query.lower()
        
        # Define keywords for each section
        keywords = {
            'core_principles': ['риба', 'гарар', 'майсир', 'основы', 'принципы', 'запрет'],
            'contracts': ['мурабаха', 'иджара', 'мудараба', 'мушарака', 'контракт', 'салам'],
            'madhabs': ['мазхаб', 'ханафит', 'маликит', 'шафиит', 'ханбалит', 'школа'],
            'standards': ['aaoifi', 'ifsb', 'регулятор', 'стандарт', 'базель'],
            'products': ['сукук', 'такафул', 'фонд', 'продукт', 'ипотека'],
            'scholars': ['усмани', 'кардави', 'учёный', 'фатва', 'шейх'],
            'cases': ['пакистан', 'малайзия', 'gcc', 'турция', 'кейс', 'мезан'],
            'russia': ['россия', 'татарстан', 'пилот', 'казань', 'российский'],
            'comparative': ['сравнение', 'отличие', 'vs', 'против', 'разница'],
            'glossary': ['термин', 'определение', 'что такое', 'значит']
        }
        
        # Find relevant sections
        for section_name, section_keywords in keywords.items():
            if any(kw in query_lower for kw in section_keywords):
                if section_name in self.sections:
                    content = self.sections[section_name]
                    # Get relevant part
                    context_parts.append(f"=== {section_name.upper()} ===\n{content[:500]}...")
        
        # If no specific section found, add general info
        if not context_parts and 'core_principles' in self.sections:
            context_parts.append(self.sections['core_principles'][:1000])
        
        result = '\n\n'.join(context_parts)
        return result[:max_length]
