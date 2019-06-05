import { lensPath, set, view } from 'ramda';

const getChannelRoleLens = rs =>
  lensPath([rs.product, 'channels', rs.channel, rs.role]);
const getPermissionRoleLens = rs =>
  lensPath([rs.product, 'permissions', rs.role]);
const getChannelScheduledChangeLens = rs =>
  lensPath([rs.product, 'channels', rs.channel, rs.role, 'sc']);
const getPermissionScheduledChangeLens = rs =>
  lensPath([rs.product, 'permissions', rs.role, 'sc']);

export default class RequiredSignoffs {
  #value = {};

  value() {
    return this.#value;
  }

  setProductRequiredSignoffs(requiredSignoffs) {
    requiredSignoffs.forEach(rs => {
      this.#value = set(
        getChannelRoleLens(rs),
        {
          signoffs_required: rs.signoffs_required,
          data_version: rs.data_version,
        },
        this.#value
      );
    });
  }

  setPermissionsRequiredSignoffs(requiredSignoffs) {
    requiredSignoffs.forEach(rs => {
      this.#value = set(
        getPermissionRoleLens(rs),
        {
          signoffs_required: rs.signoffs_required,
          data_version: rs.data_version,
        },
        this.#value
      );
    });
  }

  setProductScheduledChanges(scheduledChanges) {
    scheduledChanges.forEach(rs => {
      if (!view(getChannelRoleLens(rs), this.#value)) {
        this.#value = set(
          getChannelRoleLens(rs),
          {
            signoffs_required: 0,
            data_version: null,
          },
          this.#value
        );
      }

      this.#value = set(
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
        this.#value
      );
    });
  }

  setPermissionScheduledChanges(scheduledChanges) {
    scheduledChanges.forEach(rs => {
      if (!view(getPermissionRoleLens(rs), this.#value)) {
        this.#value = set(
          getPermissionRoleLens(rs),
          {
            signoffs_required: 0,
            data_version: null,
          },
          this.#value
        );
      }

      this.#value = set(
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
        this.#value
      );
    });
  }
}

RequiredSignoffs.instance = this;
