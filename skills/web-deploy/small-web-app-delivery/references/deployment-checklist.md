# Small Web App Deployment Checklist

## Before implementation

- [ ] Confirm the app directory and existing server are not being confused with the Hermes workspace itself.
- [ ] Inspect active listeners and the current reverse-proxy configuration.
- [ ] Check whether the requested hostname has an A/AAAA/CNAME record.
- [ ] Collect missing product facts (date, venue, timezone) instead of inventing them.

## Application smoke test

1. Start the app on a free loopback port.
2. `curl /health` and confirm a minimal 200 response.
3. `curl /` and check the title/form marker.
4. Submit one valid form with a clearly synthetic identity.
5. Query SQLite and verify the expected values.
6. Test an invalid submission and verify no row was created.
7. Delete the synthetic row and confirm it is gone.

## Hosting status language

- **Built locally:** app files and database schema exist; local smoke tests pass.
- **Running locally:** a process currently answers on the loopback port; this is not durable hosting.
- **Configured for hosting:** persistent service and reverse-proxy config are installed and validated; external DNS/HTTPS may still be pending.
- **Deployed:** persistent service, proxy, DNS, public HTTPS, and a public form submission have all been verified.

## Common handoff blockers

- Domain does not resolve: provide the exact DNS record target and stop short of claiming public availability.
- Service manager/system configuration requires authorization: do not retry with alternate destructive commands; report the blocked action.
- Existing port is occupied: identify the owning process and choose a free port or reuse the existing service only after confirming ownership and compatibility.
- Proxy is configured but backend is not persistent: fix the runtime before testing public traffic.
