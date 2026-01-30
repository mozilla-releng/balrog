import Button from '@mui/material/Button';
import { sentenceCase } from 'change-case';
import React from 'react';
import { makeStyles } from 'tss-react/mui';
import labels from '../../utils/labels';

const useStyles = makeStyles()((theme) => ({
  mini: {
    fontSize: '0.7em',
    padding: '3px 8px 2px',
  },
  error: {
    backgroundColor: `${theme.palette.error.dark} !important`,
    color: `${theme.palette.error.contrastText} !important`,
  },
  success: {
    backgroundColor: `${theme.palette.success.dark} !important`,
    color: `${theme.palette.success.contrastText} !important`,
  },
  warning: {
    backgroundColor: `${theme.palette.warning.dark} !important`,
    color: `${theme.palette.warning.contrastText} !important`,
  },
  default: {
    backgroundColor: `${theme.palette.grey[700]} !important`,
    color: `${theme.palette.getContrastText(
      theme.palette.grey[700],
    )} !important`,
  },
  info: {
    backgroundColor: `${theme.palette.info[700]} !important`,
    color: `${theme.palette.info.contrastText} !important`,
  },
}));
/**
 * A label color-coded based on known statuses.
 */
function StatusLabel({ state }) {
  const { classes } = useStyles();
  const labelKey = labels[state] || 'default';

  return (
    <Button
      size="small"
      disabled
      className={`${classes[labelKey]} ${classes.mini}`}
    >
      {sentenceCase(state).toUpperCase() || 'UNKNOWN'}
    </Button>
  );
}

export default StatusLabel;
