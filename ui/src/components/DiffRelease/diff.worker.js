import { createTwoFilesPatch } from 'diff';

onmessage = e => {
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
    secondReleaseString
  );

  postMessage(releaseDiff);
};
