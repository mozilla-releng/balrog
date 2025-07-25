import axios from 'axios';
import { stringify } from 'qs';

const getReleasesV2 = () => axios.get('/v2/releases');
const getReleaseV2 = (name) =>
  axios.get(`/v2/releases/${encodeURIComponent(name)}`);
const setRelease = ({ name, blob, oldDataVersions, when, product }) =>
  axios.put(`/v2/releases/${encodeURIComponent(name)}`, {
    name,
    blob,
    old_data_versions: oldDataVersions,
    when,
    product,
  });
const deleteReleaseV2 = (name) =>
  axios.delete(`/v2/releases/${encodeURIComponent(name)}`);
const setReadOnlyV2 = (name, readOnly, oldDataVersion) =>
  axios.put(`/v2/releases/${encodeURIComponent(name)}/read_only`, {
    read_only: readOnly,
    old_data_version: oldDataVersion,
  });
const getReleases = () => axios.get('/releases');
const getRelease = (name) => axios.get(`/releases/${encodeURIComponent(name)}`);
const getReleaseNames = () => axios.get('/releases?names_only=1');
const getReleaseNamesV2 = () => axios.get('/v2/releases?names_only=1');
const makeSignoffV2 = (name, role) =>
  axios.put(`/v2/releases/${encodeURIComponent(name)}/signoff`, { role });
const revokeSignoffV2 = (name) =>
  axios.delete(`/v2/releases/${encodeURIComponent(name)}/signoff`);
const deleteRelease = ({ name, dataVersion }) =>
  axios.delete(`/releases/${encodeURIComponent(name)}`, {
    params: { data_version: dataVersion },
  });
const setReadOnly = ({ name, readOnly, dataVersion }) =>
  axios.put(`/releases/${encodeURIComponent(name)}/read_only`, {
    read_only: readOnly,
    data_version: dataVersion,
  });
const getRevisions = (name, apiVersion) => {
  const bucket = name.includes('nightly')
    ? process.env.GCS_NIGHTLY_HISTORY_BUCKET
    : process.env.GCS_RELEASES_HISTORY_BUCKET;

  // Version 1 API Releases have one prefix per Release (${name}/)
  if (apiVersion === 1) {
    const releases = [];

    function parseReleases(rawReleases) {
      if (rawReleases) {
        rawReleases.forEach((r) => {
          const parts = r.name
            .replace(`${name}/`, '')
            .replace('.json', '')
            .split('-');
          const dataVersion = parseInt(parts[0], 10);
          const release = {
            name,
            path: null,
            data_version: Number(dataVersion) ? dataVersion : parts[0],
            timestamp: parseInt(parts[1], 10),
            changed_by: parts.slice(2).join('-'),
            data_url: r.mediaLink,
          };

          releases.push(release);
        });
      }
    }

    async function getReleases(url, pageToken) {
      const response = await axios.get(
        pageToken ? `${url}&pageToken=${pageToken}` : url,
      );

      parseReleases(response.data.items);

      if (response.data.nextPageToken) {
        return getReleases(url, response.data.nextPageToken);
      }

      // descending sort, so newer versions appear first
      return releases.sort((a, b) => a.data_version < b.data_version);
    }

    return getReleases(`${bucket}?prefix=${name}/&delimeter=/`);
  }

  // Version 2 API Releases have 1 prefix per Release (${name})
  // but must be grouped by whatever the string prior to "/" is.
  // The combination of the latest entry from each group adds
  // up to be the "current" version of the Release, while the older
  // revisions are outdated versions.

  function parseRevisions(rawRevisions) {
    const revisions = [];

    if (rawRevisions) {
      rawRevisions.forEach((r) => {
        if (!r.name.startsWith(`${name}/`) && !r.name.startsWith(`${name}-.`)) {
          return;
        }

        const [path, rest] = r.name
          .replace(`${name}-`, '')
          .replace(`${name}`, '')
          .replace('.json', '')
          .split('/');
        const parts = rest.split('-');
        const dataVersion = parseInt(parts[0], 10);
        const revision = {
          name,
          path,
          data_version: Number(dataVersion) ? dataVersion : parts[0],
          timestamp: parseInt(parts[1], 10),
          changed_by: parts.slice(2).join('-'),
          data_url: r.mediaLink,
        };

        revisions.push(revision);
      });
    }

    return revisions;
  }

  // make sure this works with page tokens
  async function getRevisions(url, pageToken, revisionsByPath) {
    const response = await axios.get(
      pageToken ? `${url}&pageToken=${pageToken}` : url,
    );

    parseRevisions(response.data.items).forEach((r) => {
      if (!(r.path in revisionsByPath)) {
        revisionsByPath[r.path] = [];
      }

      revisionsByPath[r.path].push(r);
    });

    if (response.data.nextPageToken) {
      return getRevisions(url, response.data.nextPageToken, revisionsByPath);
    }

    const latestEntries = [];
    const revisions = [];

    Object.values(revisionsByPath).forEach((pathRevisions) => {
      pathRevisions.sort((a, b) => a.timestamp > b.timestamp);
      // Split up the most recent revision for each path, and the
      // the remaining revisions.
      latestEntries.push(pathRevisions.pop());
      revisions.push(...pathRevisions);
    });

    revisions.sort((a, b) => a.timestamp < b.timestamp);

    return [latestEntries, revisions];
  }

  return getRevisions(`${bucket}?prefix=${name}&delimeter=/`, null, {});
};

const getScheduledChanges = (all) => {
  if (all === true) {
    return axios.get(`/scheduled_changes/releases?${stringify({ all: 1 })}`);
  }

  return axios.get('/scheduled_changes/releases');
};

const getScheduledChangeByName = (name) =>
  axios.get(`/scheduled_changes/releases?name=${name}`);
const getScheduledChangeById = (scId) =>
  axios.get(`/scheduled_changes/releases/${scId}`);
const createRelease = (name, product, blob) =>
  axios.post(`/releases`, { name, product, blob });
const addScheduledChange = (data) =>
  axios.post('/scheduled_changes/releases', data);
const updateScheduledChange = ({ scId, ...data }) =>
  axios.post(`/scheduled_changes/releases/${scId}`, data);
const deleteScheduledChange = ({ scId, scDataVersion }) =>
  // The backend wants sc_data_version, but calls it data_version.
  axios.delete(`/scheduled_changes/releases/${scId}`, {
    params: { data_version: scDataVersion },
  });
const getRequiredSignoffsForProduct = (name) =>
  axios.get(
    `/releases/${encodeURIComponent(name)}/read_only/product/required_signoffs`,
  );

// Releases factory
export {
  getReleasesV2,
  getReleaseV2,
  setRelease,
  deleteReleaseV2,
  setReadOnlyV2,
  getReleases,
  getRelease,
  getReleaseNames,
  getReleaseNamesV2,
  deleteRelease,
  setReadOnly,
  getRevisions,
  getScheduledChanges,
  getScheduledChangeByName,
  getScheduledChangeById,
  createRelease,
  addScheduledChange,
  updateScheduledChange,
  deleteScheduledChange,
  getRequiredSignoffsForProduct,
  makeSignoffV2,
  revokeSignoffV2,
};
