## 2026-03-17 - Fix XXE vulnerability in XML parsing
**Vulnerability:** The application was vulnerable to XML External Entity (XXE) injection attacks when parsing raw EVTX logs in `src/utils/__init__.py` using the `lxml.etree` module. The default parser didn't restrict external entity resolution.
**Learning:** Raw event log parsing that uses `lxml.etree` can easily introduce XXE vulnerabilities if the source is untrusted and external entities are permitted by default.
**Prevention:** Always configure XML parsers to disable external entity resolution explicitly, particularly when processing input that might contain user-controlled or external data. For `lxml`, use `etree.XMLParser(resolve_entities=False)` when parsing strings or files.
