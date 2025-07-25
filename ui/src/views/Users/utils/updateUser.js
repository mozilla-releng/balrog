import { equals } from 'ramda';
import {
  addRole,
  removeRole,
  addScheduledPermissionChange,
  updateScheduledPermissionChange,
  deleteScheduledPermissionChange,
} from '../../../services/users';
import {
  supportsActionRestriction,
  supportsProductRestriction,
} from '../../../utils/userUtils';

export default params => {
  const {
    username,
    roles,
    originalRoles,
    additionalRoles,
    permissions,
    originalPermissions,
    additionalPermissions,
  } = params;
  const currentRoles = roles.map(role => role.name);
  const removedRoles = originalRoles.filter(
    role => !currentRoles.includes(role.name)
  );
  const currentPermissions = permissions.map(p => p.name);
  const removedPermissions = originalPermissions.filter(
    p => !currentPermissions.includes(p.name)
  );

  return Promise.all(
    [].concat(
      additionalRoles.map(role => addRole(username, role.name)),
      removedRoles.map(role =>
        removeRole(username, role.name, role.data_version)
      ),
      permissions.map(permission => {
        let skip = false;

        originalPermissions.forEach(value => {
          const newOptions = permission.sc
            ? permission.sc.options
            : permission.options;
          const originalOptions = value.sc ? value.sc.options : value.options;

          if (
            value.name === permission.name &&
            equals(newOptions, originalOptions)
          ) {
            skip = true;
          }
        });

        if (skip) {
          return;
        }

        if (
          permission.sc &&
          equals(permission.options, permission.sc.options)
        ) {
          return deleteScheduledPermissionChange({
            scId: permission.sc.sc_id,
            scDataVersion: permission.sc.sc_data_version,
          });
        }

        const options = {};

        if (supportsProductRestriction(permission.name)) {
          options.products = permission.sc
            ? permission.sc.options.products
            : permission.options.products;
        }

        if (supportsActionRestriction(permission.name)) {
          options.actions = permission.sc
            ? permission.sc.options.actions
            : permission.options.actions;
        }

        if (permission.sc) {
          return updateScheduledPermissionChange({
            username,
            permission: permission.name,
            options,
            dataVersion: permission.data_version,
            scId: permission.sc.sc_id,
            scDataVersion: permission.sc.sc_data_version,
            when: Date.now() + 30000,
          });
        }

        return addScheduledPermissionChange({
          username,
          permission: permission.name,
          options,
          dataVersion: permission.data_version,
          changeType: 'update',
          when: Date.now() + 30000,
        });
      }),
      additionalPermissions.map(permission => {
        const options = {};

        if (supportsProductRestriction(permission.name)) {
          options.products = permission.options.products;
        }

        if (supportsActionRestriction(permission.name)) {
          options.actions = permission.options.actions;
        }

        return addScheduledPermissionChange({
          username,
          permission: permission.name,
          options,
          changeType: 'insert',
          when: Date.now() + 30000,
        });
      }),
      removedPermissions.map(permission => {
        if (permission.sc) {
          return deleteScheduledPermissionChange({
            scId: permission.sc.sc_id,
            scDataVersion: permission.sc.sc_data_version,
          });
        }

        return addScheduledPermissionChange({
          username,
          permission: permission.name,
          dataVersion: permission.data_version,
          changeType: 'delete',
          when: Date.now() + 30000,
        });
      })
    )
  );
};
