## 2024-05-01 - Fix XXE Vulnerability in XML Parsing
**Vulnerability:** XML External Entity (XXE) vulnerability in `src/utils/__init__.py` where `lxml.etree.fromstring` parsed EVTX log XML without disabling external entity resolution.
**Learning:** Parsing raw Windows Event Logs (EVTX) converted to XML inherently exposes the system to XXE if untrusted log data contains malicious entity declarations. `lxml` allows entity resolution by default.
**Prevention:** Always explicitly disable external entity resolution using `etree.XMLParser(resolve_entities=False)` when parsing XML, and ensure inputs are properly encoded to utf-8 bytes before calling `fromstring` to avoid encoding mismatch errors.
