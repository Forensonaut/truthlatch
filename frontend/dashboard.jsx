import React, { useMemo, useState } from "react";
import StatCard from "./statcard.jsx";
import SuccessRateChart from "./successratechart.jsx";
import RecVerification from "./recverification.jsx";
import { verifyClaim } from "./api.js";

function makeEvidenceId(index) {
  return globalThis.crypto?.randomUUID?.() || `evidence-${Date.now()}-${index}`;
}

function Dashboard({ records = [], onVerified = () => {}, historyError = "" }) {
  const [formOpen, setFormOpen] = useState(false);
  const [expectedObservation, setExpectedObservation] = useState("");
  const [evidenceText, setEvidenceText] = useState("");
  const [source, setSource] = useState("manual-input");
  const [authoritative, setAuthoritative] = useState(false);
  const [contradictionsText, setContradictionsText] = useState("");
  const [maxAgeSeconds, setMaxAgeSeconds] = useState("3600");
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");

  const counts = useMemo(() => ({
    verified: records.filter((record) => record.status === "VERIFIED").length,
    contradicted: records.filter((record) => record.status === "CONTRADICTED").length,
    unknown: records.filter((record) => record.status === "UNKNOWN").length,
  }), [records]);

  const totalChecks = records.length;
  const successRate = totalChecks
    ? Number(((counts.verified / totalChecks) * 100).toFixed(1))
    : 0;
  const latest = records[0];

  const stats = [
    {
      id: "verified",
      tone: "verified",
      label: "VERIFIED ACTIONS",
      value: String(counts.verified).padStart(2, "0"),
      highlight: `${counts.verified} recorded`,
      caption: "Confirmed by evidence",
    },
    {
      id: "contradicted",
      tone: "contradicted",
      label: "CONTRADICTED",
      value: String(counts.contradicted).padStart(2, "0"),
      highlight: `${counts.contradicted} recorded`,
      caption: "Evidence conflicts with claim",
    },
    {
      id: "unknown",
      tone: "unknown",
      label: "UNKNOWN",
      value: String(counts.unknown).padStart(2, "0"),
      highlight: `${counts.unknown} recorded`,
      caption: "Not enough valid evidence",
    },
  ];

  async function handleSubmit(event) {
    event.preventDefault();
    setFormError("");

    const expected = expectedObservation.trim();
    if (!expected) {
      setFormError("Enter the exact observation that should be true.");
      return;
    }

    const maxAge = Number(maxAgeSeconds);
    if (!Number.isFinite(maxAge) || maxAge < 0) {
      setFormError("Maximum evidence age must be a non-negative number.");
      return;
    }

    const observedAt = new Date().toISOString();
    const evidence = evidenceText
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean)
      .map((observation, index) => ({
        evidence_id: makeEvidenceId(index),
        source: source.trim() || "manual-input",
        observation,
        observed_at: observedAt,
        authoritative,
      }));

    const contradictoryObservations = [
      ...new Set(
        contradictionsText
          .split(/\r?\n/)
          .map((line) => line.trim())
          .filter(Boolean)
      ),
    ];

    setSubmitting(true);
    try {
      const result = await verifyClaim({
        expected_observation: expected,
        evidence,
        max_age_seconds: maxAge,
        contradictory_observations: contradictoryObservations,
      });

      onVerified({ ...result, expected_observation: expected });
      setFormOpen(false);
      setEvidenceText("");
      setContradictionsText("");
    } catch (error) {
      setFormError(error.message || "Verification request failed.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <div>
          <h1 className="dashboard__title">Verification overview</h1>
          <p className="dashboard__subtitle">
            Independently verify AI action claims against observed system state.
          </p>
          <span className="env-tag">
            <span className="env-tag__dot" /> API-CONNECTED WORKSPACE
          </span>
        </div>

        <button
          type="button"
          className="btn-primary"
          aria-expanded={formOpen}
          onClick={() => {
            setFormOpen((open) => !open);
            setFormError("");
          }}
        >
          <span aria-hidden="true">{formOpen ? "×" : "+"}</span>
          {formOpen ? "Close verification" : "Run new verification"}
        </button>
      </header>

      {historyError && (
        <div className="api-alert" role="status">
          Couldn't load saved history: {historyError}. You can still try a verification request.
        </div>
      )}

      {formOpen && (
        <section className="verify-form-card" aria-labelledby="verify-form-title">
          <div className="verify-form-card__header">
            <div>
              <h2 id="verify-form-title">New verification</h2>
              <p>Enter the expected state and any evidence returned by a trusted source.</p>
            </div>
          </div>

          <form className="verify-form" onSubmit={handleSubmit}>
            <label className="form-field">
              <span>Expected observation <strong aria-hidden="true">*</strong></span>
              <input
                value={expectedObservation}
                onChange={(event) => setExpectedObservation(event.target.value)}
                placeholder="e.g. user_access=revoked"
                required
              />
              <small>Evidence must match this text exactly, or match one of the contradictions below.</small>
            </label>

            <label className="form-field">
              <span>Evidence observations <small>(one per line)</small></span>
              <textarea
                rows={3}
                value={evidenceText}
                onChange={(event) => setEvidenceText(event.target.value)}
                placeholder={"e.g. user_access=revoked\nPaste observations from your source"}
              />
            </label>

            <div className="form-grid">
              <label className="form-field">
                <span>Evidence source</span>
                <input
                  value={source}
                  onChange={(event) => setSource(event.target.value)}
                  placeholder="e.g. IAM registry"
                />
              </label>
              <label className="form-field">
                <span>Maximum evidence age (seconds)</span>
                <input
                  type="number"
                  min="0"
                  step="1"
                  value={maxAgeSeconds}
                  onChange={(event) => setMaxAgeSeconds(event.target.value)}
                  required
                />
              </label>
            </div>

            <label className="form-checkbox">
              <input
                type="checkbox"
                checked={authoritative}
                onChange={(event) => setAuthoritative(event.target.checked)}
              />
              <span>
                Mark these supplied observations as authoritative
                <small>Only select this when the evidence really comes from a trusted source. This demo form does not authenticate the source itself.</small>
              </span>
            </label>

            <label className="form-field">
              <span>Contradictory observations <small>(optional, one per line)</small></span>
              <textarea
                rows={2}
                value={contradictionsText}
                onChange={(event) => setContradictionsText(event.target.value)}
                placeholder={"e.g. user_access=active"}
              />
            </label>

            {formError && <p className="form-error" role="alert">{formError}</p>}

            <div className="verify-form__actions">
              <button
                type="button"
                className="btn-secondary"
                onClick={() => {
                  setFormOpen(false);
                  setFormError("");
                }}
                disabled={submitting}
              >
                Cancel
              </button>
              <button type="submit" className="btn-primary" disabled={submitting}>
                {submitting ? "Verifying…" : "Verify observation"}
              </button>
            </div>
          </form>
        </section>
      )}

      <div className="dashboard__stats">
        {stats.map(({ id, ...props }) => (
          <StatCard key={id} {...props} />
        ))}
      </div>

      <div className="dashboard__row">
        <RecVerification verification={latest} />
        <SuccessRateChart
          rate={successRate}
          totalChecks={totalChecks}
          periodLabel="Loaded audit history"
        />
      </div>

      <p className="dashboard__data-note">
        Summary counts reflect the verification records currently returned by the backend audit history.
      </p>
    </div>
  );
}

export default Dashboard;
