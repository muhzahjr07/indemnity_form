# Statutory & Legal Document Specifications

## 1. Statutory Context

In Sri Lankan corporate law (Companies Act No. 07 of 2007), companies frequently execute formal Indemnity Agreements with corporate service providers and secretarial agents. These forms grant authorization to submit statutory electronic and physical filings to the Registrar General of Companies (Department of the Registrar of Companies - ROC / eROC system).

To maintain legal admissibility and audit compliance, the generated indemnity documents must conform to stringent data integrity and formatting requirements.

---

## 2. Document Field Specifications

### 2.1 Table 1: Company Identification
| Field | Source | Format / Case | Font & Size | Special Rules |
| :--- | :--- | :--- | :--- | :--- |
| **Name of Company** | Form 1 / Certificate of Incorporation | UPPERCASE | Calibri 10 pt | Exactly matches Certificate of Incorporation including punctuation. |
| **Company Registration No.** | Form 1 / Certificate of Incorporation | UPPERCASE | Calibri 10 pt | Prefixed with `PV` (e.g. `PV 00266559`, `PV 84646`, `PV 102555`). |
| **Registered Office** | Form 1 (Box 2) / Form 13 | UPPERCASE | Calibri 10 pt | Must include postal code (e.g. `POSTCODE: 01500`). |
| **Relevant Instruction** | Static Instruction Scope | UPPERCASE | Calibri 10 pt | Fixed value: **`ALL`**. |
| **Effective Date** | Incorporation Date | UPPERCASE | Calibri 10 pt | Date format: `<Day><ORD> <MON> <YEAR>` (e.g. `15TH NOV 2022`). Ordinal suffix must be **superscripted**. |

### 2.2 Table 2: Board of Directors
| Field | Source | Formatting | Styling |
| :--- | :--- | :--- | :--- |
| **Director Name** | Form 1 (Box 4) / Form 18 / Passport / NIC | UPPERCASE | Calibri 10 pt |
| **Identification** | NIC / Passport | Normal Case | e.g., `Passport No: Z4796174`, `Country: India` or `NIC No: 198114702824` |
| **Address Block** | Form 1 / Form 18 | Address title: Bold + Underline. Address: Capitalized Each Word. | Headers: `Local Address`, `Foreign Address`. Address text: 9 pt (`sz="18"`). |
| **Signature** | Signature Scan / Repository | Rendered image in `_signed.docx`; Blank in `_draft.docx` | Aspect ratio preserved; scaled ~1.15M EMUs. |
| **Date of Signing** | Incorp Date + 7 Days | Lowercase ordinal | e.g. `22nd Nov 2022`. Identical for all directors. |
| **Witness** | Blank / Execution reserved | Unfilled | Reserved for physical witness attestation. |

### 2.3 Table 3: Shareholders Schedule
- **Shareholder Name**: UPPERCASE Calibri 10 pt.
- **Identification & Address**: As recorded in Form 1 / Annual Return / Share Ledger.
- **Signatures (`_signed.docx`)**: Digital signature embedded for authorized shareholder representatives.
- **Signing Date**: Identical to company signing date (`incorp_date + 7 days`).
- **Draft Mode (`_draft.docx`)**: Signature and signed date remain blank for manual client review.

### 2.4 Table 4: Common Seal & Signatory
- **Authorised Signatory Name**: Designated Primary Director in UPPERCASE Calibri 10 pt.
- **Signature & Date**: Primary director signature image embedded along with the 7-day offset date.
- **Company Seal**: Unfilled placeholder for physical embossed / ink corporate seal.

---

## 3. Date Arithmetic & Ordinal Rules

The legal convention stipulates that the indemnity becomes effective on the date of corporate inception, while execution occurs within 7 calendar days post-incorporation:

$$\text{Effective Date} = \text{Date of Incorporation}$$
$$\text{Signed Date} = \text{Date of Incorporation} + 7\text{ days}$$

### Ordinal Generation Rule
- Ends in 1 (except 11): `ST` / `st`
- Ends in 2 (except 12): `ND` / `nd`
- Ends in 3 (except 13): `RD` / `rd`
- All other numbers (including 11, 12, 13): `TH` / `th`
