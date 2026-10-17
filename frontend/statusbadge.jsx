import React from "react";

// Maps each status to a color variant defined in style.css (.pill--success / --danger / --warn)
const VARIANT = {
  verified: "success",
  match: "success",
  contradicted: "danger",
  unknown: "warn",
};

// status: "verified" | "match" | "contradicted" | "unknown"
// children: custom label (defaults to the upper-cased status)
function StatusBadge({ status = "verified", withIcon = false, children }) {
  const label = children ?? status.toUpperCase();

  return (
    <span className={`pill pill--${VARIANT[status] ?? "success"}`}>
      {withIcon && (
        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="m5 12.5 4.5 4.5L19 7.5" />
        </svg>
      )}
      {label}
    </span>
  );
}

export default StatusBadge;

