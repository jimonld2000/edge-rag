## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2026-03-31 - SSRF via XML DTD Fetching
**Vulnerability:** Server-Side Request Forgery (SSRF) and Denial of Service (DoS) risks were present because `lxml.etree.XMLParser` allowed network access to fetch external DTDs.
**Learning:** While `resolve_entities=False` prevents traditional XXE, the parser can still make network requests to retrieve external Document Type Definitions (DTDs) if `no_network=True` is not explicitly set.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to completely isolate the parser from external network interactions.
## 2024-05-15 - Prompt Injection in RAG Pipeline
**Vulnerability:** User-provided event log data was concatenated directly into LLM prompts without isolation, allowing attackers to inject malicious instructions that the model would follow (Prompt Injection).
**Learning:** In a RAG pipeline, untrusted input (logs, retrieved context) must be clearly separated from instructions. The model cannot distinguish between system commands and user data when they are simply concatenated.
**Prevention:** Wrap untrusted variables in XML-style tags (e.g., `<log_data>`, `<retrieved_context>`) within the user prompt, and explicitly instruct the model in the system prompt to treat content within these tags as data only, ignoring any instructions they may contain.
