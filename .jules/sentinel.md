## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2026-03-31 - SSRF via XML DTD Fetching
**Vulnerability:** Server-Side Request Forgery (SSRF) and Denial of Service (DoS) risks were present because `lxml.etree.XMLParser` allowed network access to fetch external DTDs.
**Learning:** While `resolve_entities=False` prevents traditional XXE, the parser can still make network requests to retrieve external Document Type Definitions (DTDs) if `no_network=True` is not explicitly set.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to completely isolate the parser from external network interactions.

## 2026-04-28 - [Mitigate LLM Prompt Injection in RAG Pipeline]
**Vulnerability:** Untrusted log data, search queries, and retrieved contexts were directly interpolated into LLM prompts without clear boundaries, allowing potential prompt injection attacks where malicious log content could override the system instructions.
**Learning:** In a Retrieval-Augmented Generation (RAG) architecture, all untrusted external inputs must be properly isolated from the instructions to prevent them from altering the model's behavior.
**Prevention:** Wrap untrusted inputs (logs, concepts, contexts) in XML-style tags (e.g., <log_data>) and explicitly instruct the LLM system prompt to treat content within these tags strictly as data.
