## 2024-05-14 - XXE Vulnerability in EVTX Log Parsing
**Vulnerability:** External XML Entity (XXE) injection was possible because `lxml.etree.fromstring` was used to parse EVTX logs without explicitly disabling external entity resolution.
**Learning:** The default `etree.fromstring` behavior in lxml resolves external entities. Also, `lxml.etree.fromstring` can throw exceptions with strings containing an XML declaration, requiring conversion to utf-8 bytes first.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False)` when parsing untrusted XML, and ensure the input is encoded to utf-8 bytes (`xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string`) before passing to `etree.fromstring`.

## 2026-03-31 - SSRF via XML DTD Fetching
**Vulnerability:** Server-Side Request Forgery (SSRF) and Denial of Service (DoS) risks were present because `lxml.etree.XMLParser` allowed network access to fetch external DTDs.
**Learning:** While `resolve_entities=False` prevents traditional XXE, the parser can still make network requests to retrieve external Document Type Definitions (DTDs) if `no_network=True` is not explicitly set.
**Prevention:** Always initialize `etree.XMLParser(resolve_entities=False, no_network=True)` when parsing untrusted XML to completely isolate the parser from external network interactions.

## 2026-04-12 - CSV/Formula Injection via Pandas Export
**Vulnerability:** CSV/Formula Injection was possible because untrusted strings (such as extracted IDs from LLM predictions or filenames) were directly exported to CSV using `pandas.DataFrame.to_csv` without sanitization. If a user provided an EVTX file with a crafted filename or an LLM responded with a malicious ID starting with `=`, `+`, `-`, or `@`, spreadsheet applications opening the CSV could execute unintended commands.
**Learning:** Standard CSV export libraries like pandas do not sanitize data for formula injection by default. Untrusted text strings can act as executable formulas if not correctly escaped.
**Prevention:** Always sanitize untrusted string data (e.g., in pandas `object` or `string` columns) before calling `to_csv` by prepending a single quote (`'`) to any string that starts with a formula-triggering character (`=`, `+`, `-`, `@`).