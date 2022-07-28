import React from 'react';
import { func, object } from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Typography from '@material-ui/core/Typography';
import AlertIcon from 'mdi-react/AlertIcon';
import Button from '../Button';
import SignoffSummary from '../SignoffSummary';
import { withUser } from '../../utils/AuthContext';

const useStyles = makeStyles(theme => ({
  root: {
    border: `2px solid ${theme.palette.warning.dark}`,
  },
  space: {
    paddingTop: theme.spacing(2),
  },
  cardHeader: {
    backgroundColor: theme.palette.warning.main,
  },
  cardHeaderAvatar: {
    display: 'flex',
  },
  cardContentRoot: {
    padding: theme.spacing(1),
  },
  cardActions: {
    justifyContent: 'flex-end',
  },
  reason: {
    alignSelf: 'center',
    width: '100%',
    color: theme.palette.text.secondary,
  },
  actionButton: {
    minWidth: 'max-content',
  },
}));

function EmergencyShutoffCard({
  emergencyShutoff,
  onEnableUpdates,
  onCancelEnable,
  onSignoff,
  onRevoke,
  user,
  onAuthorize,
  onUnauthorize,
  ...props
}) {
  const classes = useStyles();
  const { product, channel } = emergencyShutoff;
  const requiresSignoff =
    emergencyShutoff.scheduledChange &&
    Object.keys(emergencyShutoff.scheduledChange.required_signoffs).length > 0;

  return (
    <Card classes={{ root: classes.root }} spacing={4} {...props}>
      <CardHeader
        classes={{ avatar: classes.cardHeaderAvatar }}
        className={classes.cardHeader}
        avatar={<AlertIcon />}
        title={
          <Typography component="h2" variant="h6">
            {emergencyShutoff.scheduledChange
              ? `Updates are scheduled to be enabled for the ${product} ${channel} channel`
              : `Updates are currently disabled for the ${product} ${channel} channel`}
          </Typography>
        }
      />
      <CardContent classes={{ root: classes.cardContentRoot }}>
        {requiresSignoff && (
          <SignoffSummary
            requiredSignoffs={
              emergencyShutoff.scheduledChange.required_signoffs
            }
            signoffs={emergencyShutoff.scheduledChange.signoffs}
            className={classes.space}
          />
        )}
      </CardContent>
      <CardActions className={classes.cardActions}>
        {emergencyShutoff.comment && (
          <Typography component="p" className={classes.reason}>
            Reason: {emergencyShutoff.comment}
          </Typography>
        )}

        {emergencyShutoff.scheduledChange ? (
          <Button
            className={classes.actionButton}
            color="secondary"
            disabled={!user}
            onClick={() => onCancelEnable(emergencyShutoff)}>
            Keep Updates Disabled
          </Button>
        ) : (
          <Button
            className={classes.actionButton}
            color="secondary"
            disabled={!user}
            onClick={() => onEnableUpdates(emergencyShutoff)}>
            Enable Updates
          </Button>
        )}
        {requiresSignoff &&
          (user && user.email in emergencyShutoff.scheduledChange.signoffs ? (
            <Button
              color="secondary"
              disabled={!user}
              onClick={onRevoke}
              className={classes.actionButton}>
              Revoke Signoff
            </Button>
          ) : (
            <Button
              color="secondary"
              disabled={!user}
              onClick={onSignoff}
              className={classes.actionButton}>
              Signoff
            </Button>
          ))}
      </CardActions>
    </Card>
  );
}

EmergencyShutoffCard.propTypes = {
  emergencyShutoff: object,
  onSignoff: func.isRequired,
  onRevoke: func.isRequired,
};

export default withUser(EmergencyShutoffCard);
