import React from 'react';
import { object, string } from 'prop-types';
import classNames from 'classnames';
import { makeStyles } from '@material-ui/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import Typography from '@material-ui/core/Typography';
import CheckCircleIcon from 'mdi-react/CheckCircleIcon';
import AccountClockIcon from 'mdi-react/AccountClockIcon';

const useStyles = makeStyles(theme => ({
  approval: {
    display: 'flex',
    width: 'max-content',
    flexFlow: 'row nowrap',
    justifyContent: 'center',
    alignItems: 'center',
    margin: '0 2px 0 2px',
  },
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
  signoffsContainer: {
    display: 'flex',
  },
  signoffsList: {
    width: 'max-content',
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
  const { requiredSignoffs, signoffs, className } = props;
  const listOfSignoffs = Object.entries(signoffs);
  const theRequiredSignoffs = Object.entries(requiredSignoffs);
  const classes = useStyles();

  return (
    <div className={classNames(classes.listWrapper, className)}>
      <List
        dense
        subheader={
          <ListSubheader className={classes.listSubheader}>
            Requires Signoffs From
          </ListSubheader>
        }>
        {theRequiredSignoffs.map(([role, count], index) => {
          const key = `${role}-${index}`;
          // allSigned Returns all that have signed
          let allSigned = [];

          if (listOfSignoffs) {
            allSigned = listOfSignoffs.filter(arr => {
              return role === arr[1];
            });
          }

          // allNotSigned() Gets and returns all that haven't signed
          const allNotSigned = () => {
            const leftarr = [];
            const allleft = count - allSigned.length;

            // Disabled eslint because "i+1" runs loop till eternity
            // eslint-disable-next-line no-plusplus
            for (let i = 0; i < allleft; i++) {
              leftarr.push([]);
            }

            return leftarr;
          };

          return (
            <div key={key} className={classes.signoffsContainer}>
              <ListItem className={classes.signoffsList}>
                <ListItemText
                  primary={
                    <Typography component="p" variant="body2">
                      {role === "admin" ? `${count} member${count > 1 ? 's' : ''} with full fledged ${role} permissions - `
                      :`${count} member${count > 1 ? 's' : ''} of ${role} - `}
                    </Typography>
                  }
                  className={classes.listItemText}
                />
                {listOfSignoffs && (
                  <React.Fragment>
                    {allSigned.map((arr, index) => {
                      const no = index;

                      return (
                        <div key={no} className={classes.approval}>
                          <CheckCircleIcon color="green" />
                          <Typography
                            component="p"
                            variant="body2"
                            style={{ color: 'green', width: 'max-content' }}>
                            {`${arr[0]}`}
                          </Typography>
                        </div>
                      );
                    })}
                    {allNotSigned().map(arr => {
                      const no = arr;

                      return (
                        <div key={no} className={classes.approval}>
                          <AccountClockIcon color="darkorange" />
                          <Typography
                            component="p"
                            variant="body2"
                            style={{ color: 'darkorange' }}>
                            Awaiting approval...
                          </Typography>
                        </div>
                      );
                    })}
                  </React.Fragment>
                )}
              </ListItem>
            </div>
          );
        })}
      </List>
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
