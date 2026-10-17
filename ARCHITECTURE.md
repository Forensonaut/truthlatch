# TruthLatch — System Architecture

**Team:** CoreShift  
**Platform:** IBM LinuxONE Community Cloud  
**Architecture status:** Initial design; implementation to be validated

## 1. Purpose

TruthLatch independently evaluates whether an AI agent's claim
about an action is supported by observable evidence.

The prototype uses an identity-and-access management (IAM)
scenario: an agent claims that a user's access has been revoked.

TruthLatch evaluates evidence about the resulting state rather
than trusting the agent's success message alone.

## 2. Core verification outcomes

- VERIFIED: sufficient, relevant, fresh and authoritative evidence
  confirms the expected outcome.
- CONTRADICTED: sufficient, relevant evidence demonstrates that
  the expected outcome was not achieved.
- UNKNOWN: evidence is missing, stale, conflicting, unavailable,
  or otherwise insufficient for a reliable decision.

Missing evidence alone must not be treated as proof of failure.
A decision must include an explanation and evidence references.

## 3. Logical architecture

1. Claim input: receives the claimed action and expected outcome.
2. API and orchestration: validates requests and coordinates processing.
3. Verification engine: evaluates evidence against the expected state.
4. Evidence records: represent observations, their sources and freshness.
5. Audit layer: records the decision and its supporting evidence.
6. User interface: presents the result, explanation and evidence.

These are logical boundaries. The implementation and integration
of each component remain subject to team review and testing.

## 4. Shared verification flow

1. Receive a claim and its expected outcome.
2. Validate the request and evidence structure.
3. Evaluate evidence relevance, freshness, authority and consistency.
4. Produce VERIFIED, CONTRADICTED or UNKNOWN.
5. Return a human-readable explanation and evidence references.
6. Record the decision for traceability.

## 5. Design principles

- Evidence, not an agent's assertion, determines the result.
- Uncertainty must be represented explicitly.
- Evidence provenance and freshness must be inspectable.
- Decisions should be reproducible for the same inputs.
- Invalid inputs must be rejected clearly.
- Synthetic demo evidence must be labelled as synthetic.
- No production IAM changes are required for the prototype.

## 6. Team integration boundaries

- Verification engine: evidence evaluation and decision logic.
- API and audit: request handling, orchestration and audit persistence.
- Dashboard: claim submission and result presentation.
- Evidence explorer: evidence inspection and audit history.
- System architecture and integration: shared contracts, compatibility,
  deployment coordination and end-to-end validation.

Exact function names, API paths and payload fields must be agreed
through the shared contract before components are integrated.

## 7. IBM LinuxONE deployment

The target environment is Ubuntu 24.04 on IBM LinuxONE s390x.
Dependencies must support the target architecture. Compatibility,
runtime behaviour and performance must be tested on the actual VM.

No hardware acceleration or specialised security capability is
assumed unless it is configured and demonstrated.

## 8. Validation plan

The prototype should test at least:
- Fresh authoritative evidence confirming the expected state.
- Sufficient evidence contradicting the expected state.
- Missing evidence.
- Stale evidence.
- Conflicting observations.
- Invalid requests and malformed evidence.

Tests must verify both the outcome and its explanation.

## 9. Status and limitations

This document defines the initial design, not completed functionality.
Implementation status, test results and platform capabilities must
be reported accurately as work progresses.
