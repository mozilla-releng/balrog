import React, { Fragment } from 'react';
import { makeStyles } from '@material-ui/styles';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import ArrowRightIcon from 'mdi-react/ArrowRightIcon';
import { func } from 'prop-types';
import StatusLabel from '../StatusLabel';
import Button from '../Button';
import SignoffSummary from '../SignoffSummary';
import { signoffEntry } from '../../utils/prop-types';
import { LABELS } from '../../utils/constants';
import { withUser } from '../../utils/AuthContext';

const useStyles = makeStyles(theme => ({
  diff: {
    display: 'flex',
    alignItems: 'center',
  },
  cardActions: {
    justifyContent: 'flex-end',
  },
  ul: {
    marginTop: 0,
  },
  arrowIcon: {
    margin: `0 ${theme.spacing(1)}px`,
  },
  firstColumn: {
    display: 'flex',
    flexDirection: 'column',
  },
  secondColumn: {
    display: 'flex',
  },
  statusLabel: {
    marginTop: theme.spacing(1),
  },
}));

function getStatus(entry) {
  if (!('sc' in entry)) {
    return null;
  }

  if (entry.sc.change_type !== 'delete') {
    return LABELS.PENDING;
  }

  if (entry.sc.change_type === 'delete') {
    return LABELS.PENDING_DELETE;
  }
}

function SignoffCardEntry(props) {
  const classes = useStyles();
  const { user, entry, name, onCancelDelete, onSignoff, onRevoke } = props;
  const status = getStatus(entry);
  const isScheduled = 'sc' in entry;
  const signoffsRequiredCurrent = Number(entry.signoffs_required);
  const signoffsRequiredIntent =
    isScheduled && Number(entry.sc.signoffs_required);

  return (
    <Fragment>
      <CardContent>
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4} className={classes.firstColumn}>
            <div className={classes.diff}>
              <Typography variant="body2">
                <em>
                  {signoffsRequiredCurrent} member
                  {signoffsRequiredCurrent > 1 ? 's' : ''} of {name}
                </em>
              </Typography>
              {isScheduled && (
                <Fragment>
                  <ArrowRightIcon className={classes.arrowIcon} />
                  <Typography variant="body2">
                    <em>{signoffsRequiredIntent}</em>
                  </Typography>
                </Fragment>
              )}
            </div>
            {status && (
              <div className={classes.statusLabel}>
                <StatusLabel state={status} />
              </div>
            )}
          </Grid>
          <Grid item xs={12} sm={8} className={classes.secondColumn}>
            {isScheduled && (
              <SignoffSummary
                requiredSignoffs={entry.sc.required_signoffs}
                signoffs={entry.sc.signoffs}
              />
            )}
          </Grid>
        </Grid>
      </CardContent>
      {isScheduled && (
        <CardActions className={classes.cardActions}>
          {isScheduled && entry.sc.change_type === 'delete' && (
            <Button color="secondary" onClick={onCancelDelete}>
              Cancel Delete
            </Button>
          )}
          {user && user.email in entry.sc.signoffs ? (
            <Button color="secondary" onClick={onRevoke}>
              Revoke Signoff
            </Button>
          ) : (
            <Button color="secondary" onClick={onSignoff}>
              Signoff
            </Button>
          )}
        </CardActions>
      )}
    </Fragment>
  );
}

SignoffCardEntry.propTypes = {
  entry: signoffEntry.isRequired,
  onCancelDelete: func.isRequired,
  onSignoff: func.isRequired,
  onRevoke: func.isRequired,
};

export default withUser(SignoffCardEntry);
