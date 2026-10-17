import React from "react";

/* Icons are handled as inline SVGs without external libraries (can be replaced with lucide-react later) */
const iconProps = {
  width: 16,
  height: 16,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.8,
  strokeLinecap: "round",
  strokeLinejoin: "round",
  "aria-hidden": true,
};

const Icons = {
  home: (
    <svg {...iconProps}>
      <rect x="3" y="3" width="7" height="18" rx="1.5" />
      <rect x="14" y="3" width="7" height="8" rx="1.5" />
    </svg>
  ),
  history: (
    <svg {...iconProps}>
      <path d="M3 12a9 9 0 1 0 3-6.7" />
      <path d="M3 4v5h5" />
      <path d="M12 8v4l3 2" />
    </svg>
  ),
  vault: (
    <svg {...iconProps}>
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <path d="M3 10h18M3 15h18" />
    </svg>
  ),
  audit: (
    <svg {...iconProps}>
      <path d="M3 9c3-3 6 3 9 0s6 3 9 0" />
      <path d="M3 15c3-3 6 3 9 0s6 3 9 0" />
    </svg>
  ),
  about: (
    <svg {...iconProps}>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 11v5M12 8h.01" />
    </svg>
  ),
  faq: (
    <svg {...iconProps}>
      <path d="M9.5 9a2.5 2.5 0 1 1 3.6 2.2c-.7.4-1.1 1-1.1 1.8" />
      <path d="M12 17h.01" />
    </svg>
  ),
};

const WORKSPACE_ITEMS = [
  { id: "home", label: "Home", icon: Icons.home },
  { id: "history", label: "Verification history", icon: Icons.history },
  { id: "vault", label: "Evidence vault", icon: Icons.vault },
  { id: "audit", label: "Audit trail", icon: Icons.audit },
];

const OTHER_ITEMS = [
  { id: "about", label: "About Us", icon: Icons.about },
  { id: "faq", label: "FAQ's", icon: Icons.faq },
];

function NavItem({ item, active, onNavigate }) {
  return (
    <li>
      <button
        type="button"
        className={`nav-item ${active ? "nav-item--active" : ""}`}
        aria-current={active ? "page" : undefined}
        onClick={() => onNavigate(item.id)}
      >
        <span className="nav-item__icon">{item.icon}</span>
        <span className="nav-item__label">{item.label}</span>
      </button>
    </li>
  );
}

function Sidebar({ activePage = "home", onNavigate = () => {} }) {
  return (
    <aside className="sidebar">
      {/* logo */}
      <div className="sidebar__brand">
        <div className="brand-mark">T</div>
        <div className="brand-text">
          <strong>TruthLatch</strong>
          <span>AI action verification</span>
        </div>
      </div>

      {/* workspace card */}
      <div className="workspace-card">
        <div className="workspace-card__avatar">Z</div>
        <div className="workspace-card__text">
          <strong>IBM Z Sandbox</strong>
          <span>Demo environment</span>
        </div>
      </div>

      {/* Workspace menu */}
      <nav aria-label="Workspace">
        <p className="sidebar__group-label">Workspace</p>
        <ul className="nav-list">
          {WORKSPACE_ITEMS.map((item) => (
            <NavItem
              key={item.id}
              item={item}
              active={activePage === item.id}
              onNavigate={onNavigate}
            />
          ))}
        </ul>
      </nav>

      {/* Other menu */}
      <nav aria-label="Other">
        <p className="sidebar__group-label">Other</p>
        <ul className="nav-list">
          {OTHER_ITEMS.map((item) => (
            <NavItem
              key={item.id}
              item={item}
              active={activePage === item.id}
              onNavigate={onNavigate}
            />
          ))}
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;

