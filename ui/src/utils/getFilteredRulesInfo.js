// This utility builds the string shown in the
// info alert when no rules match the selected filters
export default (productChannelQueries, rewindDate, onlyScheduledChanges) => {
  let info = 'No rules found ';
  const rewindDateStr = `on ${rewindDate}.`;
  const scheduledChangesStr = 'with scheduled changes.';

  if (!productChannelQueries) {
    if (rewindDate) {
      info += rewindDateStr;
    } else if (onlyScheduledChanges) {
      info += scheduledChangesStr;
    }
  } else if (productChannelQueries[1]) {
    info += `for the ${productChannelQueries[0]} ${productChannelQueries[1]} channel `;

    if (rewindDate) {
      info += rewindDateStr;
    } else if (onlyScheduledChanges) {
      info += scheduledChangesStr;
    }
  } else {
    info += `for the ${productChannelQueries[0]} channel `;

    if (rewindDate) {
      info += rewindDateStr;
    } else if (onlyScheduledChanges) {
      info += scheduledChangesStr;
    }
  }

  return info;
};
