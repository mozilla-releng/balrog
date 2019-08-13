import { getUserInfo, getScheduledChanges } from '../../../services/users';

export default async users => {
  const userInfo = {};
  const userData = await Promise.all(
    [].concat(users.map(user => getUserInfo(user)))
  );
  const scData = await getScheduledChanges();

  userData.forEach(user => {
    userInfo[user.data.username] = {
      roles: user.data.roles,
      permissions: user.data.permissions,
      scheduledPermissions: {},
    };
  });

  scData.data.scheduled_changes.forEach(sc => {
    if (!(sc.username in userInfo)) {
      userInfo[sc.username] = {
        roles: {},
        permissions: {},
        scheduledPermissions: {},
      };
    }

    userInfo[sc.username].scheduledPermissions[sc.permission] = sc;
  });

  return userInfo;
};
