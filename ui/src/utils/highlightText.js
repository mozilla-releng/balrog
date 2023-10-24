import React from "react";

export const highlightText = (text, searchTerm) => {
  if (!searchTerm) {
    return <span>{text}</span>;
  }

  const searchTerms = searchTerm.toLowerCase().split(" ");

  const parts = text.split(new RegExp(`(${searchTerms.join("|")})`, "gi"));
  return (
    <span>
      {parts.map((part, index) => {
        const isTextHighlighted = searchTerms.some(
          (term) => part.toLowerCase() === term
        );
        return isTextHighlighted ? (
          <span
            key={index}
            style={{ backgroundColor: "#804cc5", color: "white" }}
          >
            {part}
          </span>
        ) : (
          <span key={index}>{part}</span>
        );
      })}
    </span>
  );
};
