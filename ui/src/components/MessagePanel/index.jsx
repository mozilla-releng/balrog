import IconButton from '@material-ui/core/IconButton';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/styles';
import AlertIcon from 'mdi-react/AlertIcon';
import CloseIcon from 'mdi-react/CloseIcon';
import InformationIcon from 'mdi-react/InformationIcon';
import { bool, oneOf, string } from 'prop-types';
import React, { useState } from 'react';

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: `${theme.spacing(0)}px ${theme.spacing(2)}px`,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    minHeight: theme.spacing(6),
  },
  warning: {
    backgroundColor: theme.palette.warning.dark,
    color: theme.palette.warning.contrastText,
    '& .mdi-icon': {
      fill: theme.palette.warning.contrastText,
    },
  },
  info: {
    backgroundColor: theme.palette.info.main,
    color: theme.palette.info.contrastText,
    '& .mdi-icon': {
      fill: theme.palette.info.contrastText,
    },
  },
  closeIconDiv: {},
  variantIconDiv: {
    display: 'flex',
    marginRight: theme.spacing(1),
  },
  messageDiv: {
    flex: 1,
  },
  message: {
    padding: `${theme.spacing(1)}px 0`,
  },
}));

function MessagePanel(props) {
  const classes = useStyles();
  const { variant, message, alwaysOpen } = props;
  const [display, setDisplay] = useState(true);
  const variantIcon = {
    warning: AlertIcon,
    info: InformationIcon,
  };
  const Icon = variantIcon[variant];
  const handleClose = () => {
    setDisplay(false);
  };

  if (!display) {
    return null;
  }

  return (
    <Paper classes={{ root: classes.paper }} className={classes[variant]}>
      <div className={classes.variantIconDiv}>
        <Icon />
      </div>
      <div className={classes.messageDiv}>
        <Typography className={classes.message}>{message}</Typography>
      </div>
      {!alwaysOpen && (
        <div className={classes.closeIconDiv}>
          <IconButton onClick={handleClose}>
            <CloseIcon />
          </IconButton>
        </div>
      )}
    </Paper>
  );
}

MessagePanel.propTypes = {
  message: string.isRequired,
  variant: oneOf(['info', 'warning']),
  /**
   * If true, the message panel will not have a close icon option to close
   * the panel
   */
  alwaysOpen: bool,
};

MessagePanel.defaultProps = {
  variant: 'info',
  alwaysOpen: false,
};

export default MessagePanel;
