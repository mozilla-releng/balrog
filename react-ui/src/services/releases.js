import axios from 'axios';

const getReleases = () => axios.get('/releases');
const getReleaseNames = () => axios.get(`/releases?names_only=1`);

// Releases factory
// eslint-disable-next-line import/prefer-default-export
export { getReleases, getReleaseNames };
