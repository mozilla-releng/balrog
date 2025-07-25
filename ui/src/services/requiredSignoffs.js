import axios from 'axios';

const getRequiredSignoffs = (objectName) => axios.get(`/${objectName}`);
const getScheduledChanges = (objectName) =>
  axios.get(`/scheduled_changes/${objectName}`);
const updateRequiredSignoff = (params) => {
  const { useScheduledChange, scId, ...postData } = params;
  const type = postData.channel ? 'product' : 'permissions';
  const scPath = scId ? `/${scId}` : '';
  const url = useScheduledChange
    ? `/scheduled_changes/required_signoffs/${type}${scPath}`
    : `/required_signoffs/${type}`;

  return axios.post(url, postData);
};

const deleteScheduledChange = (params) => {
  const { scId, type, ...data } = params;
  const url = `/scheduled_changes/required_signoffs/${type}/${scId}`;

  return axios.delete(url, {
    params: data,
  });
};

// requiredSignoffs factory
export {
  getRequiredSignoffs,
  getScheduledChanges,
  updateRequiredSignoff,
  deleteScheduledChange,
};
