// Returns an array of roles of the form [role name, required signoffs number]
export default (rs, product, channel) => {
  const productRs = Object.entries(rs).find((item) => item[0] === product)[1];
  const roles = channel
    ? Object.entries(productRs.channels[channel])
    : Object.entries(productRs.permissions);

  // Formatted roles
  return roles.map(([name, role]) => {
    const isRoleScheduled = 'sc' in role;

    return {
      name,
      signoffs_required: role.signoffs_required,
      data_version: role.data_version,
      sc: isRoleScheduled
        ? {
            sc_id: role.sc.sc_id,
            signoffs_required: role.sc.signoffs_required,
            data_version: role.sc.sc_data_version,
            change_type: role.sc.change_type,
          }
        : null,
      metadata: {
        isAdditionalRole: false,
        id: `${product}-${channel}-${name}`,
      },
    };
  });
};
