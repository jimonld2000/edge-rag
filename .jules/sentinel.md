## 2024-05-18 - Fix XXE in Event Log XML Parsing
**Vulnerability:** XML External Entity (XXE) vulnerability in `src/utils/__init__.py`'s `clean_xml_to_string` function, where `lxml.etree.fromstring` was used without disabling entity resolution to process Windows EVTX logs.
**Learning:** `lxml` allows external entity resolution by default, which can lead to local file disclosure or SSRF if an attacker manages to inject a crafted XML payload into the EVTX logs. Even in a research-focused or internal logging system, untrusted input (e.g., event logs from compromised machines) parsed with default XML parsers can be weaponized.
**Prevention:** Always explicitly pass an `etree.XMLParser(resolve_entities=False)` when parsing XML strings from external or untrusted sources with `lxml`.
