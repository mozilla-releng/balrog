import axios from 'axios';
import { getRevisions } from '../src/services/releases';

jest.mock('axios');

const name = 'Firefox-test-nightly-latest';
const item = (objectName) => ({
  name: objectName,
  mediaLink: `https://gcs.example/${objectName}`,
});

describe('getRevisions', () => {
  afterEach(() => {
    axios.get.mockReset();
  });

  test('v2 groups revisions by part of the Release', async () => {
    const platform = `${name}-.platforms.WINNT_x86-msvc.locales.de`;

    // GCS lists objects in lexicographic order, so data_version 10
    // comes before 9, and platform parts come before the base part.
    axios.get.mockResolvedValueOnce({
      data: {
        items: [
          item(`${platform}/10-1000-ffxbld.json`),
          item(`${platform}/9-900-ffxbld.json`),
          item(`${name}-.platforms.Darwin.locales.fr/1-500-ffxbld.json`),
        ],
        nextPageToken: 'next',
      },
    });
    axios.get.mockResolvedValueOnce({
      data: {
        items: [item(`${name}/3-2000-someone@example.com.json`)],
      },
    });

    const [latest, revisions] = await getRevisions(name, 2);

    expect(axios.get).toHaveBeenLastCalledWith(
      expect.stringContaining('&pageToken=next'),
    );
    expect(latest.map((r) => [r.path, r.data_version])).toStrictEqual([
      ['', 3],
      ['.platforms.WINNT_x86-msvc.locales.de', 10],
      ['.platforms.Darwin.locales.fr', 1],
    ]);
    expect(latest[0].changed_by).toBe('someone@example.com');
    expect(revisions.map((r) => r.timestamp)).toStrictEqual([
      2000, 1000, 900, 500,
    ]);
  });

  test('v1 sorts revisions by descending data_version', async () => {
    axios.get.mockResolvedValueOnce({
      data: {
        items: [
          item(`${name}/10-1000-ffxbld.json`),
          item(`${name}/11-1100-ffxbld.json`),
          item(`${name}/9-900-ffxbld.json`),
        ],
      },
    });

    const revisions = await getRevisions(name, 1);

    expect(revisions.map((r) => r.data_version)).toStrictEqual([11, 10, 9]);
  });
});
