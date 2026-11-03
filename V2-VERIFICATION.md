# V2 verification

- 14 CLI contract tests passed.
- Dedicated QA account: setup, HTTP and SOCKS5 requests passed; invalid country and un-deployed city calls rejected.
- Key-only legacy auth generation regression-tested, not a new live OG fleet certification.
- City/state stays a V2 rollout-gated capability, not deployed by this change.
- Current GitHub source is the supported installation path; ClawHub/catalog packages are separate release targets.
- No gateway restart, customer balance edit or credential revocation.
