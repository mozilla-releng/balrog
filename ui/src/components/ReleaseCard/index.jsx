import React, { Fragment } from 'react';
import { stringify } from 'qs';
import { func } from 'prop-types';
import { formatDistanceStrict } from 'date-fns';
import { makeStyles } from '@material-ui/styles';
import Card from '@material-ui/core/Card';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import CardHeader from '@material-ui/core/CardHeader';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Chip from '@material-ui/core/Chip';
import UpdateIcon from 'mdi-react/UpdateIcon';
import Grid from '@material-ui/core/Grid';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import IconButton from '@material-ui/core/IconButton';
import Tooltip from '@material-ui/core/Tooltip';
import Divider from '@material-ui/core/Divider';
import HistoryIcon from 'mdi-react/HistoryIcon';
import LinkIcon from 'mdi-react/LinkIcon';
import Button from '../Button';
import SignoffSummary from '../SignoffSummary';
import { withUser } from '../../utils/AuthContext';
import Link from '../../utils/Link';
import { release } from '../../utils/prop-types';
import highlightMatchedRelease from '../../utils/highlightMatchedRelease';

const useStyles = makeStyles(theme => ({
  root: {
    '& h2': {
      '& .anchor-link-style': {
        textDecoration: 'none',
        opacity: 0,
        // To prevent the link to get the focus.
        display: 'none',
      },
      '&:hover .anchor-link-style': {
        display: 'inline-block',
        opacity: 1,
        color: theme.palette.text.hint,
        '&:hover': {
          color: theme.palette.text.secondary,
        },
      },
    },
  },
  cardHeader: {
    paddingBottom: 0,
  },
  cardHeaderContent: {
    ...theme.mixins.textEllipsis,
  },
  releaseName: {
    ...theme.mixins.textEllipsis,
  },
  listItem: {
    paddingTop: 0,
    paddingBottom: 0,
  },
  cardContentRoot: {
    padding: theme.spacing(0, 1),
  },
  cardContentChip: {
    paddingLeft: theme.spacing(4),
    paddingRight: theme.spacing(4),
  },
  chip: {
    cursor: 'pointer',
    marginRight: theme.spacing(1),
    marginBottom: theme.spacing(1),
  },
  badge: {
    padding: theme.spacing(0, 2, 0, 0),
  },
  cardActions: {
    justifyContent: 'flex-end',
  },
  switchLabel: {
    marginLeft: theme.spacing(0.5),
  },
  formControlLabelSwitch: {
    marginLeft: 0,
  },
  cardHeaderActions: {
    display: 'flex',
    alignItems: 'center',
  },
  switchPaper: {
    display: 'flex',
    height: theme.spacing(4),
    marginRight: theme.spacing(1),
  },
  link: {
    ...theme.mixins.link,
  },
  divider: {
    margin: `${theme.spacing(1)}px`,
  },
  scheduledChangesContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  scheduledChangesContent: {
    display: 'flex',
    alignItems: 'baseline',
  },
  scheduledChangesTitle: {
    padding: `0 ${theme.spacing(1)}px`,
  },
  changeTimeChip: {
    height: theme.spacing(3),
  },
  changeTimeChipIcon: {
    marginLeft: theme.spacing(1),
    marginBottom: 1,
  },
  space: {
    paddingTop: theme.spacing(2),
  },
}));

function ReleaseCard(props) {
  const {
    release,
    user,
    onSignoff,
    onRevoke,
    onAccessChange,
    onReleaseDelete,
    onViewScheduledChangeDiff,
    // We don't actually use these, but we need to avoid passing them onto
    // `Card` like the rest of the props.
    onAuthorize: _,
    onUnauthorize: __,
    ...rest
  } = props;
  const classes = useStyles();
  const hasRulesPointingAtRevision = Object.keys(release.rule_info).length > 0;
  const hasScheduledChange =
    release.scheduledChange && Object.keys(release.scheduledChange).length > 0;
  const requiredSignoffs = release.required_signoffs
    ? release.required_signoffs
    : release.scheduledChange && release.scheduledChange.required_signoffs;
  const requiresSignoff = Object.keys(requiredSignoffs).length > 0;
  const handleAccessChange = ({ target: { checked } }) => {
    onAccessChange({ release, checked });
  };

  const updatingToModifiable = release =>
    release.scheduledChange &&
    !release.scheduledChange.read_only &&
    release.read_only;
  const getRuleLink = (ruleId, product, channel) => {
    const args = { product };

    if (channel) {
      args.channel = channel.replace(/[-*]*$/, '');
    }

    const qs = stringify(args, { addQueryPrefix: true });

    return `/rules${qs}#ruleId=${ruleId}`;
  };

  return (
    <Card classes={{ root: classes.root }} {...rest}>
      <CardHeader
        className={classes.cardHeader}
        classes={{ content: classes.cardHeaderContent }}
        title={
          <Typography
            className={classes.releaseName}
            component="h2"
            variant="h6">
            {rest.releaseHighlight
              ? highlightMatchedRelease(rest.releaseHighlight,release.name)
              : release.name}{' '}
            <a
              href={`#${release.name}`}
              aria-label="Anchor"
              className="anchor-link-style">
              #
            </a>
          </Typography>
        }
        subheader={release.product}
        action={
          <div className={classes.cardHeaderActions}>
            <Paper className={classes.switchPaper}>
              <FormControlLabel
                className={classes.formControlLabelSwitch}
                control={
                  <Switch
                    checked={release.read_only}
                    onChange={handleAccessChange}
                  />
                }
                label={
                  <Typography className={classes.switchLabel} variant="body2">
                    Read only
                  </Typography>
                }
              />
            </Paper>
            <Link
              className={classes.link}
              to={
                release.api_version === 1
                  ? `/releases/${release.name}/revisions`
                  : `/releases/${release.name}/revisions/v2`
              }>
              <Tooltip title="Revisions">
                <IconButton>
                  <HistoryIcon />
                </IconButton>
              </Tooltip>
            </Link>
          </div>
        }
      />
      <CardContent classes={{ root: classes.cardContentRoot }}>
        <List>
          <Grid container>
            {release.api_version === 1 && (
              <Grid item xs={12}>
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="Data Version"
                    secondary={release.data_version}
                  />
                </ListItem>
              </Grid>
            )}
            <Grid item>
              <ListItem className={classes.listItem}>
                <ListItemText
                  primary="Used By"
                  secondaryTypographyProps={{ component: 'div' }}
                  secondary={
                    hasRulesPointingAtRevision ? (
                      Object.entries(release.rule_info).map(
                        ([ruleId, ruleInfo]) => (
                          <Link
                            className={classes.link}
                            key={ruleId}
                            to={getRuleLink(
                              ruleId,
                              ruleInfo.product,
                              ruleInfo.channel
                            )}>
                            <Chip
                              clickable
                              size="small"
                              icon={<LinkIcon />}
                              label={ruleId}
                              className={classes.chip}
                            />
                          </Link>
                        )
                      )
                    ) : (
                      <em>n/a</em>
                    )
                  }
                />
              </ListItem>
            </Grid>
          </Grid>
        </List>
        {release.scheduledChange && (
          <Fragment>
            <Divider className={classes.divider} />
            <div className={classes.scheduledChangesContainer}>
              <div className={classes.scheduledChangesContent}>
                <Typography
                  className={classes.scheduledChangesTitle}
                  component="h4"
                  variant="subtitle1">
                  Scheduled Changes
                </Typography>
                {updatingToModifiable(release) ? (
                  <small>
                    <i>Changing release state to modifiable</i>
                  </small>
                ) : (
                  <Button
                    color="secondary"
                    onClick={() => onViewScheduledChangeDiff(release)}>
                    View Diff
                  </Button>
                )}
              </div>
              <Chip
                className={classes.changeTimeChip}
                icon={
                  <UpdateIcon
                    className={classes.changeTimeChipIcon}
                    size={16}
                  />
                }
                label={`${formatDistanceStrict(
                  release.scheduledChange.when,
                  new Date(),
                  { addSuffix: true }
                )} (${release.scheduledChange.change_type})`}
              />
            </div>
          </Fragment>
        )}
        {hasScheduledChange && requiresSignoff && (
          <SignoffSummary
            requiredSignoffs={requiredSignoffs}
            signoffs={release.scheduledChange.signoffs}
            className={classes.space}
          />
        )}
      </CardContent>
      <CardActions className={classes.cardActions}>
        <Link
          className={classes.link}
          to={
            release.api_version === 1
              ? `/releases/${release.name}`
              : `/releases/${release.name}/v2`
          }>
          <Button color="secondary">
            {release.read_only ? 'View' : 'Update'}
          </Button>
        </Link>
        <Button
          disabled={release.read_only || hasRulesPointingAtRevision}
          color="secondary"
          onClick={() => onReleaseDelete(release)}>
          Delete
        </Button>
        {hasScheduledChange &&
          requiresSignoff &&
          (user && user.email in release.scheduledChange.signoffs ? (
            <Button color="secondary" disabled={!user} onClick={onRevoke}>
              Revoke Signoff
            </Button>
          ) : (
            <Button color="secondary" disabled={!user} onClick={onSignoff}>
              Signoff
            </Button>
          ))}
      </CardActions>
    </Card>
  );
}

ReleaseCard.propTypes = {
  release: release.isRequired,
  onViewScheduledChangeDiff: func.isRequired,
  onAccessChange: func, // Required if readOnly is false
  onSignoff: func, // Required if readOnly is false
  onRevoke: func, // Required if readOnly is false
};

export default withUser(ReleaseCard);
