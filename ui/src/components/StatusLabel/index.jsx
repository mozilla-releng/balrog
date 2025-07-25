import Label from '@mozilla-frontend-infra/components/Label';
import { sentenceCase } from 'change-case';
import { bool, string } from 'prop-types';
import React from 'react';
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
      {...rest}
    >
      {sentenceCase(state).toUpperCase() || 'UNKNOWN'}
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
