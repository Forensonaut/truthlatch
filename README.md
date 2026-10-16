# CoreShift — TruthLatch

**Tagline:** Don't trust an AI's claim until the evidence agrees.

## Problem

AI agents can report that an action succeeded even when the underlying system state does not confirm the result. Relying on claims alone can lead to incomplete actions and unreliable audit records.

## Proposed solution

TruthLatch independently verifies AI execution claims against observed evidence and returns one of three outcomes:

- **VERIFIED** — sufficient evidence confirms the expected result.
- **CONTRADICTED** — evidence shows the claimed result was not achieved.
- **UNKNOWN** — evidence is missing, unavailable, stale, or inconclusive.

## Datathon

IBM Z Datathon 2026  
Team: CoreShift  
Theme: AI Secured — Innovation Without Exposure

## Development status

Project setup and planning.

Implementation will begin during the official datathon window.

## Planned technologies

- Python
- IBM LinuxONE Community Cloud
- AI/ML components
- Automated tests and evidence-linked audit records
