// eslint-disable-next-line import/prefer-default-export
export const USER_SESSION = 'react-auth0-session';
export const BASE_URL = `${process.env.BALROG_ROOT_URL}/api`;
export const OBJECT_NAMES = {
  PERMISSIONS_REQUIRED_SIGNOFF: 'required_signoffs/permissions',
  PRODUCT_REQUIRED_SIGNOFF: 'required_signoffs/product',
};
export const LABELS = {
  PENDING: 'pending',
  PENDING_DELETE: 'pendingDelete',
};
export const RULE_DIFF_PROPERTIES = [
  'alias',
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
};
export const EMPTY_MENU_ITEM_CHAR = '-';
