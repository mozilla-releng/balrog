import React, { Fragment } from 'react';

export default (highlights, releaseName) => {
    // The highlights array elements are arrays with pairs of indices representing:
        // 1. the first index of a match
        // 2. (the last index of a match) + 1
    if (highlights) {
      // The first array in highlights is ignored because it represents the:
        // 1. the first index of releaseName i.e. release.name[0]
        // 2. (the last index of releaseName that matched the searchValue) + 1

      // Add the first part of the release name before the first match
      const firstSubstring = releaseName.slice(0, highlights[1][0])
      const highlightedName = firstSubstring ? [firstSubstring] : [];

      for (let i = 1; i < highlights.length; i += 1) {
        // Add the highlighted matches with mark to highlight them
        highlightedName.push(
          <mark key={i}>{releaseName.slice(...highlights[i])}</mark>
        );

        if (highlights[i + 1]) {
          // If current match is not last element in array, add all characters between current match and next match
          highlightedName.push(
            releaseName.slice(highlights[i][1], highlights[i + 1][0])
          );
        } else {
          // If current match is last element in array and there are remaining characters in releaseName, add all remaining characters
            if (highlights[i][1] < releaseName.length) {
              highlightedName.push(
                releaseName.slice(highlights[i][1])
              );
            }
        }
      }
      return <Fragment>{highlightedName}</Fragment>;
    }
  };
