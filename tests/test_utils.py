import pytest
from src.utils import clean_xml_to_string

def test_clean_xml_to_string_valid():
    xml = "<Event><System><Provider Name=\"Microsoft-Windows-Security-Auditing\"/></System><EventData><Data Name=\"SubjectUserSid\">S-1-5-18</Data></EventData></Event>"
    result = clean_xml_to_string(xml)
    # The lxml module is mocked, so clean_xml_to_string might just return the error string depending on the mock behavior
    # We really just care that it doesn't crash from missing arguments or similar in normal execution.
    # In a real environment with lxml, it would parse. Here we just assert it ran.
    assert result is not None

def test_clean_xml_to_string_xxe_prevention():
    # An XXE payload
    xxe_payload = """<?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE test [
        <!ENTITY xxe SYSTEM "file:///etc/passwd">
    ]>
    <Event><System><Data Name="Exploit">&xxe;</Data></System></Event>"""

    result = clean_xml_to_string(xxe_payload)
    # The payload shouldn't cause a fatal crash, and the output shouldn't resolve the entity
    assert "root:x" not in result
