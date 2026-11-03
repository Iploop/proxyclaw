# ProxyClaw — IPLoop V2

Residential proxy requests for agents and scripts. Create/sign in at **https://platform.iploop.io/**. Save your account API key, separate proxy username and proxy password privately. Add bandwidth and use the connection settings shown in the dashboard. Do not assume a free credit amount or guaranteed target-site acceptance.

## V2 setup
```bash
export IPLOOP_API_KEY="YOUR_ACCOUNT_API_KEY"
export IPLOOP_PROXY_USERNAME="YOUR_PROXY_USERNAME"
export IPLOOP_PROXY_PASSWORD="YOUR_PROXY_PASSWORD"
```
The account key is not your proxy password. Setting both proxy credentials explicitly opts into V2; key-only existing integrations retain legacy authentication.

## Country, sessions and V2 city targeting
- Country routing uses valid ISO alpha-2 codes; availability depends on the live pool.
- Sticky sessions group requests; device availability can change the exit. A new session does not guarantee a never-used IP.
- **State/city targeting is a V2 capability pending server deployment. It is not live yet.** It remains in the interfaces, but calls fail clearly until the deployment gate is enabled after the owner confirms rollout. Do not restart gateways or disconnect device SDKs merely to enable client options.
- V2 ASN targeting is not currently supported.

## Python SDK
```bash
python -m pip install 'iploop-sdk[async,socks]>=1.8.2'
```
```python
import os
from iploop import IPLoop
client = IPLoop(
    os.environ['IPLOOP_API_KEY'],
    proxy_username=os.environ['IPLOOP_PROXY_USERNAME'],
    proxy_password=os.environ['IPLOOP_PROXY_PASSWORD'],
)
r = client.get('https://example.com', country='US', timeout=15)
r.raise_for_status()
```
The released Python SDK keeps city selectors unavailable until backend rollout. HTTP/SOCKS5, sticky and account usage instructions: https://proxyclaw.ai/docs.html

## Boundaries
A successful proxy connection does not prove anti-bot bypass, CAPTCHA solving, JavaScript rendering or accurate structured extraction. These are separate integrations requiring their own tests. Historical inventory/benchmark numbers are not capacity or availability guarantees. Existing earnings/node programs and legacy API guides are separate from the V2 proxy contract; verify eligibility and rates with support.

Support: support@iploop.io. Keep credentials private.

## Agent CLI (this repository)
Requires **Python 3, bash and curl**. Clone the current GitHub source; an older ClawHub package is not automatically updated by a repository change.
```bash
git clone https://github.com/Iploop/proxyclaw.git
cd proxyclaw
./setup.sh
./fetch.sh https://example.com --country US
./fetch.sh https://example.com --country US --session demo123
./fetch.sh https://example.com --country GB --protocol socks5h
./fetch.sh https://example.com --format markdown
```
`--format markdown` is a basic text conversion, not JavaScript rendering or structured extraction. Credentials are delivered to curl through stdin, not command-line arguments. Failed connections or non-success HTTP status exit nonzero. Setup does not announce success on failure.

### V2 state/city interface (not yet deployed)
`--country US --state tx --city austin` is retained for the future V2 rollout. It currently fails locally rather than silently dropping geography. `IPLOOP_V2_CITY_ENABLED=1` is a deployment gate for a separately verified server rollout, not a way to make today's server support it. Leave it unset today.

### Legacy integrations
Leave both V2 proxy credential variables unset to retain existing key-only authentication. This does not migrate legacy credentials or certify all legacy selectors. No customer key revocation is required.
