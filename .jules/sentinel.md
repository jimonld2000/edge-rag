## 2024-05-24 - [CRITICAL] Fix XXE vulnerability in XML parsing
**Vulnerability:** The application parsed raw XML strings from EVTX logs using `lxml.etree.fromstring()` without disabling external entity resolution, creating a risk for XML External Entity (XXE) vulnerabilities if logs contain untrusted input.
**Learning:** `lxml` allows external entity resolution by default in some contexts. Explicitly configuring the `XMLParser` to disable it is a necessary defense-in-depth measure.
**Prevention:** Always use an explicitly configured `XMLParser` with `resolve_entities=False` when using `lxml.etree.fromstring` or `lxml.etree.parse` on data originating from potentially untrusted sources like EVTX logs.
