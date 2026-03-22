import pytest
from src.utils import clean_xml_to_string

def test_clean_xml_to_string_secure():
    xml_string = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<test>&xxe;</test>
"""
    result = clean_xml_to_string(xml_string)
    assert "Error parsing XML" in result

def test_clean_xml_to_string_bytes():
    xml_bytes = b"<test>hello</test>"
    result = clean_xml_to_string(xml_bytes)
    assert "test: hello" in result
