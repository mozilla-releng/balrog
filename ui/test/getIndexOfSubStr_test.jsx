import getIndexOfSubStr from '../src/utils/getIndexOfSubStr';

const word = "Hi, I'm AMUZY, an outreachy intern";
const noOfOccurrences = 2;

describe('searching through a string', () => {
  test('should return index of occurrence of substring in a string', () => {
    const subStr = ',';
    const index = getIndexOfSubStr(word, subStr, noOfOccurrences);

    expect(index).toEqual(13);
  });

  test('shoud return -1 when substring does not exist in string', () => {
    const subStr = 'fail';
    const index = getIndexOfSubStr(word, subStr, noOfOccurrences);

    expect(index).toEqual(-1);
  });
});
