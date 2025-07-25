import { lensPath, set, view } from 'ramda';

const getChannelRoleLens = (rs) =>
  lensPath([rs.product, 'channels', rs.channel, rs.role]);
const getPermissionRoleLens = (rs) =>
  lensPath([rs.product, 'permissions', rs.role]);
const getChannelScheduledChangeLens = (rs) =>
  lensPath([rs.product, 'channels', rs.channel, rs.role, 'sc']);
const getPermissionScheduledChangeLens = (rs) =>
  lensPath([rs.product, 'permissions', rs.role, 'sc']);

export default class RequiredSignoffs {
  constructor() {
    this.val = {};
  }

  value() {
    return this.val;
  }

  setProductRequiredSignoffs(requiredSignoffs) {
    requiredSignoffs.forEach((rs) => {
      this.val = set(
        getChannelRoleLens(rs),
        {
          signoffs_required: rs.signoffs_required,
          data_version: rs.data_version,
        },
        this.val,
      );
    });
  }

  setPermissionsRequiredSignoffs(requiredSignoffs) {
    requiredSignoffs.forEach((rs) => {
      this.val = set(
        getPermissionRoleLens(rs),
        {
          signoffs_required: rs.signoffs_required,
          data_version: rs.data_version,
        },
        this.val,
      );
    });
  }

  setProductScheduledChanges(scheduledChanges) {
    scheduledChanges.forEach((rs) => {
      if (!view(getChannelRoleLens(rs), this.val)) {
        this.val = set(
          getChannelRoleLens(rs),
          {
            signoffs_required: 0,
            data_version: null,
          },
          this.val,
        );
      }

      this.val = set(
        getChannelScheduledChangeLens(rs),
        {
          required_signoffs: rs.required_signoffs,
          signoffs_required: rs.signoffs_required || 0,
          sc_id: rs.sc_id,
          scheduled_by: rs.scheduled_by,
          sc_data_version: rs.sc_data_version,
          signoffs: rs.signoffs,
          change_type: rs.change_type,
        },
        this.val,
      );
    });
  }

  setPermissionScheduledChanges(scheduledChanges) {
    scheduledChanges.forEach((rs) => {
      if (!view(getPermissionRoleLens(rs), this.val)) {
        this.val = set(
          getPermissionRoleLens(rs),
          {
            signoffs_required: 0,
            data_version: null,
          },
          this.val,
        );
      }

      this.val = set(
        getPermissionScheduledChangeLens(rs),
        {
          required_signoffs: rs.required_signoffs,
          signoffs_required: rs.signoffs_required || 0,
          sc_id: rs.sc_id,
          scheduled_by: rs.scheduled_by,
          sc_data_version: rs.sc_data_version,
          signoffs: rs.signoffs,
          change_type: rs.change_type,
        },
        this.val,
      );
    });
  }
}

RequiredSignoffs.instance = this;
