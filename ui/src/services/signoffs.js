import axios from 'axios';

const makeSignoff = ({ type, scId, role }) =>
  axios.post(`/scheduled_changes/${type}/${scId}/signoffs`, { role });
const revokeSignoff = ({ type, scId }) =>
  axios.delete(`/scheduled_changes/${type}/${scId}/signoffs`);

export { makeSignoff, revokeSignoff };
