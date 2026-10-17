import React from "react";

const DOT_COUNT = 72;
const SIZE = 220;
const CENTER = SIZE / 2;
const RADIUS = 92;
const DOT_RADIUS = 2.6;

/* rate: 0–100. Draw a circle using 72 dots, and fill a portion corresponding to 'rate' with green (starting from the 12 o'clock position and moving clockwise). */
function SuccessRateChart({
  rate = 94.1,
  totalChecks = 138,
  periodLabel = "Last 7 days",
}) {
  const dots = Array.from({ length: DOT_COUNT }, (_, i) => {
    const angle = (i / DOT_COUNT) * 2 * Math.PI - Math.PI / 2;
    const filled = ((i + 0.5) / DOT_COUNT) * 100 <= rate;
    return {
      key: i,
      cx: CENTER + RADIUS * Math.cos(angle),
      cy: CENTER + RADIUS * Math.sin(angle),
      filled,
    };
  });

  return (
    <section className="rate-card" aria-label="Verification success rate">
      <h2 className="rate-card__title">Verification success rate</h2>
      <p className="rate-card__subtitle">Claims confirmed by authoritative evidence</p>

      <div className="rate-card__chart">
        <svg
          viewBox={`0 0 ${SIZE} ${SIZE}`}
          width="100%"
          role="img"
          aria-label={`${rate}% of claims verified across ${totalChecks} checks`}
        >
          {dots.map((d) => (
            <circle
              key={d.key}
              cx={d.cx}
              cy={d.cy}
              r={DOT_RADIUS}
              className={d.filled ? "rate-dot rate-dot--on" : "rate-dot"}
            />
          ))}
        </svg>
        <div className="rate-card__center">
          <strong>{rate}%</strong>
          <span>VERIFIED</span>
        </div>
      </div>

      <p className="rate-card__total">Across {totalChecks} checks</p>
      <p className="rate-card__period">{periodLabel}</p>

      <ul className="rate-card__legend">
        <li><span className="legend-dot legend-dot--on" /> Verified</li>
        <li><span className="legend-dot" /> Not verified</li>
      </ul>
    </section>
  );
}

export default SuccessRateChart;
