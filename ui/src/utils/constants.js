export const USER_SESSION = 'react-auth0-session';
export const BASE_URL = `${process.env.BALROG_ROOT_URL}`;
export const OBJECT_NAMES = {
  PERMISSIONS_REQUIRED_SIGNOFF: 'required_signoffs/permissions',
  PRODUCT_REQUIRED_SIGNOFF: 'required_signoffs/product',
};
export const LABELS = {
  PENDING: 'pending',
  PENDING_INSERT: 'pendingInsert',
  PENDING_DELETE: 'pendingDelete',
  PENDING_UPDATE: 'pendingUpdate',
};
export const RULE_DIFF_PROPERTIES = [
  'alias',
  'fallbackMapping',
  'mapping',
  'backgroundRate',
  'buildTarget',
  'buildID',
  'comment',
  'data_version',
  'distVersion',
  'distribution',
  'headerArchitecture',
  'instructionSet',
  'jaws',
  'locale',
  'memory',
  'mig64',
  'osVersion',
  'priority',
  'product',
  'channel',
  'rule_id',
  'update_type',
  'version',
];
// Products that use only a subset of the available Rule fields
// should define them here.
export const RULE_PRODUCT_UNSUPPORTED_PROPERTIES = {
  Guardian: [
    'buildID',
    'distVersion',
    'distribution',
    'headerArchitecture',
    'instructionSet',
    'jaws',
    'locale',
    'memory',
    'mig64',
    'osVersion',
  ],
};
export const CONTENT_MAX_WIDTH = 980;
export const APP_BAR_HEIGHT = 64;
export const SNACKBAR_AUTO_HIDE_DURATION = 5000;
export const SNACKBAR_INITIAL_STATE = {
  message: '',
  variant: 'success',
  open: false,
};
export const DIALOG_ACTION_INITIAL_STATE = {
  error: null,
  title: '',
  body: '',
  confirmText: '',
  item: null,
  open: false,
  destructive: false,
  mode: null,
  handleSubmit: Function.prototype,
  handleClose: Function.prototype,
  handleError: Function.prototype,
  handleComplete: Function.prototype,
};
export const EMPTY_MENU_ITEM_CHAR = '-';
// product/action restrictions need to match the backend definitions from
// https://github.com/mozilla/balrog/blob/main/auslib/db.py#L2144
export const PERMISSION_RESTRICTION_MAPPINGS = {
  admin: {
    restrict_products: true,
    restrict_actions: false,
    supported_actions: [],
  },
  emergency_shutoff: {
    restrict_products: true,
    restrict_actions: true,
    supported_actions: ['create', 'modify'],
  },
  rule: {
    restrict_products: true,
    restrict_actions: true,
    supported_actions: ['create', 'modify', 'delete'],
  },
  release: {
    restrict_products: true,
    restrict_actions: true,
    supported_actions: ['create', 'modify', 'delete'],
  },
  release_read_only: {
    restrict_products: true,
    restrict_actions: true,
    supported_actions: ['set', 'unset'],
  },
  release_locale: {
    restrict_products: true,
    restrict_actions: true,
    supported_actions: ['modify'],
  },
  required_signoff: {
    restrict_products: true,
    restrict_actions: false,
    supported_actions: ['create', 'modify', 'delete'],
  },
  permission: {
    restrict_products: false,
    restrict_actions: true,
    supported_actions: ['create', 'modify', 'delete'],
  },
  scheduled_change: {
    restrict_products: false,
    restrict_actions: true,
    supported_actions: ['enact'],
  },
  pinnable_release: {
    restrict_products: true,
    restrict_actions: false,
    supported_actions: [],
  },
};
export const ALL_PERMISSIONS = [
  'admin',
  'emergency_shutoff',
  'rule',
  'release',
  'release_read_only',
  'release_locale',
  'required_signoff',
  'permission',
  'scheduled_change',
  'pinnable_release',
];
export const NEW_LINES_REGEX = /\r?\n|\r/g;
export const SPLIT_WITH_NEWLINES_AND_COMMA_REGEX = /[,\r\n]+/;
export const RULES_COMMON_FILTERS = [
  {
    label: 'Firefox Release',
    link: '/rules?product=Firefox&channel=release',
  },
  {
    label: 'Firefox Beta',
    link: '/rules?product=Firefox&channel=beta',
  },
  {
    label: 'Firefox Aurora (DevEdition)',
    link: '/rules?product=Firefox&channel=aurora',
  },
  {
    label: 'Thunderbird Release',
    link: '/rules?product=Thunderbird&channel=release',
  },
  {
    label: 'Thunderbird Beta',
    link: '/rules?product=Thunderbird&channel=beta',
  },
];
export const DIFF_COLORS = {
  ADDED: '#eaffee',
  REMOVED: '#fdeff0',
};
export const INITIAL_JS_DIFF_SUMMARY = { added: 0, removed: 0 };
export const RELEASE_ROOT_LEVEL_KEY = '.';
