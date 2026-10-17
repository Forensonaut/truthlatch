import React, { useState } from "react";
import Sidebar from "./sidebar.jsx";
import TopNavBar from "./topnavbar.jsx";
import Dashboard from "./dashboard.jsx";
import VerificationHistory from "./verificationhistory.jsx";
import "./style.css";

// Page titles used for the breadcrumb and for pages that are not built yet
const PAGE_TITLES = {
  home: "Overview",
  history: "Verification History",
  vault: "Evidence Vault",
  audit: "Audit Trail",
  about: "About Us",
  faq: "FAQ's",
};

function renderPage(activePage) {
  switch (activePage) {
    case "home":
      return <Dashboard />;
    case "history":
      return <VerificationHistory />;
    default:
      // Placeholder until the remaining pages are implemented
      return (
        <div className="dashboard">
          <h1 className="dashboard__title">{PAGE_TITLES[activePage]}</h1>
          <p className="dashboard__subtitle">Coming soon.</p>
        </div>
      );
  }
}

function App() {
  const [activePage, setActivePage] = useState("home");

  return (
    <div className="app">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />

      <div className="app__main">
        <TopNavBar breadcrumb={["Workspace", PAGE_TITLES[activePage]]} />
        <main className="app__content">{renderPage(activePage)}</main>
      </div>
    </div>
  );
}

export default App;

