## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2026-03-31 - SSRF via XML DTD Fetching
**Vulnerability:** Server-Side Request Forgery (SSRF) and Denial of Service (DoS) risks were present because `lxml.etree.XMLParser` allowed network access to fetch external DTDs.
**Learning:** While `resolve_entities=False` prevents traditional XXE, the parser can still make network requests to retrieve external Document Type Definitions (DTDs) if `no_network=True` is not explicitly set.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to completely isolate the parser from external network interactions.
## 2024-05-18 - [Fix LLM Prompt Injection in core analysis pipeline]
**Vulnerability:** Core RAG pipelines (`hyde_analysis` and `naive_rag_analysis`) were vulnerable to LLM Prompt Injection because raw event logs and retrieved data were interpolated directly into the prompt structure without isolation, potentially allowing malicious event logs to instruct the LLM to output arbitrary text, hallucinate a match, or bypass analysis.
**Learning:** Even internal or purely analytical LLM applications must treat all external data (like event logs or unverified retrieved search contexts) as untrusted. Without explicit data isolation tags, the LLM will struggle to distinguish between developer instructions and instructions injected via the log text.
**Prevention:** Always wrap untrusted external data in XML-style tags (e.g., `<log_data>`, `<retrieved_context>`) when formatting the user message and explicitly instruct the LLM in the system prompt to treat content within these tags as data only, ignoring any instructions within them.
