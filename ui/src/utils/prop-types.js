import { bool, number, object, oneOfType, shape, string } from 'prop-types';

export const signoffEntry = shape({
  channel: string,
  data_version: number,
  role: string,
  signoffs_required: number,
});

export const rule = shape({
  alias: string,
  backgroundRate: oneOfType([number, string]),
  buildID: string,
  buildTarget: string,
  channel: string,
  comment: string,
  data_version: oneOfType([number, string]),
  distVersion: string,
  distribution: string,
  fallbackMapping: string,
  headerArchitecture: string,
  instructionSet: string,
  jaws: bool,
  locale: string,
  mapping: string,
  memory: string,
  mig64: bool,
  osVersion: string,
  priority: oneOfType([number, string]),
  product: string,
  rule_id: oneOfType([number, string]),
  update_type: string,
  version: string,
});

export const release = shape({
  data_version: number,
  name: string,
  product: string,
  read_only: bool,
  required_signoffs: object,
  rule_info: shape({
    rule_id: shape({
      channel: string,
      product: string,
    }),
  }),
});
