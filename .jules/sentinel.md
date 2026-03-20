
## 2024-05-28 - XXE Vulnerability in EVTX Parsing
**Vulnerability:** XML External Entity (XXE) vulnerability via `etree.fromstring`.
**Learning:** `lxml`'s `etree` parser resolves external entities by default, leading to XXE. EVTX logs parsed to XML can be a vector.
**Prevention:** Use `etree.XMLParser(resolve_entities=False)` explicitly when parsing untrusted XML data.
