# Deployed V2 geography verification

New SDK/CLI/MCP accept validated state/city by default. Require country, allow city without state. Legacy mode preserved; no gateway changes. Tests and real dedicated QA canaries are recorded in the task release report. State/city selectors are deployed in V2. Country is required; state is optional for a city request. Exact-city accuracy is not certified: some Austin test exits were labeled San Antonio or Schertz by independent geo services. Inspect the observed location when precision matters.
