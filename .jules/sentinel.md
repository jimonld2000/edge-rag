## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2026-03-31 - SSRF via XML DTD Fetching
**Vulnerability:** Server-Side Request Forgery (SSRF) and Denial of Service (DoS) risks were present because `lxml.etree.XMLParser` allowed network access to fetch external DTDs.
**Learning:** While `resolve_entities=False` prevents traditional XXE, the parser can still make network requests to retrieve external Document Type Definitions (DTDs) if `no_network=True` is not explicitly set.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to completely isolate the parser from external network interactions.
## 2024-05-18 - CSV/Formula Injection in Data Export
**Vulnerability:** CSV Injection (Formula Injection) was possible because untrusted LLM outputs ("Pred" column) were written directly to a CSV file without sanitization. If opened in spreadsheet applications, crafted inputs starting with `=, +, -, @` could execute arbitrary formulas.
**Learning:** Pandas `to_csv` does not automatically neutralize formula-triggering characters. Even "AI-generated" content must be treated as untrusted input, especially when it acts on attacker-controlled log files.
**Prevention:** Always sanitize string/object type columns in pandas DataFrames prior to exporting to CSV by prepending a single quote (`'`) to values that start with `=, +, -, @` (e.g., `df['col'].astype(str).str.startswith(...)`).
