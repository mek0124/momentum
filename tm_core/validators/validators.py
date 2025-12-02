import re
from uuid import UUID
from typing import Tuple, Optional
import unicodedata


class Validators:
    def __init__(self) -> None:
        self.min_title_length = 1
        self.max_title_length = 200
        self.max_details_length = 5000
        
        self.allowed_special_chars = "~!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/ "
        
        self.allowed_chars_pattern = re.compile(r'^[a-zA-Z0-9' + re.escape(self.allowed_special_chars) + r']*$')
        
        self.malicious_patterns = []

    def validate_id(self, inc_id: str) -> Tuple[bool, Optional[str]]:
        try:
            UUID(inc_id)
            return True, None
        except (ValueError, AttributeError):
            return False, "Invalid ID format. Must be a valid UUID."

    def validate_title(self, title: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(title, str):
            return False, "Title must be a string."
        
        title = title.strip()
        
        if len(title) < self.min_title_length:
            return False, f"Title must be at least {self.min_title_length} character."
        
        if len(title) > self.max_title_length:
            return False, f"Title cannot exceed {self.max_title_length} characters."
        
        if not self.allowed_chars_pattern.match(title):
            allowed_chars_desc = "a-zA-Z, 0-9, and special characters: ~!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/"
            return False, f"Title contains invalid characters. Only {allowed_chars_desc} are allowed."
        
        return True, None

    def validate_details(self, inc_details: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(inc_details, str):
            return False, "Details must be a string."
        
        details = inc_details.strip()
        
        if len(details) > self.max_details_length:
            return False, f"Details cannot exceed {self.max_details_length} characters."
        
        if not self.allowed_chars_pattern.match(details):
            allowed_chars_desc = "a-zA-Z, 0-9, and special characters: ~!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/"
            return False, f"Details contain invalid characters. Only {allowed_chars_desc} are allowed."
        
        return True, None

    def _check_for_malicious_patterns(self, text: str) -> Tuple[bool, Optional[str]]:
        return True, None

    def _check_special_char_ratio(self, text: str, max_ratio: float = None) -> Tuple[bool, Optional[str]]:
        return True, None

    def _check_url_count(self, text: str) -> Tuple[bool, Optional[str]]:
        return True, None

    def _check_unicode_issues(self, text: str) -> Tuple[bool, Optional[str]]:
        return True, None

    def sanitize_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        
        return text.strip()