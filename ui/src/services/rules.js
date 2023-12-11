import { stringify } from 'qs';
import axios from 'axios';

const getRules = (timestamp = null) =>
  timestamp ? axios.get(`/rules?timestamp=${timestamp}`) : axios.get('/rules');
const getRule = id => axios.get(`/rules/${id}`);
const getChannels = () => axios.get('/rules/columns/channel');
const getProducts = () => axios.get('/rules/columns/product');
const getRevisions = id => axios.get(`/rules/${id}/revisions?limit=10000`);
const deleteRule = ({ ruleId, dataVersion }) =>
  axios.delete(`/rules/${ruleId}`, { params: { data_version: dataVersion } });
const getScheduledChanges = all => {
  if (all === true) {
    return axios.get(`/scheduled_changes/rules?${stringify({ all: 1 })}`);
  }

  return axios.get('/scheduled_changes/rules');
};

const getScheduledChangeByRuleId = ruleId =>
  axios.get(`/scheduled_changes/rules?rule_id=${ruleId}`);
const getScheduledChangeByScId = scId =>
  axios.get(`/scheduled_changes/rules/${scId}`);
const addScheduledChange = data => axios.post(`/scheduled_changes/rules`, data);
const updateScheduledChange = ({ scId, ...data }) =>
  axios.post(`/scheduled_changes/rules/${scId}`, data);
const deleteScheduledChange = ({ scId, scDataVersion }) =>
  // The backend wants sc_data_version, but calls it data_version.
  axios.delete(`/scheduled_changes/rules/${scId}`, {
    params: { data_version: scDataVersion },
  });

// const getScheduledChangeHistory = () => axios.get();
// const signoffOnScheduledChange = () => axios.get();
// const revokeSignoffOnScheduledChange = () => axios.get();
// const ruleSignoffsRequired = () => axios.get();

// Rules factory
export {
  getRules,
  deleteRule,
  getRule,
  getChannels,
  getProducts,
  getRevisions,
  getScheduledChanges,
  getScheduledChangeByRuleId,
  getScheduledChangeByScId,
  addScheduledChange,
  updateScheduledChange,
  deleteScheduledChange,
};
