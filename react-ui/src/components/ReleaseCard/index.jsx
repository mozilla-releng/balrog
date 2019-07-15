import React from 'react';
import { func } from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import CardHeader from '@material-ui/core/CardHeader';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Chip from '@material-ui/core/Chip';
import Grid from '@material-ui/core/Grid';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import IconButton from '@material-ui/core/IconButton';
import Tooltip from '@material-ui/core/Tooltip';
import HistoryIcon from 'mdi-react/HistoryIcon';
import LinkIcon from 'mdi-react/LinkIcon';
import Link from '../../utils/Link';
import { release } from '../../utils/prop-types';

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
  ruleName: {
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
}));

function ReleaseCard(props) {
  const { release, onAccessChange, ...rest } = props;
  const classes = useStyles();
  const hasRulesPointingAtRevision = release.rule_ids.length > 0;
  // eslint-disable-next-line no-unused-vars
  const onReleaseDelete = release => {};
  const handleAccessChange = ({ target: { checked } }) => {
    onAccessChange({ release, checked });
  };

  return (
    <Card classes={{ root: classes.root }} {...rest}>
      <CardHeader
        className={classes.cardHeader}
        classes={{ content: classes.cardHeaderContent }}
        title={
          <Typography component="h2" variant="h6">
            {release.name}{' '}
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
            <Tooltip title="History">
              <IconButton>
                <HistoryIcon />
              </IconButton>
            </Tooltip>
          </div>
        }
      />
      <CardContent classes={{ root: classes.cardContentRoot }}>
        <List>
          <Grid container>
            <Grid item xs={12}>
              <ListItem className={classes.listItem}>
                <ListItemText
                  primary="Data Version"
                  secondary={release.data_version}
                />
              </ListItem>
            </Grid>
            <Grid item>
              <ListItem className={classes.listItem}>
                <ListItemText
                  primary="Used By"
                  secondaryTypographyProps={{ component: 'div' }}
                  secondary={
                    hasRulesPointingAtRevision ? (
                      release.rule_ids.map(ruleId => (
                        <Link key={ruleId} to={`/rules/${ruleId}`}>
                          <Chip
                            clickable
                            size="small"
                            icon={<LinkIcon />}
                            label={ruleId}
                            className={classes.chip}
                          />
                        </Link>
                      ))
                    ) : (
                      <em>n/a</em>
                    )
                  }
                />
              </ListItem>
            </Grid>
          </Grid>
        </List>
      </CardContent>
      <CardActions className={classes.cardActions}>
        <Link to={`/releases/${release.name}`}>
          <Button disabled={release.read_only} color="secondary">
            Update
          </Button>
        </Link>
        {!hasRulesPointingAtRevision && (
          <Button
            disabled={release.read_only}
            color="secondary"
            onClick={() => onReleaseDelete(release)}>
            Delete
          </Button>
        )}
      </CardActions>
    </Card>
  );
}

ReleaseCard.propTypes = {
  release: release.isRequired,
  onAccessChange: func.isRequired,
};

export default ReleaseCard;
