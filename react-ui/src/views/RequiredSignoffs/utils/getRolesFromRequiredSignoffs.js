// Returns an array of roles of the form [role name, required signoffs number]
export default (rs, product, channel) => {
  const productRs = Object.entries(rs).find(item => item[0] === product)[1];
  const roles = channel
    ? Object.entries(productRs.channels[channel])
    : Object.entries(productRs.permissions);

  // Formatted roles
  return roles.map(([name, role]) => {
    const isRoleScheduled = 'sc' in role;

    return [
      name,
      isRoleScheduled ? role.sc.signoffs_required : role.signoffs_required,
      {
        isAdditionalRole: false,
        id: `${product}-${channel}-${name}`,
      },
    ];
  });
};
