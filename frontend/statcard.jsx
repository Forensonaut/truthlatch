import React from "react";

/* tone: "verified" | "contradicted" | "unknown" → determines the color of the icon box and the supplementary text */
const ICONS = {
  verified: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m5 12.5 4.5 4.5L19 7.5" />
    </svg>
  ),
  contradicted: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="2.6" strokeLinecap="round" aria-hidden="true">
      <path d="M12 5v9M12 19h.01" />
    </svg>
  ),
  unknown: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M9.5 9a2.5 2.5 0 1 1 3.6 2.2c-.7.4-1.1 1-1.1 1.8M12 18h.01" />
    </svg>
  ),
};

function StatCard({ label, value, highlight, caption, tone = "verified" }) {
  return (
    <article className={`stat-card stat-card--${tone}`}>
      <header className="stat-card__header">
        <span className="stat-card__label">{label}</span>
        <span className="stat-card__icon">{ICONS[tone]}</span>
      </header>

      <p className="stat-card__value">{value}</p>

      <div className="stat-card__meta">
        <span className="stat-card__highlight">{highlight}</span>
        <span className="stat-card__caption">{caption}</span>
      </div>
    </article>
  );
}

export default StatCard;

