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
  'build_ID',
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
export const RULES_ROWS_PER_PAGE = 25;
