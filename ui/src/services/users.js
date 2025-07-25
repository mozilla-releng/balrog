import axios from 'axios';

const userExists = async (username) => {
  try {
    await axios.head(`/users/${username}`);

    return true;
  } catch {
    return false;
  }
};

const getUsers = () => axios.get('/users');
const getUserInfo = (username) => axios.get(`/users/${username}`);
const getScheduledChanges = () => axios.get('/scheduled_changes/permissions');
const addRole = (username, role) =>
  axios.put(`/users/${username}/roles/${role}`);
const removeRole = (username, role, dataVersion) =>
  axios.delete(`/users/${username}/roles/${role}`, {
    params: { data_version: dataVersion },
  });
const addScheduledPermissionChange = ({
  username,
  permission,
  options,
  dataVersion,
  changeType,
  when,
}) =>
  axios.post('/scheduled_changes/permissions', {
    username,
    permission,
    data_version: dataVersion,
    options: JSON.stringify(options),
    change_type: changeType,
    when,
  });
const updateScheduledPermissionChange = ({
  username,
  permission,
  options,
  dataVersion,
  scId,
  scDataVersion,
  when,
}) =>
  axios.post(`/scheduled_changes/permissions/${scId}`, {
    username,
    permission,
    data_version: dataVersion,
    options: JSON.stringify(options),
    sc_data_version: scDataVersion,
    when,
  });
const deleteScheduledPermissionChange = ({ scId, scDataVersion }) =>
  axios.delete(`/scheduled_changes/permissions/${scId}`, {
    params: {
      data_version: scDataVersion,
    },
  });

export {
  userExists,
  getUsers,
  getUserInfo,
  getScheduledChanges,
  addRole,
  removeRole,
  addScheduledPermissionChange,
  updateScheduledPermissionChange,
  deleteScheduledPermissionChange,
};
