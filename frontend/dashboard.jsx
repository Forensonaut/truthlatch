import React from "react";
import StatCard from "./statcard.jsx";
import SuccessRateChart from "./successratechart.jsx";
import RecVerification from "./recverification.jsx";

/* Currently using dummy data with values ​​taken directly from Figma. Will be replaced with an API response later. */
const STATS = [
  {
    id: "verified",
    tone: "verified",
    label: "VERIFIED ACTIONS",
    value: "128",
    highlight: "+12.8%",
    caption: "vs. previous 7 days",
  },
  {
    id: "contradicted",
    tone: "contradicted",
    label: "CONTRADICTED",
    value: "07",
    highlight: "2 require review",
    caption: "Claims disproved by state",
  },
  {
    id: "unknown",
    tone: "unknown",
    label: "UNKNOWN",
    value: "03",
    highlight: "Evidence incomplete",
    caption: "Needs another check",
  },
];

function Dashboard() {
  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <div>
          <h1 className="dashboard__title">Verification overview</h1>
          <p className="dashboard__subtitle">
            Independent proof that AI actions actually changed system state.
          </p>
          <span className="env-tag">
            <span className="env-tag__dot" /> DEMO ENVIRONMENT
          </span>
        </div>

        <button type="button" className="btn-primary">
          <span aria-hidden="true">+</span> Run new verification
        </button>
      </header>

      <div className="dashboard__stats">
        {STATS.map(({ id, ...props }) => (
          <StatCard key={id} {...props} />
        ))}
      </div>

      <div className="dashboard__row">
        <RecVerification />
        <SuccessRateChart rate={94.1} totalChecks={138} periodLabel="Last 7 days" />
      </div>
    </div>
  );
}

export default Dashboard;

