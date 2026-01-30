import Alert from '@mui/material/Alert';
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

ErrorPanel.defaultProps = {
  error: null,
};
