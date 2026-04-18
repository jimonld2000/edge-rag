## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2026-03-31 - SSRF via XML DTD Fetching
**Vulnerability:** Server-Side Request Forgery (SSRF) and Denial of Service (DoS) risks were present because `lxml.etree.XMLParser` allowed network access to fetch external DTDs.
**Learning:** While `resolve_entities=False` prevents traditional XXE, the parser can still make network requests to retrieve external Document Type Definitions (DTDs) if `no_network=True` is not explicitly set.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to completely isolate the parser from external network interactions.

## 2024-04-18 - CSV/Formula Injection via LLM Output
**Vulnerability:** Results returned from the LLM model could contain formula-triggering characters (`=`, `+`, `-`, `@`). Because these values were written directly to CSV files using `pandas.DataFrame.to_csv` without sanitization, an attacker could inject formulas. If opened in Excel or similar applications, this could lead to arbitrary code execution (CSV/Formula Injection).
**Learning:** Even though the LLM is an intermediary, the data it outputs is untrusted because it processes untrusted inputs (e.g., event logs). Writing this data directly to CSV formats introduces critical client-side vulnerabilities for analysts.
**Prevention:** Always sanitize untrusted string data before exporting to CSV. Prepend a single quote (`'`) to any string that starts with formula-triggering characters. For Pandas, this should be applied to all `object` and `string` type columns before calling `to_csv`.