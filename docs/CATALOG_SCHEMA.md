# Company Catalog Schema & Data Dictionary

## 1. Schema Definition

The company catalog consists of an array of company definition dictionaries named `ALL_COMPANIES`. Each entry represents a corporate entity and its statutory officers.

```json
{
  "name": "string (UPPERCASE)",
  "reg_no": "string (PV xxxxxx)",
  "office": "string (UPPERCASE with POSTCODE)",
  "instruction": "string (Fixed: ALL)",
  "folder_name": "string",
  "file_prefix": "string",
  "incorp_day": "string (1-31)",
  "incorp_ord": "string (ST, ND, RD, TH)",
  "incorp_month_year": "string (e.g. NOV 2022)",
  "signing_day": "string (1-31, +7 days)",
  "signing_ord": "string (st, nd, rd, th)",
  "signing_month_year": "string (e.g. Nov 2022)",
  "signatory_name": "string (UPPERCASE)",
  "signatory_sig": "string (path to image or null)",
  "directors": [
    {
      "name": "string (UPPERCASE)",
      "id_lines": ["string"],
      "address_paragraphs": ["string"],
      "sig_file": "string (path to image or null)"
    }
  ],
  "shareholders": [
    {
      "name": "string (UPPERCASE)",
      "id_lines": ["string"],
      "address_paragraphs": ["string"],
      "sig_file": "string (path to image or null)"
    }
  ]
}
```

---

## 2. Field Specifications

### Company Level
- `name` *(str)*: Registered corporate name in full uppercase, matching the Certificate of Incorporation.
- `reg_no` *(str)*: Registrar of Companies registration number, formatted as `PV <number>`.
- `office` *(str)*: Official registered office address in uppercase, ending with `POSTCODE: <5-digit code>`.
- `instruction` *(str)*: The instruction scope, set to `ALL` per statutory indemnity instructions.
- `folder_name` *(str)*: Name of the output directory created inside `final/`.
- `file_prefix` *(str)*: Prefix for the output documents (`<file_prefix>_draft.docx` and `<file_prefix>_signed.docx`).
- `incorp_day`, `incorp_ord`, `incorp_month_year` *(str)*: Incorporation date components.
- `signing_day`, `signing_ord`, `signing_month_year` *(str)*: Exactly 7 days after the incorporation date.
- `signatory_name` *(str)*: Primary director authorized to execute corporate resolutions and seal the indemnity.
- `signatory_sig` *(str | None)*: Relative path to the signature image for the authorised signatory.

### Director & Shareholder Level
- `name` *(str)*: Full legal name in uppercase.
- `id_lines` *(list[str])*: Array of identification strings (e.g. `['NIC No: 198114702824']` or `['Passport No: Z4796174', 'Country: India']`).
- `address_paragraphs` *(list[str])*:
  - If domestic only: `['No. 12, Main Street, Colombo 03, Postcode: 00300']`
  - If foreign: Must include section headers:
    ```python
    [
        'Local Address',
        '568/2, Aluthmawath Road, Colombo 15, Postcode: 01500',
        'Foreign Address',
        '194, 8th Main, 9th Cross, H M T Layout, RT Nagar, Bengaluru, Karnataka, Zipcode: 560032, India'
    ]
    ```
- `sig_file` *(str | None)*: Relative path to the client's signature image file.
