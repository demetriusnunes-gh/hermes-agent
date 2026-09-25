# Small Application Deployment Checklist

## Before implementation

- [ ] Confirm the app directory and existing server are not being confused with the Hermes workspace.
- [ ] Inspect active listeners and current reverse-proxy configuration.
- [ ] Check whether the requested hostname has an A/AAAA/CNAME record.
- [ ] Collect missing product facts instead of inventing them.

## Application smoke test

1. Start the app on a free loopback port.
2. Check `/health` and confirm a minimal 200 response.
3. Check `/` and verify the title/form marker.
4. Submit one valid form with a clearly synthetic identity.
5. Query SQLite and verify expected values.
6. Test invalid input and verify no row was created.
7. Delete the synthetic row and confirm it is gone.

## Status language

- **Built locally:** app files and database schema exist; local smoke tests pass.
- **Running locally:** a process answers on loopback; this is not durable hosting.
- **Configured for hosting:** persistent service and proxy are installed and validated; external DNS/HTTPS may still be pending.
- **Deployed:** persistent service, proxy, DNS, public HTTPS, and a public form submission have all been verified.

## Handoff blockers

- Domain does not resolve: provide the exact DNS record target and stop short of claiming public availability.
- Service-manager/system configuration requires authorization: report the blocked action.
- Existing port is occupied: identify the owner and choose a free port or reuse only after confirming compatibility.
- Proxy is configured but backend is not persistent: fix the runtime before testing public traffic.
