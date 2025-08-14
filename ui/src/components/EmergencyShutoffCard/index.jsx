import { withAuth0 } from '@auth0/auth0-react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Typography from '@mui/material/Typography';
import AlertIcon from 'mdi-react/AlertIcon';
import { func, object } from 'prop-types';
import React from 'react';
import { makeStyles } from 'tss-react/mui';
import Button from '../Button';
import SignoffSummary from '../SignoffSummary';

const useStyles = makeStyles()((theme) => ({
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
  auth0,
  ...props
}) {
  const { classes } = useStyles();
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
            disabled={!auth0.user}
            onClick={() => onCancelEnable(emergencyShutoff)}
          >
            Keep Updates Disabled
          </Button>
        ) : (
          <Button
            className={classes.actionButton}
            color="secondary"
            disabled={!auth0.user}
            onClick={() => onEnableUpdates(emergencyShutoff)}
          >
            Enable Updates
          </Button>
        )}
        {requiresSignoff &&
          (auth0.user &&
          auth0.user.email in emergencyShutoff.scheduledChange.signoffs ? (
            <Button
              color="secondary"
              disabled={!auth0.user}
              onClick={onRevoke}
              className={classes.actionButton}
            >
              Revoke Signoff
            </Button>
          ) : (
            <Button
              color="secondary"
              disabled={!auth0.user}
              onClick={onSignoff}
              className={classes.actionButton}
            >
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

export default withAuth0(EmergencyShutoffCard);
