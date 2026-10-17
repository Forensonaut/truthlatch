import React, { useEffect, useRef } from "react";

/* Search box used within the top navbar. Focus with ⌘K / Ctrl+K */
function SearchBar({ value, onChange, placeholder = "Search verifications..." }) {
  const inputRef = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  return (
    <label className="searchbar">
      <svg
        className="searchbar__icon"
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        aria-hidden="true"
      >
        <circle cx="11" cy="11" r="7" />
        <path d="m20 20-3.5-3.5" />
      </svg>
      <input
        ref={inputRef}
        type="search"
        className="searchbar__input"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        aria-label="Search verifications"
      />
      <kbd className="searchbar__kbd">⌘ K</kbd>
    </label>
  );
}

export default SearchBar;

