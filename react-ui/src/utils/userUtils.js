import { PERMISSION_RESTRICTION_MAPPINGS } from './constants';

// TODO: use https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ListFormat
// when it's available in Firefox
const formatListToLanguage = array =>
  array.concat(array.splice(-2, 2).join(' and ')).join(', ');
const permissionStrings = (productStr, actionStr) => ({
  admin: `is a full fledged administrator ${productStr}`,
  emergency_shutoff: `is allowed to ${actionStr} on Emergency Shutoffs ${productStr}`,
  release: `is allowed to ${actionStr} Releases ${productStr}`,
  release_locale: `is allowed to ${actionStr} on locale sections of Releases ${productStr}`,
  release_read_only: `is allowed to ${actionStr} the read only flag of Releases ${productStr}`,
  rule: `is allowed to ${actionStr} on Rules ${productStr}`,
  permission: `is allowed to ${actionStr} User Permissions`,
  required_signoff: `is allowed to ${actionStr} on Required Signoff configuration ${productStr}`,
  scheduled_change: `is allowed to ${actionStr} Scheduled Changes`,
});
const getPermissionString = (permission, actions, products) => {
  let actionStr = 'perform any action';
  let productStr = 'for all products';

  if (actions.length > 0) {
    actionStr = formatListToLanguage(actions);
  }

  if (products.length > 0) {
    const tmp = formatListToLanguage(products);

    productStr = `for ${tmp}`;
  }

  return permissionStrings(productStr, actionStr)[permission];
};

const getRolesString = roles => {
  const joined = formatListToLanguage(Array.from(roles));
  let roleStr = 'role';

  if (roles.length > 1) {
    roleStr = 'roles';
  }

  return `${joined} ${roleStr}`;
};

const supportsProductRestriction = permission => {
  if (!Object.keys(PERMISSION_RESTRICTION_MAPPINGS).includes(permission)) {
    return false;
  }

  return PERMISSION_RESTRICTION_MAPPINGS[permission].restrict_products;
};

const supportsActionRestriction = permission => {
  if (!Object.keys(PERMISSION_RESTRICTION_MAPPINGS).includes(permission)) {
    return false;
  }

  return PERMISSION_RESTRICTION_MAPPINGS[permission].restrict_actions;
};

const getSupportedActions = permission => {
  if (!Object.keys(PERMISSION_RESTRICTION_MAPPINGS).includes(permission)) {
    return [];
  }

  return PERMISSION_RESTRICTION_MAPPINGS[permission].supported_actions;
};

// eslint-disable-next-line import/prefer-default-export
export {
  getPermissionString,
  getRolesString,
  supportsProductRestriction,
  supportsActionRestriction,
  getSupportedActions,
};
