# Security & Data Governance Policy

## 1. Confidentiality Statement

The Corporate Indemnity Form Generator processes sensitive corporate filings and Personal Identifying Information (PII), including:
- National Identity Card (NIC) numbers and passport copies.
- Residential street addresses and personal contact details of foreign and domestic directors.
- Corporate shareholding structures and commercial entity identifiers.
- Certified physical and electronic signatures of directors and authorized representatives.

Under corporate data protection standards and client confidentiality mandates, **none of these production assets are tracked in version control or published to public repositories**.

---

## 2. Zero External Sourcing Mandate

To guarantee legal fidelity and protect clients against hallucinated or conflated identity records:

1. **No External Web Scraping**: The engine strictly forbids querying external public registries, search engines, or third-party databases (e.g. Indian Ministry of Corporate Affairs, international business directories).
2. **Ground Truth Sourcing**: Every entry in the production catalog must originate directly and solely from certified statutory files:
   - Registrar of Companies (ROC) Form 1 (Incorporation Application)
   - Form 15 (Notice of Annual Return / Director Particulars)
   - Form 18 (Consent and Certificate of Director)
   - Official Certificates of Incorporation issued by the Department of the Registrar of Companies Sri Lanka.
3. **No Inferred PII**: If a statutory field is obscured or degraded in a low-resolution scan, it must be visually confirmed from high-resolution master filings rather than guessed or completed from internet search results.

---

## 3. Version Control Exclusion Architecture

The repository's `.gitignore` isolates all proprietary client information from git tracking:

| Path / Pattern | Classification | Rationale |
| :--- | :--- | :--- |
| `data/` | RESTRICTED | Contains raw image scans of certified Form 1/15/18 filings, NICs, and passports. |
| `signatures of clients/` | RESTRICTED | Contains high-resolution isolated client signature PNG/JPEG assets. |
| `final/` | CONFIDENTIAL | Contains generated production `.docx` forms featuring real identities and signatures. |
| `companies_catalog.py` | CONFIDENTIAL | Master dataset containing unredacted client PII for all operational entities. |
| `all_data_folders_ocr.json` | CONFIDENTIAL | Full-text OCR dumps of confidential corporate filings and personal identity documents. |
| `scratch/` | INTERNAL | Development crops, debug scripts, and temporary visual verification files. |
| `*.docx` | SENSITIVE | Base templates and generated binary documents. |

---

## 4. Anonymized Public Testing

For external audit, code review, and continuous integration:
- A sanitized sample catalog ([`companies_catalog_sample.py`](../companies_catalog_sample.py)) is provided.
- The sample uses fictional company identities (e.g. `ACME PACIFIC HOLDINGS`) with mock passport numbers and public addresses.
- The generation engine automatically detects whether the production `companies_catalog.py` is present, falling back gracefully to the anonymized sample for open-source execution.
