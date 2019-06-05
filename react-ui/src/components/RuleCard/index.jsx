import React, { Fragment, useState, useEffect } from 'react';
import classNames from 'classnames';
import { makeStyles } from '@material-ui/styles';
import Card from '@material-ui/core/Card';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Avatar from '@material-ui/core/Avatar';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';
import Chip from '@material-ui/core/Chip';
import DeleteIcon from 'mdi-react/DeleteIcon';
import UpdateIcon from 'mdi-react/UpdateIcon';
import PlusCircleIcon from 'mdi-react/PlusCircleIcon';
import HistoryIcon from 'mdi-react/HistoryIcon';
import { diffLines, formatLines } from 'unidiff';
import { parseDiff, Diff, Hunk } from 'react-diff-view';
import { distanceInWordsStrict } from 'date-fns';
import 'react-diff-view/style/index.css';
import { RULE_DIFF_PROPERTIES } from '../../utils/constants';
import { rule } from '../../utils/prop-types';
import getDiff from '../../utils/diff';

const useStyles = makeStyles(theme => ({
  cardHeader: {
    paddingBottom: 0,
  },
  cardContentRoot: {
    padding: theme.spacing(1),
  },
  deletedText: {
    padding: theme.spacing(1),
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
  scheduledChangesTitle: {
    padding: `0 ${theme.spacing(1)}px`,
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
    margin: `${theme.spacing(1)}px`,
  },
  scheduledChangesHeader: {
    display: 'flex',
    justifyContent: 'space-between',
  },
  inline: {
    display: 'inline',
  },
  avatar: {
    height: theme.spacing(4),
    width: theme.spacing(4),
  },
  avatarText: {
    fontSize: 10,
  },
}));

function RuleCard({ rule, ...props }) {
  const classes = useStyles();
  const [{ type, hunks }, setDiff] = useState('');
  const getChipIcon = changeType => {
    switch (changeType) {
      case 'delete': {
        return DeleteIcon;
      }

      case 'update': {
        return UpdateIcon;
      }

      case 'insert': {
        return PlusCircleIcon;
      }

      default: {
        return PlusCircleIcon;
      }
    }
  };

  const ChipIcon = getChipIcon(
    rule.scheduledChange && rule.scheduledChange.change_type
  );

  useEffect(() => {
    if (!rule.scheduledChange) {
      return;
    }

    const [oldText, newText] = getDiff(
      RULE_DIFF_PROPERTIES,
      rule,
      rule.scheduledChange
    );
    const diffText = formatLines(diffLines(oldText, newText), {
      context: 0,
    });
    const [diff] = parseDiff(diffText, { nearbySequences: 'zip' });

    setDiff(diff);
  }, [rule]);

  return (
    <Card spacing={4} {...props}>
      {rule.product && (
        <CardHeader
          className={classes.cardHeader}
          avatar={
            Number.isInteger(Number(rule.priority)) && (
              <Avatar
                title="Priority"
                aria-label="Priority"
                className={classes.avatar}>
                <Typography className={classes.avatarText}>
                  {rule.priority}
                </Typography>
              </Avatar>
            )
          }
          titleTypographyProps={{
            component: 'h2',
            variant: 'h6',
          }}
          title={
            rule.channel ? `${rule.product} : ${rule.channel}` : rule.product
          }
          action={
            <Tooltip title="History">
              <IconButton>
                <HistoryIcon />
              </IconButton>
            </Tooltip>
          }
        />
      )}
      <CardContent classes={{ root: classes.cardContentRoot }}>
        <Grid container>
          <Grid item xs={4}>
            <List>
              {rule.mapping && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    secondaryTypographyProps={{
                      className: classes.textEllipsis,
                    }}
                    primary="Mapping"
                    secondary={rule.mapping}
                  />
                </ListItem>
              )}
              {rule.fallbackMapping && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    secondaryTypographyProps={{
                      className: classes.textEllipsis,
                    }}
                    primary="Fallback Mapping"
                    secondary={rule.fallbackMapping}
                  />
                </ListItem>
              )}
              {Number.isInteger(Number(rule.backgroundRate)) && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="Background Rate"
                    secondary={rule.backgroundRate}
                  />
                </ListItem>
              )}
              {rule.comment && (
                <List>
                  <ListItem className={classes.listItem}>
                    <ListItemText
                      primary="Comment"
                      secondary={rule.comment}
                      secondaryTypographyProps={{
                        className: classes.textEllipsis,
                      }}
                    />
                  </ListItem>
                </List>
              )}
            </List>
          </Grid>
          <Grid item xs={4}>
            <List>
              {rule.data_version && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="Data Version"
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
                          color="textPrimary">
                          {rule.rule_id}
                        </Typography>
                        {rule.alias && ` ${rule.alias} (alias)`}
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
                  <ListItemText primary="Version" secondary={rule.version} />
                </ListItem>
              )}
              {rule.buildID && (
                <ListItem className={classes.listItem}>
                  <ListItemText primary="Build ID" secondary={rule.buildID} />
                </ListItem>
              )}
              {rule.buildTarget && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="Build Target"
                    secondary={rule.buildTarget}
                  />
                </ListItem>
              )}
              {rule.locale && (
                <ListItem className={classes.listItem}>
                  <ListItemText primary="Locale" secondary={rule.locale} />
                </ListItem>
              )}
              {rule.distribution && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="Distribution"
                    secondary={rule.distribution}
                  />
                </ListItem>
              )}
              {rule.distVersion && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="Distribution Version"
                    secondary={rule.distVersion}
                  />
                </ListItem>
              )}
              {rule.osVersion && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="OS Version"
                    secondary={rule.osVersion}
                    secondaryTypographyProps={{
                      className: classes.textEllipsis,
                    }}
                  />
                </ListItem>
              )}
              {rule.instructionSet && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="Instruction Set"
                    secondary={rule.instructionSet}
                  />
                </ListItem>
              )}
              {rule.memory && (
                <ListItem className={classes.listItem}>
                  <ListItemText primary="Memory" secondary={rule.memory} />
                </ListItem>
              )}
              {rule.mig64 && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="64-bit Migration Opt-in"
                    secondary={rule.mig64}
                  />
                </ListItem>
              )}
              {rule.jaws && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="Incompatible JAWS Screen Reader"
                    secondary={rule.jaws}
                  />
                </ListItem>
              )}
              {rule.headerArchitecture && (
                <ListItem className={classes.listItem}>
                  <ListItemText
                    primary="Header Architecture"
                    secondary={rule.headerArchitecture}
                  />
                </ListItem>
              )}
            </List>
          </Grid>
        </Grid>
        {rule.scheduledChange && (
          <Fragment>
            {rule.scheduledChange.change_type !== 'insert' && (
              <Divider className={classes.divider} />
            )}
            <div className={classes.scheduledChangesHeader}>
              <Typography
                className={classes.scheduledChangesTitle}
                variant="subtitle1">
                Scheduled Changes
              </Typography>
              <Chip
                className={classNames(classes.chip, {
                  [classes.deleteChip]:
                    rule.scheduledChange.change_type === 'delete',
                })}
                icon={<ChipIcon className={classes.chipIcon} size={16} />}
                label={`${distanceInWordsStrict(
                  new Date(),
                  rule.scheduledChange.when,
                  { addSuffix: true }
                )} (${rule.scheduledChange.change_type})`}
              />
            </div>
            {rule.scheduledChange.change_type === 'delete' ? (
              <Typography
                className={classes.deletedText}
                variant="body2"
                color="textSecondary">
                All properties will be deleted
              </Typography>
            ) : (
              type && (
                <Diff
                  className={classes.diff}
                  viewType="split"
                  diffType={type}
                  hunks={hunks || []}>
                  {hunks =>
                    hunks.map(hunk => <Hunk key={hunk.content} hunk={hunk} />)
                  }
                </Diff>
              )
            )}
          </Fragment>
        )}
      </CardContent>
      <CardActions className={classes.cardActions}>
        <Button color="secondary">Duplicate</Button>
        <Button color="secondary">Update</Button>
        <Button color="secondary">Delete</Button>
      </CardActions>
    </Card>
  );
}

RuleCard.propTypes = {
  rule,
};

export default RuleCard;
