import React, { Fragment } from 'react';
import { makeStyles } from '@material-ui/styles';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import ArrowRightIcon from 'mdi-react/ArrowRightIcon';
import StatusLabel from '../StatusLabel';
import { signoffEntry } from '../../utils/prop-types';
import { LABELS } from '../../utils/constants';
import { withUser } from '../../utils/AuthContext';

const useStyles = makeStyles(theme => ({
  diff: {
    display: 'flex',
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
  listSubheader: {
    lineHeight: 1.5,
    marginBottom: theme.spacing(1),
  },
  listWrapper: {
    display: 'flex',
  },
  requiresSignoffsList: {
    marginRight: theme.spacing(6),
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
  const { user, entry, name } = props;
  const status = getStatus(entry);
  const isScheduled = 'sc' in entry;
  const signoffsRequiredCurrent = Number(entry.signoffs_required);
  const signoffsRequiredIntent =
    isScheduled && Number(entry.sc.signoffs_required);
  const listOfSignoffs = isScheduled && Object.entries(entry.sc.signoffs);

  return (
    <Fragment>
      <CardContent>
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4} className={classes.firstColumn}>
            <div className={classes.diff}>
              <Typography>
                {signoffsRequiredCurrent} member
                {signoffsRequiredCurrent > 1 ? 's' : ''} of {name}
              </Typography>
              {isScheduled && (
                <Fragment>
                  <ArrowRightIcon className={classes.arrowIcon} />
                  <Typography>{signoffsRequiredIntent}</Typography>
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
              <div className={classes.listWrapper}>
                <List
                  dense
                  subheader={
                    <ListSubheader className={classes.listSubheader}>
                      Requires Signoffs From
                    </ListSubheader>
                  }>
                  {Object.entries(entry.sc.required_signoffs).map(
                    ([role, count], index) => {
                      const key = `${role}-${index}`;

                      return (
                        <ListItem
                          key={key}
                          dense
                          className={classes.requiresSignoffsList}>
                          <ListItemText
                            primary={`${count} member${
                              count > 1 ? 's' : ''
                            } of ${role}`}
                          />
                        </ListItem>
                      );
                    }
                  )}
                </List>
                {listOfSignoffs && Boolean(listOfSignoffs.length) && (
                  <List
                    dense
                    subheader={
                      <ListSubheader className={classes.listSubheader}>
                        Signed By
                      </ListSubheader>
                    }>
                    <ListItem dense>
                      {listOfSignoffs.map(([username, signoffRole]) => (
                        <ListItemText
                          key={username}
                          primary={
                            <Fragment>
                              {username}
                              {' - '}
                              <Typography
                                color="textSecondary"
                                variant="caption">
                                {signoffRole}
                              </Typography>
                            </Fragment>
                          }
                        />
                      ))}
                    </ListItem>
                  </List>
                )}
              </div>
            )}
          </Grid>
        </Grid>
      </CardContent>
      {isScheduled && (
        <CardActions className={classes.cardActions}>
          {isScheduled && entry.sc.change_type === 'delete' && (
            <Button color="secondary">Cancel Delete</Button>
          )}
          {user && user.email in entry.sc.signoffs ? (
            <Button color="secondary">Revoke Signoff</Button>
          ) : (
            <Button color="secondary">Signoff as</Button>
          )}
        </CardActions>
      )}
    </Fragment>
  );
}

SignoffCardEntry.propTypes = {
  entry: signoffEntry.isRequired,
};

export default withUser(SignoffCardEntry);
