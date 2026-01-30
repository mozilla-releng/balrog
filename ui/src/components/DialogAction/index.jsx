import CircularProgress from '@mui/material/CircularProgress';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import React, { useEffect, useRef, useState } from 'react';
import { makeStyles } from 'tss-react/mui';
import tryCatch from '../../utils/tryCatch';
import Button from '../Button';
import ErrorPanel from '../ErrorPanel';

const useStyles = makeStyles()((theme) => ({
  executingActionWrapper: {
    position: 'relative',
  },
  buttonProgress: {
    position: 'absolute',
    left: '50%',
    top: '50%',
    marginLeft: -theme.spacing(1) * 1.5,
    marginTop: -theme.spacing(1) * 1.5,
  },
  paper: {
    minWidth: theme.spacing(50),
  },
}));

function DialogAction(props) {
  const { classes } = useStyles();
  const [actionExecuting, setActionExecuting] = useState(false);
  const cancelled = useRef(false);
  const {
    open,
    title,
    body,
    confirmText,
    error,
    onClose,
    onExited,
    onSubmit,
    onComplete,
    onError,
    destructive,
    ...rest
  } = props;

  // Set this so we can avoid calling setActionExecuting if the caller
  // decides to do something that unmounts us in onComplete or onError.
  useEffect(() => {
    return () => {
      cancelled.current = true;
    };
  }, []);

  const handleSubmit = async () => {
    if (cancelled.current === false) {
      setActionExecuting(true);
    }

    const [error, result] = await tryCatch(onSubmit());

    if (error) {
      if (onError) {
        onError(error);
      }

      if (cancelled.current === false) {
        setActionExecuting(false);
      }

      return;
    }

    if (onComplete) {
      onComplete(result);
    }

    if (cancelled.current === false) {
      setActionExecuting(false);
    }
  };

  return (
    <Dialog
      classes={{ paper: classes.paper }}
      open={open}
      onClose={onClose}
      {...rest}
      TransitionProps={{
        onExited: (...props) => onExited?.(...props),
      }}
    >
      {title && <DialogTitle>{title}</DialogTitle>}
      <DialogContent>
        {error && (
          <DialogContentText component="div">
            <ErrorPanel error={error} />
          </DialogContentText>
        )}
        {body && <DialogContentText component="div">{body}</DialogContentText>}
      </DialogContent>
      <DialogActions>
        <Button disabled={actionExecuting} onClick={onClose}>
          Cancel
        </Button>
        <div className={classes.executingActionWrapper}>
          <Button
            disabled={actionExecuting}
            onClick={handleSubmit}
            color={destructive ? 'danger' : 'primary'}
            variant="contained"
            autoFocus
          >
            {confirmText}
          </Button>
          {actionExecuting && (
            <CircularProgress size={24} className={classes.buttonProgress} />
          )}
        </div>
      </DialogActions>
    </Dialog>
  );
}

DialogAction.defaultProps = {
  title: '',
  body: '',
  onComplete: null,
  onError: null,
  error: null,
  destructive: false,
};

export default DialogAction;
