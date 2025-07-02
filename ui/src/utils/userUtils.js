import { PERMISSION_RESTRICTION_MAPPINGS } from './constants';

// TODO: use https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ListFormat
// when it's available in Firefox
const formatListToLanguage = array =>
  [].concat(array.slice(null, -2), array.slice(-2).join(' and ')).join(', ');
const permissionStrings = (productStr, actionStr) => ({
  admin: `a full fledged administrator ${productStr}`,
  emergency_shutoff: `allowed to ${actionStr} Emergency Shutoffs ${productStr}`,
  release: `allowed to ${actionStr} Releases ${productStr}`,
  release_locale: `allowed to ${actionStr} locale sections of Releases ${productStr}`,
  release_read_only: `allowed to ${actionStr} the read only flag of Releases ${productStr}`,
  rule: `allowed to ${actionStr} Rules ${productStr}`,
  permission: `allowed to ${actionStr} User Permissions`,
  required_signoff: `allowed to ${actionStr} on Required Signoff configuration ${productStr}`,
  scheduled_change: `allowed to ${actionStr} Scheduled Changes`,
  pinnable_release: `allowed to manage Pinnable Releases ${productStr}`,
});
const getPermissionString = (
  permission,
  actions,
  products,
  scheduledChangeType = null
) => {
  const prefix =
    (scheduledChangeType &&
      (scheduledChangeType === 'delete' ? 'will no longer be' : 'will be')) ||
    'is';
  let actionStr = 'perform any action on';
  let productStr = 'for all products';

  if (actions.length > 0) {
    actionStr = formatListToLanguage(actions);
  }

  if (products.length > 0) {
    const tmp = formatListToLanguage(products);

    productStr = `for ${tmp}`;
  }

  return `${prefix} ${permissionStrings(productStr, actionStr)[permission]}`;
};

const getRolesString = roles => {
  const joined = formatListToLanguage(roles.map(role => role.role));
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

export {
  getPermissionString,
  getRolesString,
  supportsProductRestriction,
  supportsActionRestriction,
  getSupportedActions,
};
