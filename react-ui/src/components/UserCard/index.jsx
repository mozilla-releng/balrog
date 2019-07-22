import React from 'react';
import { string, object } from 'prop-types';
import classNames from 'classnames';
import Card from '@material-ui/core/Card';
import { makeStyles } from '@material-ui/styles';
import CardHeader from '@material-ui/core/CardHeader';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import AccountGroupIcon from 'mdi-react/AccountGroupIcon';
import KeyVariantIcon from 'mdi-react/KeyVariantIcon';
import PencilIcon from 'mdi-react/PencilIcon';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Link from '../../utils/Link';
import { getPermissionString, getRolesString } from '../../utils/userUtils';

const useStyles = makeStyles(theme => ({
  card: {
    listStyle: 'none',
  },
  cardHeader: {
    borderBottom: '1px gray dashed',
  },
  cardHeaderAction: {
    alignSelf: 'end',
  },
  pencilIcon: {
    marginRight: theme.spacing(1),
  },
  link: {
    ...theme.mixins.link,
  },
}));

export default function User(props) {
  const classes = useStyles();
  const { className, username, roles, permissions } = props;
  const returnOptionIfExists = (options, key, defaultValue) => {
    if (options && options[key]) {
      return options[key];
    }

    return defaultValue;
  };

  // TODO: Add admin-or-not marker. Needs backend support.
  // should links like the ones below be in a component?
  return (
    <Card className={classNames(classes.card, className)}>
      <Link className={classes.link} to={`/users/${username}`}>
        <CardActionArea>
          <CardHeader
            classes={{ action: classes.cardHeaderAction }}
            className={classes.cardHeader}
            title={username}
            action={<PencilIcon className={classes.pencilIcon} />}
          />
        </CardActionArea>
      </Link>
      <CardContent>
        <List>
          {Object.entries(permissions).map(([permission, details]) => (
            <ListItem key={permission}>
              <ListItemIcon>
                <KeyVariantIcon />
              </ListItemIcon>
              <ListItemText>
                {getPermissionString(
                  permission,
                  returnOptionIfExists(details.options, 'actions', []),
                  returnOptionIfExists(details.options, 'products', [])
                )}
              </ListItemText>
            </ListItem>
          ))}
          {Object.keys(roles).length > 0 && (
            <ListItem>
              <ListItemIcon>
                <AccountGroupIcon />
              </ListItemIcon>
              <ListItemText>
                holds the {getRolesString(Object.keys(roles))}
              </ListItemText>
            </ListItem>
          )}
        </List>
      </CardContent>
    </Card>
  );
}

User.propTypes = {
  username: string.isRequired,
  roles: object,
  permissions: object,
};

User.defaultProps = {
  roles: {},
  permissions: {},
};
