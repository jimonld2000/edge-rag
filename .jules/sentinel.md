## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2024-05-14 - SSRF/XXE via Network Access in XML Parser
**Vulnerability:** Even with `resolve_entities=False`, `lxml.etree.XMLParser` could potentially make network requests to retrieve external DTDs or other resources depending on the XML payload (e.g., `<!DOCTYPE ... SYSTEM "http://...">`).
**Learning:** `resolve_entities=False` stops entity replacement but does not entirely stop the parser from initiating network connections.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to robustly block all external network access.
