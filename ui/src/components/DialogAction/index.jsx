import CircularProgress from '@material-ui/core/CircularProgress';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { makeStyles } from '@material-ui/styles';
import { bool, func, node, object, oneOfType, string } from 'prop-types';
import React, { useEffect, useRef, useState } from 'react';
import tryCatch from '../../utils/tryCatch';
import Button from '../Button';
import ErrorPanel from '../ErrorPanel';

const useStyles = makeStyles((theme) => ({
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
  const classes = useStyles();
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
      onExited={(...props) => onExited?.(...props)}
      onClose={onClose}
      {...rest}
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

DialogAction.propTypes = {
  /** If true, the Dialog is open. */
  open: bool.isRequired,
  /** The title of the Dialog. */
  title: string,
  /** The body of the Dialog. */
  body: node,
  /** The text content of the executing action button */
  confirmText: string.isRequired,
  /** Callback fired when the executing action button is clicked */
  onSubmit: func.isRequired,
  /**
   * Callback fired when the action is complete with
   * the return value of onSubmit. This function will not
   * be called if onSubmit throws an error.
   * */
  onComplete: func,
  /** Callback fired when onSubmit throws an error.
   * The error will be provided in the callback. */
  onError: func,
  /** Callback fired when the component requests to be closed. */
  onClose: func.isRequired,
  onExited: func,
  /** Error to display. */
  error: oneOfType([string, object]),
  /**
   * If true, the action is considered destructive (e.g., delete)
   * and will have the confirmation button filled with red
   */
  destructive: bool,
};

DialogAction.defaultProps = {
  title: '',
  body: '',
  onComplete: null,
  onError: null,
  error: null,
  destructive: false,
};

export default DialogAction;
