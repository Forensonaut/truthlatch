import React from "react";
import StatusBadge from "./statusbadge.jsx";

// rows: [{ id, action, time, outcome }]
function VerificationTable({ rows }) {
  if (rows.length === 0) {
    return <p className="vtable__empty">No verifications match this filter.</p>;
  }

  return (
    <div className="vtable-wrap">
      <table className="vtable">
        <thead>
          <tr>
            <th scope="col">ACTION</th>
            <th scope="col">TIME</th>
            <th scope="col">OUTCOME</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td className="vtable__action">
                <strong>{row.action}</strong>
                <span>{row.id}</span>
              </td>
              <td className="vtable__time">{row.time}</td>
              <td>
                <StatusBadge status={row.outcome} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default VerificationTable;

