import React, { useEffect, useState } from "react";
import Sidebar from "./sidebar.jsx";
import TopNavBar from "./topnavbar.jsx";
import Dashboard from "./dashboard.jsx";
import VerificationHistory from "./verificationhistory.jsx";
import { fetchHistory } from "./api.js";
import "./style.css";

const PAGE_TITLES = {
  home: "Overview",
  history: "Verification History",
  vault: "Evidence Vault",
  audit: "Audit Trail",
  about: "About Us",
  faq: "FAQ's",
};

function App() {
  const [activePage, setActivePage] = useState("home");
  const [records, setRecords] = useState([]);
  const [historyError, setHistoryError] = useState("");

  useEffect(() => {
    let isCurrent = true;

    fetchHistory()
      .then((history) => {
        if (isCurrent) {
          setRecords(Array.isArray(history) ? history : []);
          setHistoryError("");
        }
      })
      .catch((error) => {
        if (isCurrent) setHistoryError(error.message);
      });

    return () => {
      isCurrent = false;
    };
  }, []);

  function handleVerified(record) {
    setRecords((current) => [
      record,
      ...current.filter((item) => item.verification_id !== record.verification_id),
    ]);
    setHistoryError("");
  }

  let page;
  if (activePage === "home") {
    page = (
      <Dashboard
        records={records}
        onVerified={handleVerified}
        historyError={historyError}
      />
    );
  } else if (activePage === "history") {
    page = <VerificationHistory records={records} error={historyError} />;
  } else {
    page = (
      <div className="dashboard">
        <h1 className="dashboard__title">{PAGE_TITLES[activePage]}</h1>
        <p className="dashboard__subtitle">This workspace page is not connected yet.</p>
      </div>
    );
  }

  return (
    <div className="app">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />
      <div className="app__main">
        <TopNavBar breadcrumb={["Workspace", PAGE_TITLES[activePage]]} />
        <main className="app__content">{page}</main>
      </div>
    </div>
  );
}

export default App;
