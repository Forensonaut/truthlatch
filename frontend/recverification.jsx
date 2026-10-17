import React from "react";
import StatusBadge from "./statusbadge.jsx";

function formatTimestamp(value) {
  if (!value) return "Timestamp unavailable";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function RecVerification({ verification }) {
  if (!verification) {
    return (
      <section className="rec-card" aria-label="Latest verification">
        <p className="rec-card__eyebrow">LATEST VERIFICATION</p>
        <h2 className="rec-card__title">No verification run yet</h2>
        <p className="rec-card__meta">
          Run a verification to see its result, explanation and evidence here.
        </p>
        <hr className="rec-card__divider" />
        <p className="rec-card__claim">
          TruthLatch returns VERIFIED, CONTRADICTED or UNKNOWN based on fresh,
          authoritative evidence.
        </p>
      </section>
    );
  }

  const status = verification.status || "UNKNOWN";
  const evidence = Array.isArray(verification.evidence) ? verification.evidence : [];
  const expected = verification.expected_observation
    || evidence[0]?.observation
    || "No sufficient evidence matched the expected state.";
  const sourceSummary = evidence.length
    ? [...new Set(evidence.map((item) => item.source))].join(", ")
    : "No relevant evidence was accepted";
  const badgeStatus = status === "VERIFIED"
    ? "match"
    : status.toLowerCase();

  return (
    <section className="rec-card" aria-label="Latest verification">
      <p className="rec-card__eyebrow">LATEST VERIFICATION</p>

      <header className="rec-card__header">
        <div>
          <h2 className="rec-card__title">{expected}</h2>
          <p className="rec-card__meta">
            {verification.verification_id} · API / VERIFY
          </p>
        </div>
        <StatusBadge status={badgeStatus} withIcon>{status}</StatusBadge>
      </header>

      <hr className="rec-card__divider" />

      <div className="rec-card__block">
        <p className="rec-card__eyebrow">VERIFICATION EXPLANATION</p>
        <p className="rec-card__claim">{verification.explanation}</p>
      </div>

      <div className="rec-card__block">
        <p className="rec-card__eyebrow">EVIDENCE REVIEWED</p>
        <div className="rec-check">
          <span className="rec-check__icon" aria-hidden="true">
            {evidence.length > 0 ? "✓" : "—"}
          </span>
          <div className="rec-check__text">
            <strong>{sourceSummary}</strong>
            <span>{evidence.length} relevant evidence item{evidence.length === 1 ? "" : "s"} returned by the verifier</span>
          </div>
          <StatusBadge status={badgeStatus}>
            {evidence.length ? "REVIEWED" : "NONE"}
          </StatusBadge>
        </div>
      </div>

      <hr className="rec-card__divider" />

      <footer className="rec-card__footer">
        <div>
          <p className="rec-card__eyebrow">CHECKED AT</p>
          <p className="rec-card__time">{formatTimestamp(verification.checked_at)}</p>
        </div>
        <div>
          <p className="rec-card__eyebrow">EVIDENCE COVERAGE</p>
          <p className="rec-card__coverage">
            {evidence.length} relevant item{evidence.length === 1 ? "" : "s"}
          </p>
        </div>
      </footer>
    </section>
  );
}

export default RecVerification;
