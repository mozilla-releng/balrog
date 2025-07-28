import Alert from '@material-ui/lab/Alert';
import { string } from 'prop-types';
import React, { useState } from 'react';

export default function ErrorPanel({ error }) {
  const [currentError, setCurrentError] = useState(null);
  const [previousError, setPreviousError] = useState(null);
  const handleErrorClose = () => {
    setCurrentError(null);
  };

  if (error !== previousError) {
    setCurrentError(error);
    setPreviousError(error);
  }

  return currentError ? (
    <Alert severity="error" variant="filled" onClose={handleErrorClose}>
      {currentError instanceof Error ? currentError.message : currentError}
    </Alert>
  ) : null;
}

ErrorPanel.propTypes = {
  /** Error to display. */
  error: string,
};

ErrorPanel.defaultProps = {
  error: null,
};
