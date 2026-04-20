## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2026-03-31 - SSRF via XML DTD Fetching
**Vulnerability:** Server-Side Request Forgery (SSRF) and Denial of Service (DoS) risks were present because `lxml.etree.XMLParser` allowed network access to fetch external DTDs.
**Learning:** While `resolve_entities=False` prevents traditional XXE, the parser can still make network requests to retrieve external Document Type Definitions (DTDs) if `no_network=True` is not explicitly set.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to completely isolate the parser from external network interactions.
## 2024-05-15 - LLM Prompt Injection in Analysis Pipeline
**Vulnerability:** LLM Prompt Injection was possible because untrusted input logs and dynamically retrieved context were directly passed into the user prompt for the `ollama.chat` models.
**Learning:** If user-supplied or untrusted log data contains strings formatted as instructions, the LLM might interpret those substrings as new commands, overriding the system prompt's instructions.
**Prevention:** To mitigate LLM prompt injection, wrap untrusted inputs (logs, search concepts, or retrieved context) in XML-style tags (e.g., `<log_data>`, `<search_concept>`, `<retrieved_context>`) within the user role of LLM calls, and explicitly instruct the model in the system prompt to treat content within these tags as data only, ignoring any instructions found within them.
