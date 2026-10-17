import React from "react";

const ICONS = {
  verified: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="m5 12.5 4.5 4.5L19 7.5" />
    </svg>
  ),
  contradicted: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="3.4" strokeLinecap="round" aria-hidden="true">
      <path d="M12 5v9M12 19h.01" />
    </svg>
  ),
  unknown: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M9.5 9a2.5 2.5 0 1 1 3.6 2.2c-.7.4-1.1 1-1.1 1.8M12 18h.01" />
    </svg>
  ),
};

// A clickable summary card that doubles as a filter toggle.
// active:  this card's outcome is the current filter
// dimmed:  another card's outcome is the current filter
function VerificationCard({ outcome, label, count, caption, active, dimmed, onToggle }) {
  const classes = [
    "outcome-card",
    `outcome-card--${outcome}`,
    active ? "outcome-card--active" : "",
    dimmed ? "outcome-card--dimmed" : "",
  ].join(" ");

  return (
    <button
      type="button"
      className={classes}
      aria-pressed={active}
      onClick={() => onToggle(outcome)}
    >
      <span className="outcome-card__icon">{ICONS[outcome]}</span>
      <span className="outcome-card__label">{label}</span>
      <span className="outcome-card__count">
        <strong>{String(count).padStart(2, "0")}</strong>
        <small>{caption}</small>
      </span>
    </button>
  );
}

export default VerificationCard;

