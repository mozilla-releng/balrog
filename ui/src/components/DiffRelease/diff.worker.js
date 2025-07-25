import { createTwoFilesPatch } from 'diff';

// biome-ignore lint/suspicious/noGlobalAssign: This module is imported as an object
onmessage = (e) => {
  const [
    firstFilename,
    secondFilename,
    firstReleaseString,
    secondReleaseString,
  ] = e.data;
  const releaseDiff = createTwoFilesPatch(
    firstFilename,
    secondFilename,
    firstReleaseString,
    secondReleaseString,
  );

  postMessage(releaseDiff);
};
