import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CloseIcon from '@mui/icons-material/Close';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import InfoIcon from '@mui/icons-material/Info';
import WarningIcon from '@mui/icons-material/Warning';
import { amber, green } from '@mui/material/colors';
import IconButton from '@mui/material/IconButton';
import MuiSnackbar from '@mui/material/Snackbar';
import SnackbarContent from '@mui/material/SnackbarContent';
import React from 'react';
import { makeStyles } from 'tss-react/mui';
import { SNACKBAR_AUTO_HIDE_DURATION } from '../../utils/constants';

const variantIcon = {
  success: CheckCircleIcon,
  warning: WarningIcon,
  error: ErrorOutlineIcon,
  info: InfoIcon,
};
const useStyles = makeStyles()((theme) => ({
  iconButtonRoot: {
    color: theme.palette.common.white,
  },
  success: {
    backgroundColor: green[600],
  },
  info: {
    backgroundColor: theme.palette.primary.main,
  },
  error: {
    backgroundColor: theme.palette.error.dark,
  },
  warning: {
    backgroundColor: amber[700],
  },
  iconVariant: {
    opacity: 0.9,
    marginRight: theme.spacing(1),
  },
  message: {
    display: 'flex',
    alignItems: 'center',
  },
}));

function Snackbar(props) {
  const { classes } = useStyles();
  const { onClose, variant, message, snackbarContentProps, ...rest } = props;
  const Icon = variantIcon[variant];

  return (
    <MuiSnackbar
      autoHideDuration={SNACKBAR_AUTO_HIDE_DURATION}
      onClose={onClose}
      {...rest}
    >
      <SnackbarContent
        className={classes[variant]}
        action={
          <IconButton
            classes={{ root: classes.iconButtonRoot }}
            aria-label="Close"
            onClick={onClose}
            size="large"
          >
            <CloseIcon />
          </IconButton>
        }
        message={
          <span className={classes.message}>
            <Icon className={classes.iconVariant} />
            {message}
          </span>
        }
        {...snackbarContentProps}
      />
    </MuiSnackbar>
  );
}

Snackbar.defaultProps = {
  variant: 'success',
  snackbarContentProps: null,
};

export default Snackbar;
