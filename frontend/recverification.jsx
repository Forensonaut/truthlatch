import React from "react";

/* Since statusbadge.jsx does not exist yet, the VERIFIED / MATCH "pills" within this card are defined here temporarily. 
Once statusbadge.jsx is created, this can simply be replaced with an import. */
function Pill({ children, check = false }) {
  return (
    <span className="pill pill--success">
      {check && (
        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="m5 12.5 4.5 4.5L19 7.5" />
        </svg>
      )}
      {children}
    </span>
  );
}

const DEFAULT_VERIFICATION = {
  title: "Revoke privileged access",
  id: "VER-2026-1048",
  category: "IAM / PERMISSIONS",
  status: "VERIFIED",
  claim: "User access was successfully revoked.",
  check: {
    summary: "IAM registry confirms access disabled",
    principal: "svc-deploy-prod",
    policy: "admin-write",
    result: "MATCH",
  },
  verifiedAt: "14:32:08 UTC",
  coverage: "3 of 3 checks passed",
};

function RecVerification({ verification = DEFAULT_VERIFICATION }) {
  const { title, id, category, status, claim, check, verifiedAt, coverage } = verification;

  return (
    <section className="rec-card" aria-label="Latest verification">
      <p className="rec-card__eyebrow">LATEST VERIFICATION</p>

      <header className="rec-card__header">
        <div>
          <h2 className="rec-card__title">{title}</h2>
          <p className="rec-card__meta">{id} · {category}</p>
        </div>
        <Pill check>{status}</Pill>
      </header>

      <hr className="rec-card__divider" />

      <div className="rec-card__block">
        <p className="rec-card__eyebrow">AI AGENT CLAIM</p>
        <p className="rec-card__claim">“{claim}”</p>
      </div>

      <div className="rec-card__block">
        <p className="rec-card__eyebrow">AUTHORITATIVE STATE CHECK</p>
        <div className="rec-check">
          <span className="rec-check__icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="m5 12.5 4.5 4.5L19 7.5" />
            </svg>
          </span>
          <div className="rec-check__text">
            <strong>{check.summary}</strong>
            <span>principal: {check.principal} · policy: {check.policy}</span>
          </div>
          <Pill>{check.result}</Pill>
        </div>
      </div>

      <hr className="rec-card__divider" />

      <footer className="rec-card__footer">
        <div>
          <p className="rec-card__eyebrow">VERIFIED AT</p>
          <p className="rec-card__time">{verifiedAt}</p>
        </div>
        <div>
          <p className="rec-card__eyebrow">EVIDENCE COVERAGE</p>
          <p className="rec-card__coverage">{coverage}</p>
        </div>
      </footer>
    </section>
  );
}

export default RecVerification;


