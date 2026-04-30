## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2026-03-31 - SSRF via XML DTD Fetching
**Vulnerability:** Server-Side Request Forgery (SSRF) and Denial of Service (DoS) risks were present because `lxml.etree.XMLParser` allowed network access to fetch external DTDs.
**Learning:** While `resolve_entities=False` prevents traditional XXE, the parser can still make network requests to retrieve external Document Type Definitions (DTDs) if `no_network=True` is not explicitly set.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to completely isolate the parser from external network interactions.
## 2026-04-30 - Prompt Injection in LLM RAG Pipeline
**Vulnerability:** The application was vulnerable to Prompt Injection. Raw event log text and dynamically generated search concepts were passed directly into LLM prompts without clear boundaries.
**Learning:** LLMs cannot reliably distinguish between system instructions and untrusted user data if they are concatenated directly. Even with explicit instructions, the model may still be susceptible to well-crafted injections.
**Prevention:** Always wrap untrusted inputs (logs, retrieved context, search concepts) in explicit XML-style tags (e.g., <log_data>, <retrieved_context>) and instruct the LLM in the system prompt to treat content within these specific tags strictly as data.
