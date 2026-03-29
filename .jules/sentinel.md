## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2024-05-15 - SSRF / Incomplete XXE Mitigation in lxml
**Vulnerability:** While `resolve_entities=False` prevents basic XXE, an attacker could still potentially trigger Server-Side Request Forgery (SSRF) if `lxml` attempts to fetch remote DTDs or other network resources during parsing.
**Learning:** `lxml`'s `etree.XMLParser` may perform network requests during XML parsing even if entity resolution is disabled.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` to explicitly block network access during XML parsing in `lxml`, ensuring robust prevention of both XXE and SSRF.
