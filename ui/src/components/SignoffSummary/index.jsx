import React from 'react';
import { object, string } from 'prop-types';
import classNames from 'classnames';
import { makeStyles } from '@material-ui/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles(theme => ({
  listSubheader: {
    lineHeight: 1.5,
    marginBottom: theme.spacing(0.5),
    paddingLeft: theme.spacing(1),
  },
  listWrapper: {
    display: 'flex',
  },
  listItemText: {
    marginBottom: 0,
    marginTop: 0,
  },
  signoffsList: {
    marginRight: theme.spacing(6),
    paddingTop: 0,
    paddingBottom: 0,
  },
  signedBy: {
    display: 'flex',
    alignItems: 'center',
  },
}));

function SignoffSummary(props) {
  const classes = useStyles();
  const { requiredSignoffs, signoffs, className } = props;

  const listOfSignoffs = Object.entries(signoffs);

  return (
    <div className={classNames(classes.listWrapper, className)}>
      <List
        dense
        subheader={
          <ListSubheader className={classes.listSubheader}>
            Requires Signoffs From
          </ListSubheader>
        }>
        {Object.entries(requiredSignoffs).map(([role, count], index) => {
          const key = `${role}-${index}`;

          return (
            <ListItem key={key} className={classes.signoffsList}>
              <ListItemText
                primary={
                  <Typography component="p" variant="body2">
                    {`${count} member${count > 1 ? 's' : ''} of ${role}`}
                  </Typography>
                }
                className={classes.listItemText}
              />
            </ListItem>
          );
        })}
      </List>
      {listOfSignoffs && Boolean(listOfSignoffs.length) && (
        <List
          dense
          subheader={
            <ListSubheader className={classes.listSubheader}>
              Signed By
            </ListSubheader>
          }>
          {listOfSignoffs.map(([username, signoffRole]) => (
            <ListItem key={username} className={classes.signoffsList}>
              <ListItemText
                disableTypography
                primary={
                  <Typography
                    component="p"
                    className={classes.signedBy}
                    variant="body2">
                    {username}
                    &nbsp; - &nbsp;
                    <Typography
                      component="span"
                      color="textSecondary"
                      variant="caption">
                      {signoffRole}
                    </Typography>
                  </Typography>
                }
                className={classes.listItemText}
              />
            </ListItem>
          ))}
        </List>
      )}
    </div>
  );
}

SignoffSummary.propTypes = {
  requiredSignoffs: object.isRequired,
  signoffs: object.isRequired,
  className: string,
};

SignoffSummary.defaultProps = {
  className: null,
};

export default SignoffSummary;
