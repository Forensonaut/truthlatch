import React, { useState } from "react";
import SearchBar from "./searchbar.jsx";

function TopNavBar({
  breadcrumb = ["Workspace", "Overview"],
  user = { name: "Admin", role: "Security operator", initials: "AS" },
  hasNotification = true,
}) {
  const [query, setQuery] = useState("");

  return (
    <header className="topnav">
      {/* left side: breadcrumb */}
      <nav className="topnav__breadcrumb" aria-label="Breadcrumb">
        {breadcrumb.map((crumb, i) => (
          <React.Fragment key={crumb}>
            {i > 0 && <span className="topnav__sep">/</span>}
            <span
              className={i === breadcrumb.length - 1 ? "topnav__crumb--current" : ""}
            >
              {crumb}
            </span>
          </React.Fragment>
        ))}
      </nav>

      {/* right side: search bar + notification + profile*/}
      <div className="topnav__right">
        <SearchBar value={query} onChange={setQuery} />

        {hasNotification && (
          <span className="topnav__dot" role="status" aria-label="New notifications" />
        )}

        <div className="topnav__profile">
          <div className="topnav__avatar">{user.initials}</div>
          <div className="topnav__user">
            <strong>{user.name}</strong>
            <span>{user.role}</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default TopNavBar;

