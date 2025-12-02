import re
from uuid import UUID
from typing import Tuple, Optional
import unicodedata


class Validators:
    def __init__(self) -> None:
        # Configuration for validation limits
        self.min_title_length = 1
        self.max_title_length = 200
        self.max_details_length = 5000
        
        # Allowed character pattern (letters, numbers, spaces, common punctuation)
        # Adjust based on your specific needs
        self.allowed_chars_pattern = re.compile(r'^[\w\s.,!?@#$%^&*()_+\-=\[\]{}|;:"\'<>/~`\n\r]*$')
        
        # Suspicious patterns to detect
        self.malicious_patterns = [
            (re.compile(r'(?i)<script[^>]*>'), "Script tags are not allowed"),
            (re.compile(r'javascript:'), "JavaScript protocol is not allowed"),
            (re.compile(r'(?i)data:[^;]+;base64,'), "Base64 data URLs are not allowed"),
            (re.compile(r'on\w+\s*='), "HTML event handlers are not allowed"),
            (re.compile(r'(?i)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|OR\s+1=1|--|;|\/\*|\*\/)'), 
             "SQL keywords detected"),
            # Unicode bidirectional override characters
            (re.compile(r'[\u202e\u202d\u2066\u2067\u2068\u2069]'), 
             "Bidirectional text override characters are not allowed"),
            # Null bytes and other control characters (except common whitespace)
            (re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]'), 
             "Control characters are not allowed"),
        ]
        
        # Maximum allowed percentage of special characters
        self.max_special_char_ratio = 0.3
        
        # Maximum number of URLs allowed in details
        self.max_urls_allowed = 3
        
        # URL detection pattern
        self.url_pattern = re.compile(r'(https?://|www\.)[^\s]+', re.IGNORECASE)

    def validate_id(self, inc_id: str) -> Tuple[bool, Optional[str]]:
        """Validate UUID format."""
        try:
            UUID(inc_id)
            return True, None
        except (ValueError, AttributeError):
            return False, "Invalid ID format. Must be a valid UUID."

    def validate_title(self, title: str) -> Tuple[bool, Optional[str]]:
        """Validate task title."""
        if not isinstance(title, str):
            return False, "Title must be a string."
        
        # Trim whitespace
        title = title.strip()
        
        # Length validation
        if len(title) < self.min_title_length:
            return False, f"Title must be at least {self.min_title_length} character."
        if len(title) > self.max_title_length:
            return False, f"Title cannot exceed {self.max_title_length} characters."
        
        # Basic character validation
        if not self.allowed_chars_pattern.match(title):
            return False, "Title contains invalid characters. Only letters, numbers, spaces, and common punctuation are allowed."
        
        # Check for malicious patterns
        malicious_check = self._check_for_malicious_patterns(title)
        if not malicious_check[0]:
            return malicious_check
        
        # Check for excessive special characters
        special_check = self._check_special_char_ratio(title)
        if not special_check[0]:
            return special_check
        
        # Unicode normalization check
        unicode_check = self._check_unicode_issues(title)
        if not unicode_check[0]:
            return unicode_check
        
        return True, None

    def validate_details(self, inc_details: str) -> Tuple[bool, Optional[str]]:
        """Validate task details."""
        if not isinstance(inc_details, str):
            return False, "Details must be a string."
        
        # Trim whitespace
        details = inc_details.strip()
        
        # Length validation
        if len(details) > self.max_details_length:
            return False, f"Details cannot exceed {self.max_details_length} characters."
        
        # Basic character validation (with more leniency than title)
        if not self.allowed_chars_pattern.match(details):
            return False, "Details contain invalid characters. Only letters, numbers, spaces, and common punctuation are allowed."
        
        # Check for malicious patterns
        malicious_check = self._check_for_malicious_patterns(details)
        if not malicious_check[0]:
            return malicious_check
        
        # Check for excessive URLs
        url_check = self._check_url_count(details)
        if not url_check[0]:
            return url_check
        
        # Check for excessive special characters
        special_check = self._check_special_char_ratio(details, max_ratio=0.4)  # More lenient for details
        if not special_check[0]:
            return special_check
        
        # Unicode normalization check
        unicode_check = self._check_unicode_issues(details)
        if not unicode_check[0]:
            return unicode_check
        
        return True, None

    def _check_for_malicious_patterns(self, text: str) -> Tuple[bool, Optional[str]]:
        """Check for malicious patterns in text."""
        for pattern, error_message in self.malicious_patterns:
            if pattern.search(text):
                return False, error_message
        return True, None

    def _check_special_char_ratio(self, text: str, max_ratio: float = None) -> Tuple[bool, Optional[str]]:
        """Check if text has excessive special characters."""
        if max_ratio is None:
            max_ratio = self.max_special_char_ratio
        
        if not text:
            return True, None
        
        # Count non-alphanumeric, non-space characters
        special_char_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
        ratio = special_char_count / len(text)
        
        if ratio > max_ratio:
            return False, f"Too many special characters ({(ratio*100):.1f}%). Maximum allowed is {(max_ratio*100):.0f}%."
        
        return True, None

    def _check_url_count(self, text: str) -> Tuple[bool, Optional[str]]:
        """Check for excessive URLs in text."""
        urls = self.url_pattern.findall(text)
        if len(urls) > self.max_urls_allowed:
            return False, f"Too many URLs ({len(urls)}). Maximum allowed is {self.max_urls_allowed}."
        return True, None

    def _check_unicode_issues(self, text: str) -> Tuple[bool, Optional[str]]:
        """Check for Unicode-related issues."""
        # Normalize to NFC form
        normalized = unicodedata.normalize('NFC', text)
        
        # Check for mixed script (could be used for homoglyph attacks)
        # This is a simplified check - consider using libraries like 'charset-normalizer' for production
        if text != normalized:
            # Check for suspicious character combinations
            # Add more specific checks based on your requirements
            pass
        
        return True, None

    def sanitize_text(self, text: str) -> str:
        """Sanitize text by removing malicious content while preserving safe content."""
        if not isinstance(text, str):
            return ""
        
        # Remove null bytes and control characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        
        # Remove script tags and content (basic)
        text = re.sub(r'(?i)<script[^>]*>.*?</script>', '', text)
        
        # Remove other dangerous patterns
        text = re.sub(r'(?i)javascript:', '', text)
        text = re.sub(r'(?i)data:[^;]+;base64,', '', text)
        text = re.sub(r'on\w+\s*=', '', text)
        
        # Remove bidirectional override characters
        text = re.sub(r'[\u202e\u202d\u2066\u2067\u2068\u2069]', '', text)
        
        # Normalize Unicode
        text = unicodedata.normalize('NFC', text)
        
        return text.strip()