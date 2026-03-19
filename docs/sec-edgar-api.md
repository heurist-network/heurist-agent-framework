# SEC EDGAR Runtime Notes

Primary sources used for this integration:

- `https://www.sec.gov/edgar/sec-api-documentation`
- `https://www.sec.gov/os/accessing-edgar-data`
- `https://www.sec.gov/files/company_tickers.json`
- `https://data.sec.gov/submissions/CIK##########.json`
- `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
- `https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets`

Runtime observations validated during implementation:

- `company_tickers.json` is the simplest issuer-resolution surface for ticker/name to CIK.
- `submissions/CIK##########.json` exposes recent filing arrays plus paged historical submission files in `filings.files`.
- `companyfacts/CIK##########.json` is large and concept names drift across issuers, so the agent resolves metrics by label/name matching instead of hardcoding one concept per request.
- Recent insider ownership filings appear in issuer submissions as Forms `3`, `4`, and `5`, and the `primaryDocument` field often points to rendered ownership HTML under `xslF345X0*`.
- Schedule `13D` and `13G` filings are available in issuer submissions and can be summarized from the primary filing HTML.
- The Form 13F flattened ZIP currently contains `SUBMISSION.tsv`, `COVERPAGE.tsv`, `SUMMARYPAGE.tsv`, `INFOTABLE.tsv`, and related tables.
- In the current 13F metadata, `INFOTABLE.VALUE` is described as market value rounded to the nearest dollar starting January 3, 2023.

Chosen first-class tool surface:

- `resolve_company`
- `filing_timeline`
- `filing_diff`
- `xbrl_fact_trends`
- `insider_activity`
- `activist_watch`
- `institutional_holders`

Implementation notes:

- The agent sets a declared SEC `User-Agent` and spaces requests to stay within fair-access expectations.
- `institutional_holders` is issuer-first. It matches the issuer against the latest 13F dataset using SEC company-name normalization, then aggregates matching rows by filing manager.
- `filing_diff` is intentionally honest: it is a paragraph-level comparison of filing body text, not a semantic redline supplied by the SEC.
