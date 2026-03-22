
## 2024-03-22 - Prevent XXE Vulnerability in XML Parsing
**Vulnerability:** The `clean_xml_to_string` function in `src/utils/__init__.py` parsed untrusted XML data using `lxml.etree.fromstring()` with default settings, which left it vulnerable to XML External Entity (XXE) injection attacks.
**Learning:** `lxml`'s default parser configuration resolves external entities. When processing user-provided or external data (like event logs) without explicitly disabling external entities, it allows an attacker to read arbitrary files from the server or cause a Denial of Service (DoS).
**Prevention:** Always explicitly disable external entity resolution using `etree.XMLParser(resolve_entities=False)` when parsing XML. Additionally, encode XML strings to `utf-8` bytes before parsing to avoid `ValueError` crashes caused by XML declarations with encoding attributes.
