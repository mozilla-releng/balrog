import React from "react";

// // highlighted search text
export const highlightText = (text, searchTerm) => {
  if (!searchTerm) {
    return text;
  }
  const searchTerms = searchTerm.toLowerCase().split(" ");
  return text.split("\n").map((line, index) => {
    const highlightedLine = searchTerms.reduce((acc, term) => {
      if (term) {
        const regex = new RegExp(term, "gi");
        return acc.replace(
          regex,
          (match) =>
            `<span style="background-color: #804cc5; color: white;">${match}</span>`
        );
      } else {
        return acc;
      }
    }, line);
    return (
      <div key={index} dangerouslySetInnerHTML={{ __html: highlightedLine }} />
    );
  });
};
