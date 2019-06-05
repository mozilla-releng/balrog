import axios from 'axios';
import { stringify } from 'qs';

const baseUrl = `${process.env.BALROG_ROOT_URL}/api`;
const getRules = () => axios.get(`${baseUrl}/rules`);
const getChannels = () => axios.get(`${baseUrl}/rules/columns/channel`);
const getProducts = () => axios.get(`${baseUrl}/rules/columns/product`);
const getHistory = (id, limit, page) =>
  axios.get(`${baseUrl}/${id}/revisions?${stringify({ limit, page })}`);
// const getRule = () => axios.get();
// const updateRule = () => axios.put();
// const deleteRule = () => axios.delete();
// const addRule = () => axios.post();
// const revertRule = () => axios.post();
const getScheduledChanges = all => {
  if (!all || all === true) {
    return axios.get(
      `${baseUrl}/scheduled_changes/rules?${stringify({ all: 1 })}`
    );
  }

  return axios.get(`${baseUrl}/scheduled_changes/rules/`);
};
// const getScheduledChange = () => axios.get();
// const addScheduledChange = () => axios.get();
// const getScheduledChangeHistory = () => axios.get();
// const updateScheduledChange = () => axios.get();
// const deleteScheduledChange = () => axios.get();
// const signoffOnScheduledChange = () => axios.get();
// const revokeSignoffOnScheduledChange = () => axios.get();
// const ruleSignoffsRequired = () => axios.get();

// Rules factory
export { getRules, getChannels, getProducts, getHistory, getScheduledChanges };
