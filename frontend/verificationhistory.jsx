import React, { useMemo, useState } from "react";
import VerificationCard from "./verificationcard.jsx";
import VerificationTable from "./verificationtable.jsx";

function formatTime(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function VerificationHistory({ records = [], error = "" }) {
  const [activeFilter, setActiveFilter] = useState(null);

  const counts = useMemo(() => ({
    verified: records.filter((record) => record.status === "VERIFIED").length,
    contradicted: records.filter((record) => record.status === "CONTRADICTED").length,
    unknown: records.filter((record) => record.status === "UNKNOWN").length,
  }), [records]);

  const rows = useMemo(() => records.map((record) => ({
    id: record.verification_id,
    action: record.expected_observation
      || record.evidence?.[0]?.observation
      || record.explanation
      || "Verification result",
    time: formatTime(record.checked_at),
    outcome: (record.status || "UNKNOWN").toLowerCase(),
  })), [records]);

  const visibleRows = activeFilter
    ? rows.filter((row) => row.outcome === activeFilter)
    : rows;

  function toggleFilter(outcome) {
    setActiveFilter((current) => current === outcome ? null : outcome);
  }

  return (
    <div className="history">
      <header className="history__header">
        <div>
          <h1 className="history__title">Verification history</h1>
          <p className="history__meta">
            Results loaded from the backend audit log.
          </p>
        </div>
        {activeFilter && (
          <button
            type="button"
            className="filter-chip"
            onClick={() => setActiveFilter(null)}
          >
            Showing {activeFilter.toUpperCase()} · Clear filter
          </button>
        )}
      </header>

      {error && (
        <div className="api-alert" role="status">
          Couldn't refresh saved history: {error}
        </div>
      )}

      <div className="outcome-cards" aria-label="Filter by verification outcome">
        <VerificationCard
          outcome="verified"
          label="Verified"
          count={counts.verified}
          caption="results"
          active={activeFilter === "verified"}
          dimmed={activeFilter !== null && activeFilter !== "verified"}
          onToggle={toggleFilter}
        />
        <VerificationCard
          outcome="contradicted"
          label="Contradicted"
          count={counts.contradicted}
          caption="results"
          active={activeFilter === "contradicted"}
          dimmed={activeFilter !== null && activeFilter !== "contradicted"}
          onToggle={toggleFilter}
        />
        <VerificationCard
          outcome="unknown"
          label="Unknown"
          count={counts.unknown}
          caption="results"
          active={activeFilter === "unknown"}
          dimmed={activeFilter !== null && activeFilter !== "unknown"}
          onToggle={toggleFilter}
        />
      </div>

      <section aria-labelledby="history-table-heading">
        <h2 id="history-table-heading" className="history__title">
          Recorded decisions
        </h2>
        <p className="history__meta">
          {visibleRows.length} result{visibleRows.length === 1 ? "" : "s"}
          {activeFilter ? ` · ${activeFilter.toUpperCase()}` : ""}
        </p>
        <VerificationTable rows={visibleRows} />
      </section>

      <p className="history__footer">
        This list reflects records returned by the backend audit log; it does not imply that Firebase connectivity has been verified.
      </p>
    </div>
  );
}

export default VerificationHistory;
