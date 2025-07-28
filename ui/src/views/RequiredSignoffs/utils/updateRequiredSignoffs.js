import {
  deleteScheduledChange,
  updateRequiredSignoff,
} from '../../../services/requiredSignoffs';

// A utlity to holds all of the Required Signoffs - product, permissions,
// and scheduled changes
export default (params) => {
  // For an entirely new Required Signoff (eg: a product/channel or
  // product/permissions that has no required roles yet,
  // we do not need to schedule the initial required role, we can
  // insert it directly. For other required roles that may be added,
  // we must schedule them.
  // Required Signoffs that have any existing required roles will
  // always required changes, additions, or deletions to be scheduled.
  const {
    product,
    channel,
    roles,
    originalRoles,
    additionalRoles,
    isNewSignoff,
  } = params;
  const currentRoles = roles.map((role) => role.name);
  const removed = originalRoles.filter(
    (role) => !currentRoles.includes(role.name),
  );
  let useScheduledChange = !isNewSignoff;

  return Promise.all(
    [].concat(
      roles.map(async (role) => {
        const extraData = role.sc
          ? { sc_data_version: role.sc.data_version }
          : {};
        let skip = false;

        originalRoles.forEach((value) => {
          const newSignoffsRequired = role.sc
            ? role.sc.signoffs_required
            : role.signoffs_required;
          const originalSignoffsRequired = value.sc
            ? value.sc.signoffs_required
            : value.signoffs_required;

          if (
            value.name === role.name &&
            originalSignoffsRequired === newSignoffsRequired
          ) {
            skip = true;
          }
        });

        if (skip) {
          return;
        }

        if (role.sc && role.signoffs_required === role.sc.signoffs_required) {
          return deleteScheduledChange({
            scId: role.sc.sc_id,
            type: channel ? 'product' : 'permissions',
            data_version: role.sc.data_version,
          });
        }

        return updateRequiredSignoff({
          product,
          channel,
          role: role.name,
          signoffs_required: role.sc
            ? role.sc.signoffs_required
            : role.signoffs_required,
          data_version: role.data_version,
          useScheduledChange: true,
          change_type: 'update',
          when: Date.now() + 30000,
          scId: role.sc ? role.sc.sc_id : null,
          ...extraData,
        });
      }),
      additionalRoles.map((role) => {
        const ret = updateRequiredSignoff({
          product,
          channel,
          useScheduledChange,
          role: role.name,
          signoffs_required: role.signoffs_required,
          change_type: 'insert',
          when: Date.now() + 30000,
        });

        useScheduledChange = true;

        return ret;
      }),
      removed.map((role) => {
        // role doesn't exist yet, we should just delete that scheduled change
        if (role.sc && role.sc.change_type === 'insert') {
          return deleteScheduledChange({
            scId: role.sc.sc_id,
            type: channel ? 'product' : 'permissions',
            data_version: role.sc.data_version,
          });
        }

        return updateRequiredSignoff({
          product,
          channel,
          role: role.name,
          data_version: role.data_version,
          useScheduledChange: true,
          change_type: 'delete',
          when: Date.now() + 30000,
        });
      }),
    ),
  );
};
