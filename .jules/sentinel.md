## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2026-03-31 - SSRF via XML DTD Fetching
**Vulnerability:** Server-Side Request Forgery (SSRF) and Denial of Service (DoS) risks were present because `lxml.etree.XMLParser` allowed network access to fetch external DTDs.
**Learning:** While `resolve_entities=False` prevents traditional XXE, the parser can still make network requests to retrieve external Document Type Definitions (DTDs) if `no_network=True` is not explicitly set.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to completely isolate the parser from external network interactions.
## 2024-05-18 - CSV Injection in Report Generation
**Vulnerability:** A CSV Injection (Formula Injection) vulnerability was possible because unvalidated user input or LLM predictions were directly passed into pandas `to_csv` methods. Attackers could manipulate log content to output characters like `=`, `+`, `-`, or `@`, causing arbitrary execution when the resulting CSV was opened in Excel.
**Learning:** Even internal reporting tools are vulnerable if they blindly trust complex systems like LLMs to only output safe content. We must defensively assume anything coming from an LLM that originated from untrusted log input could contain formula injection attempts.
**Prevention:** Always sanitize pandas DataFrames prior to exporting to CSV by prepending single quotes to `object` and `string` column types that begin with `=`, `+`, `-`, or `@`.
