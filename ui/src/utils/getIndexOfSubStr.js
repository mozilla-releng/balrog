// Function that returns the index of the
// (noOfOccurrences)th/st appearance of "subStr"
// inside of "word"
const getIndexOfSubStr = (word, subStr, noOfOccurrences) => {
  let currentIndex = 0;

  if (!word.includes(subStr)) {
    return -1;
  }

  for (
    let count = 0;
    count < noOfOccurrences && currentIndex < word.length;
    count += 1
  ) {
    currentIndex = word.indexOf(subStr, currentIndex + 1);

    // if currentIndex === -1, end the iteration because as soon as
    // indexOf() can't find the substr, it returns a value of -1...
    if (currentIndex === -1) {
      break;
    }
  }

  // ...so we then make use of the current index value "currentIndex",
  // which is what we are looking for, by returning it
  return currentIndex;
};

export default getIndexOfSubStr;
