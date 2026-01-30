import { withAuth0 } from '@auth0/auth0-react';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import DeleteIcon from '@mui/icons-material/Delete';
import HistoryIcon from '@mui/icons-material/History';
import UpdateIcon from '@mui/icons-material/Update';
import Avatar from '@mui/material/Avatar';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Chip from '@mui/material/Chip';
import ClickAwayListener from '@mui/material/ClickAwayListener';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/GridLegacy';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import classNames from 'classnames';
import { formatDistanceStrict } from 'date-fns';
import React, { Fragment, useState } from 'react';
import { makeStyles } from 'tss-react/mui';
import { RULE_DIFF_PROPERTIES } from '../../utils/constants';
import getDiffedProperties from '../../utils/getDiffedProperties';
import getIndexOfSubStr from '../../utils/getIndexOfSubStr';
import Link from '../../utils/Link';
import Button from '../Button';
import DiffRule from '../DiffRule';
import SignoffSummary from '../SignoffSummary';

const useStyles = makeStyles()((theme) => ({
  root: {
    '& h2, & h4': {
      '& .anchor-link-style': {
        textDecoration: 'none',
        opacity: 0,
        // To prevent the link to get the focus.
        display: 'none',
      },
      '&:hover .anchor-link-style': {
        display: 'inline-block',
        opacity: 1,
        color: theme.palette.text.disabled,
        '&:hover': {
          color: theme.palette.text.secondary,
        },
      },
    },
  },
  space: {
    paddingTop: theme.spacing(2),
  },
  cardHeader: {
    paddingBottom: 0,
    paddingTop: theme.spacing(1),
  },
  cardHeaderAvatar: {
    display: 'flex',
  },
  cardHeaderAction: {
    marginTop: 0,
  },
  cardContentRoot: {
    padding: theme.spacing(1),
  },
  noDiffedPropertiesText: {
    padding: `0 ${theme.spacing(1)}`,
  },
  listItem: {
    paddingTop: 0,
    paddingBottom: 0,
  },
  textEllipsis: {
    ...theme.mixins.textEllipsis,
  },
  cardActions: {
    justifyContent: 'flex-end',
  },
  changesTitle: {
    padding: `0 ${theme.spacing(1)}`,
  },
  diff: {
    fontSize: theme.typography.body2.fontSize,
    marginTop: theme.spacing(1),
  },
  chip: {
    height: theme.spacing(3),
  },
  chipIcon: {
    marginLeft: theme.spacing(1),
    marginBottom: 1,
  },
  deleteChip: {
    background: theme.palette.error.main,
    color: theme.palette.error.contrastText,
    '& svg': {
      fill: theme.palette.error.contrastText,
    },
  },
  divider: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.grey[200],
  },
  changesHeader: {
    display: 'flex',
    justifyContent: 'space-between',
  },
  inline: {
    display: 'inline',
  },
  avatar: {
    height: theme.spacing(4),
    padding: theme.spacing(1),
    width: 'auto',
    background: 'unset',
    color: theme.palette.text.primary,
    border: `1px solid ${theme.palette.primary.light}`,
  },
  avatarText: {
    fontSize: theme.typography.body2.fontSize,
  },
  propertyWithChange: {
    ...theme.mixins.redDot,
  },
  priorityScheduledChange: {
    marginLeft: -10,
    zIndex: 1,
  },
  primaryText: {
    display: 'flex',
    alignItems: 'baseline',
  },
  primaryTextWithButton: {
    whiteSpace: 'nowrap',
  },
  link: {
    ...theme.mixins.link,
  },
  schedPriorityChange: {
    backgroundColor: '#c0dc91',
  },
  viewReleaseBtn: {
    paddingTop: 0,
    paddingBottom: 0,
    marginLeft: theme.spacing(1),
  },
}));

function RuleCard({
  rule,
  currentRule,
  rulesFilter,
  onRuleDelete,
  canSignoff,
  onSignoff,
  onRevoke,
  onViewReleaseClick,
  auth0,
  readOnly,
  actionLoading,
  disableActions,
  diffRules,
  ...props
}) {
  const [open, setOpen] = useState(false);
  const [seeMore, setSeeMore] = useState('...see more');
  const { classes } = useStyles();
  const requiresSignoff =
    rule.scheduledChange &&
    Object.keys(rule.scheduledChange.required_signoffs).length > 0;
  const getChipIcon = (changeType) => {
    switch (changeType) {
      case 'delete': {
        return DeleteIcon;
      }

      case 'update': {
        return UpdateIcon;
      }

      case 'insert': {
        return AddCircleIcon;
      }

      default: {
        return AddCircleIcon;
      }
    }
  };

  const ChipIcon = getChipIcon(rule.scheduledChange?.change_type);
  const diffCause = currentRule || rule.scheduledChange;
  const diffedProperties =
    rule && diffCause
      ? getDiffedProperties(RULE_DIFF_PROPERTIES, rule, diffCause)
      : [];
  const markChangedProperties =
    (diffRules && currentRule) ||
    (rule.scheduledChange && rule.scheduledChange.change_type === 'update');
  // If there's a scheduled change that may be updating the priority, we want
  // to display it in the header rather than the current priority.
  // For other types of scheduled changes (inserts and deletes) we either
  // don't show it at all, or don't have a value in the scheduled change to
  // show.
  const isScheduledPriorityUpdate =
    rule.scheduledChange &&
    rule.scheduledChange.change_type === 'update' &&
    rule.priority !== rule.scheduledChange.priority;
  const headerPriority = isScheduledPriorityUpdate
    ? rule.scheduledChange.priority
    : rule.priority;
  const priorityTitle = isScheduledPriorityUpdate
    ? 'Scheduled Priority'
    : 'Priority';
  const handleTooltipOpen = () => {
    setOpen(true);
    setSeeMore('...see less');
  };

  const handleTooltipClose = () => {
    setOpen(false);
    setSeeMore('...see more');
  };

  const splitAmount = 5;
  const isOsVersionLong = () => {
    if (rule.osVersion) {
      const osVersionsLength = rule.osVersion.split(',').length;

      if (osVersionsLength > splitAmount) {
        return true;
      }

      return false;
    }
  };

  const osVersionLimit = () => {
    const allOsVersions = rule.osVersion;
    const firstIndex = getIndexOfSubStr(allOsVersions, `,`, splitAmount);
    const osVersionP = (
      <p
        style={{
          display: 'flex',
          flexFlow: 'column',
          color: '#ffffff',
          fontSize: '14px',
          lineHeight: '16px',
          margin: '2px 4px',
        }}
      >
        {allOsVersions.split(',').map((item) => (
          <p key={item} style={{ margin: '2px 0' }}>
            {item}
          </p>
        ))}
      </p>
    );

    return (
      <React.Fragment>
        {allOsVersions.substring(0, firstIndex)}
        <ClickAwayListener onClickAway={handleTooltipClose}>
          <Tooltip
            title={osVersionP}
            onClose={handleTooltipClose}
            open={open}
            disableFocusListener
            disableHoverListener
            disableTouchListener
            arrow
          >
            <button
              type="button"
              style={{
                color: 'black',
                backgroundColor: 'transparent',
                border: 'none',
                margin: 0,
                padding: 0,
                display: 'inline-block',
                cursor: 'pointer',
              }}
              onClick={open ? handleTooltipClose : handleTooltipOpen}
            >
              {seeMore}
            </button>
          </Tooltip>
        </ClickAwayListener>
      </React.Fragment>
    );
  };

  return (
    <Card classes={{ root: classes.root }} spacing={4} {...props}>
      {rule.product && (
        <CardHeader
          classes={{
            avatar: classes.cardHeaderAvatar,
            action: classes.cardHeaderAction,
          }}
          className={classes.cardHeader}
          avatar={
            Number.isInteger(Number(headerPriority)) && (
              <Fragment>
                <Avatar
                  title={priorityTitle}
                  aria-label={priorityTitle}
                  className={classNames(classes.avatar, {
                    [classes.schedPriorityChange]: isScheduledPriorityUpdate,
                  })}
                >
                  <Typography className={classes.avatarText}>
                    {headerPriority}
                  </Typography>
                </Avatar>
              </Fragment>
            )
          }
          title={
            <Typography component="h2" variant="h6">
              {rule.channel
                ? `${rule.product} : ${rule.channel}`
                : rule.product}{' '}
              <a
                href={`#ruleId=${rule.rule_id}`}
                aria-label="Anchor"
                className="anchor-link-style"
              >
                #
              </a>
            </Typography>
          }
          action={
            !readOnly ? (
              <Link
                to={`/rules/${rule.rule_id}/revisions`}
                state={{ rulesFilter }}
              >
                <Tooltip title="Revisions">
                  <IconButton size="large">
                    <HistoryIcon />
                  </IconButton>
                </Tooltip>
              </Link>
            ) : null
          }
        />
      )}
      <CardContent classes={{ root: classes.cardContentRoot }}>
        {(!rule.scheduledChange ||
          rule.scheduledChange.change_type !== 'insert') && (
          <Grid container>
            <Grid item xs={4}>
              <List>
                {rule.mapping && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      title={rule.mapping}
                      primaryTypographyProps={{
                        component: 'div',
                        className: classNames(
                          classes.primaryText,
                          classes.primaryTextWithButton,
                        ),
                      }}
                      secondaryTypographyProps={{
                        className: classes.textEllipsis,
                      }}
                      primary={
                        <Fragment>
                          Mapping
                          {diffedProperties.includes('mapping') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                          {!readOnly && (
                            <Button
                              size="small"
                              disabled={actionLoading}
                              name={rule.mapping}
                              onClick={onViewReleaseClick}
                              variant="outlined"
                              className={classes.viewReleaseBtn}
                            >
                              View Release
                            </Button>
                          )}
                        </Fragment>
                      }
                      secondary={rule.mapping}
                    />
                  </ListItem>
                )}
                {rule.fallbackMapping && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      title={rule.fallbackMapping}
                      primaryTypographyProps={{
                        component: 'div',
                        className: classNames(
                          classes.primaryText,
                          classes.primaryTextWithButton,
                        ),
                      }}
                      secondaryTypographyProps={{
                        className: classes.textEllipsis,
                      }}
                      primary={
                        <Fragment>
                          Fallback Mapping
                          {diffedProperties.includes('fallbackMapping') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                          {!readOnly && (
                            <Button
                              size="small"
                              disabled={actionLoading}
                              name={rule.fallbackMapping}
                              onClick={onViewReleaseClick}
                              variant="outlined"
                              className={classes.viewReleaseBtn}
                            >
                              View Release
                            </Button>
                          )}
                        </Fragment>
                      }
                      secondary={rule.fallbackMapping}
                    />
                  </ListItem>
                )}
                {Number.isInteger(Number(rule.backgroundRate)) && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Background Rate
                          {diffedProperties.includes('backgroundRate') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.backgroundRate}
                    />
                  </ListItem>
                )}
              </List>
            </Grid>
            <Grid item xs={4}>
              <List>
                {rule.data_version && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Data Version
                          {diffedProperties.includes('data_version') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.data_version}
                    />
                  </ListItem>
                )}
                {Number.isInteger(Number(rule.rule_id)) && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primary="Rule ID"
                      secondary={
                        <Fragment>
                          <Typography
                            component="span"
                            variant="body2"
                            className={classes.inline}
                            color="textSecondary"
                          >
                            {rule.rule_id}
                          </Typography>
                          <strong>
                            {rule.alias && ` ${rule.alias} (alias)`}
                          </strong>
                        </Fragment>
                      }
                    />
                  </ListItem>
                )}
              </List>
            </Grid>
            <Grid item xs={4}>
              <List>
                {rule.version && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Version
                          {diffedProperties.includes('version') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.version}
                    />
                  </ListItem>
                )}
                {rule.buildID && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Build ID
                          {diffedProperties.includes('buildID') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.buildID}
                    />
                  </ListItem>
                )}
                {rule.buildTarget && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Build Target
                          {diffedProperties.includes('buildTarget') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.buildTarget}
                    />
                  </ListItem>
                )}
                {rule.locale && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Locale
                          {diffedProperties.includes('locale') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.locale}
                    />
                  </ListItem>
                )}
                {rule.distribution && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Distribution
                          {diffedProperties.includes('distribution') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.distribution}
                    />
                  </ListItem>
                )}
                {rule.distVersion && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Distribution Version
                          {diffedProperties.includes('distVersion') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.distVersion}
                    />
                  </ListItem>
                )}
                {rule.osVersion && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          {`OS Version${
                            rule.osVersion.split(',').length > 1 ? 's' : ''
                          }`}
                          {diffedProperties.includes('osVersion') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={
                        isOsVersionLong() ? osVersionLimit() : rule.osVersion
                      }
                    />
                  </ListItem>
                )}
                {rule.instructionSet && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Instruction Set
                          {diffedProperties.includes('instructionSet') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.instructionSet}
                    />
                  </ListItem>
                )}
                {rule.memory && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Memory
                          {diffedProperties.includes('memory') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.memory}
                    />
                  </ListItem>
                )}
                {rule.mig64 != null && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          64-bit Migration Opt-in
                          {diffedProperties.includes('mig64') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={String(rule.mig64)}
                    />
                  </ListItem>
                )}
                {rule.jaws != null && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Incompatible JAWS Screen Reader
                          {diffedProperties.includes('jaws') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={String(rule.jaws)}
                    />
                  </ListItem>
                )}
                {rule.headerArchitecture && (
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      primary={
                        <Fragment>
                          Header Architecture
                          {diffedProperties.includes('headerArchitecture') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.headerArchitecture}
                    />
                  </ListItem>
                )}
              </List>
            </Grid>
            <Grid item xs={12}>
              {rule.comment && (
                <List>
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      title={rule.comment}
                      primaryTypographyProps={{
                        component: 'div',
                        className: classes.primaryText,
                      }}
                      secondaryTypographyProps={{
                        className: classes.textEllipsis,
                      }}
                      primary={
                        <Fragment>
                          Comment
                          {diffedProperties.includes('comment') &&
                            markChangedProperties && (
                              <span className={classes.propertyWithChange} />
                            )}
                        </Fragment>
                      }
                      secondary={rule.comment}
                    />
                  </ListItem>
                </List>
              )}
            </Grid>
          </Grid>
        )}
        {rule.scheduledChange && (
          <Fragment>
            {rule.scheduledChange.change_type !== 'insert' && (
              <Divider className={classes.divider} />
            )}
            <div className={classes.changesHeader}>
              <Typography
                className={classes.changesTitle}
                component="h4"
                variant="subtitle1"
              >
                Scheduled Changes{' '}
                <a
                  href={`#scId=${rule.scheduledChange.sc_id}`}
                  aria-label="Anchor"
                  className="anchor-link-style"
                >
                  #
                </a>
              </Typography>
              <Chip
                className={classNames(classes.chip, {
                  [classes.deleteChip]:
                    rule.scheduledChange.change_type === 'delete',
                })}
                icon={<ChipIcon className={classes.chipIcon} size={16} />}
                label={`${formatDistanceStrict(
                  rule.scheduledChange.when,
                  new Date(),
                  { addSuffix: true },
                )} (${rule.scheduledChange.change_type})`}
              />
            </div>
            {rule.scheduledChange.change_type === 'delete' ? (
              <Typography
                className={classes.noDiffedPropertiesText}
                variant="body2"
                color="textSecondary"
              >
                All properties will be deleted
              </Typography>
            ) : (
              <DiffRule firstRule={rule} secondRule={rule.scheduledChange} />
            )}
          </Fragment>
        )}
        {!readOnly && requiresSignoff && (
          <SignoffSummary
            requiredSignoffs={rule.scheduledChange.required_signoffs}
            signoffs={rule.scheduledChange.signoffs}
            className={classes.space}
          />
        )}
        {diffRules && (
          <Fragment>
            <Divider className={classes.divider} />
            <div className={classes.changesHeader}>
              <Typography
                className={classes.changesTitle}
                component="h4"
                variant="subtitle1"
              >
                Historical Changes{' '}
              </Typography>
            </div>
            {diffedProperties.length === 0 ? (
              <Typography
                className={classes.noDiffedPropertiesText}
                variant="body2"
                color="textSecondary"
              >
                {currentRule ? 'No changes made yet' : 'Rule was deleted'}
              </Typography>
            ) : (
              <DiffRule firstRule={rule} secondRule={currentRule} />
            )}
          </Fragment>
        )}
      </CardContent>
      {!readOnly && (
        <CardActions className={classes.cardActions}>
          {disableActions ? (
            <Button color="secondary" disabled={disableActions}>
              Duplicate
            </Button>
          ) : (
            <Link
              className={classes.link}
              to={
                rule.rule_id
                  ? `/rules/duplicate/ruleId/${rule.rule_id}`
                  : `/rules/duplicate/scId/${rule.scheduledChange.sc_id}`
              }
              state={{ rulesFilter }}
            >
              <Button color="secondary">Duplicate</Button>
            </Link>
          )}
          {disableActions ? (
            <Button color="secondary" disabled={disableActions}>
              Update
            </Button>
          ) : (
            <Link
              className={classes.link}
              to={
                rule.rule_id
                  ? `/rules/${rule.rule_id}`
                  : `/rules/create/${rule.scheduledChange.sc_id}`
              }
              state={{ rulesFilter }}
            >
              <Button color="secondary">Update</Button>
            </Link>
          )}
          <Button
            color="secondary"
            disabled={disableActions || actionLoading}
            onClick={() => onRuleDelete(rule)}
          >
            Delete
          </Button>
          {requiresSignoff &&
            (auth0.user && auth0.user.email in rule.scheduledChange.signoffs ? (
              <Button
                color="secondary"
                disabled={disableActions || actionLoading}
                onClick={onRevoke}
              >
                Revoke Signoff
              </Button>
            ) : (
              <Button
                color="secondary"
                disabled={disableActions || actionLoading || !canSignoff}
                onClick={onSignoff}
              >
                Signoff
              </Button>
            ))}
        </CardActions>
      )}
    </Card>
  );
}

RuleCard.defaultProps = {
  onRuleDelete: Function.prototype,
  readOnly: false,
  actionLoading: false,
  disableActions: false,
};

export default withAuth0(RuleCard);
