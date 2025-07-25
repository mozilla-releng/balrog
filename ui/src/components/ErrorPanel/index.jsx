import { makeStyles } from '@material-ui/styles';
import MuiErrorPanel from '@mozilla-frontend-infra/components/ErrorPanel';
import classNames from 'classnames';
import { bool, func, object, oneOfType, string } from 'prop-types';
import React, { useState } from 'react';
import { CONTENT_MAX_WIDTH } from '../../utils/constants';

const useStyles = makeStyles((theme) => ({
  fixed: {
    position: 'fixed',
    zIndex: theme.zIndex.snackbar,
    left: '50%',
    right: '50%',
    transform: 'translateX(-50%)',
    width: '92%',
    maxWidth: CONTENT_MAX_WIDTH,
  },
}));

export default function ErrorPanel({
  onClose,
  className,
  error,
  fixed,
  ...props
}) {
  const classes = useStyles();
  const [currentError, setCurrentError] = useState(null);
  const [previousError, setPreviousError] = useState(null);
  const handleErrorClose = () => {
    setCurrentError(null);

    if (onClose) {
      onClose();
    }
  };

  if (error !== previousError) {
    setCurrentError(error);
    setPreviousError(error);
  }

  return currentError ? (
    <MuiErrorPanel
      className={classNames(className, {
        [classes.fixed]: fixed,
      })}
      error={currentError}
      onClose={handleErrorClose}
      {...props}
    />
  ) : null;
}

ErrorPanel.propTypes = {
  /** Error to display. */
  error: oneOfType([string, object]),
  /** If true, the component will be fixed. */
  fixed: bool,
  className: string,
  onClose: func,
};

ErrorPanel.defaultProps = {
  className: null,
  error: null,
  fixed: false,
  onClose: null,
};
