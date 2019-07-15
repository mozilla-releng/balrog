import React from 'react';
import { bool, string } from 'prop-types';
import { upperCase, sentenceCase } from 'change-case';
import Label from '@mozilla-frontend-infra/components/Label';
import labels from '../../utils/labels';

/**
 * A label color-coded based on known statuses.
 */
function StatusLabel(props) {
  const { state, mini, className, ...rest } = props;

  return (
    <Label
      mini={mini}
      status={labels[state] || 'default'}
      className={className}
      {...rest}>
      {upperCase(sentenceCase(state)) || 'UNKNOWN'}
    </Label>
  );
}

StatusLabel.propTypes = {
  /**
   * A state string.
   */
  state: string.isRequired,
  /**
   * Render the label using dense styling.
   */
  mini: bool,
  /** The CSS class name of the wrapper element */
  className: string,
};

StatusLabel.defaultProps = {
  mini: true,
  className: null,
};

export default StatusLabel;
