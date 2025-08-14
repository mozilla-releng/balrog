import { withAuth0 } from '@auth0/auth0-react';
import Card from '@mui/material/Card';
import CardActionArea from '@mui/material/CardActionArea';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import classNames from 'classnames';
import AccountGroupIcon from 'mdi-react/AccountGroupIcon';
import ArrowRightIcon from 'mdi-react/ArrowRightIcon';
import KeyVariantIcon from 'mdi-react/KeyVariantIcon';
import PencilIcon from 'mdi-react/PencilIcon';
import { arrayOf, func, object, string } from 'prop-types';
import React, { Fragment } from 'react';
import { makeStyles } from 'tss-react/mui';
import { LABELS } from '../../utils/constants';
import Link from '../../utils/Link';
import { getPermissionString, getRolesString } from '../../utils/userUtils';
import Button from '../Button';
import SignoffSummary from '../SignoffSummary';
import StatusLabel from '../StatusLabel';

const useStyles = makeStyles()((theme) => ({
  card: {
    listStyle: 'none',
  },
  cardHeader: {
    borderBottom: '1px gray dashed',
  },
  cardHeaderAction: {
    alignSelf: 'end',
  },
  cardActions: {
    justifyContent: 'flex-end',
  },
  pencilIcon: {
    marginRight: theme.spacing(1),
  },
  link: {
    ...theme.mixins.link,
  },
  scheduledChangeContainer: {
    display: 'flex',
    marginBottom: theme.spacing(1),
    textAlign: 'justify',
    alignItems: 'center',
  },
  statusLabelDiv: {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(4),
  },
  propertyWithScheduledChange: {
    ...theme.mixins.redDot,
    display: 'inline-block',
  },
  arrowRightIcon: {
    margin: `0 ${theme.spacing(1)}`,
  },
  permissionText: {
    wordBreak: 'break-all',
  },
  signoffSummary: {
    marginLeft: -8,
  },
}));

function getStatus(changeType) {
  switch (changeType) {
    case 'insert':
      return LABELS.PENDING_INSERT;
    case 'delete':
      return LABELS.PENDING_DELETE;
    default:
      return LABELS.PENDING_UPDATE;
  }
}

function User(props) {
  const { classes } = useStyles();
  const {
    auth0,
    className,
    username,
    roles,
    permissions,
    scheduledPermissions,
    onSignoff,
    onRevoke,
  } = props;
  const returnOptionIfExists = (options, key, defaultValue) => {
    if (options?.[key]) {
      return options[key];
    }

    return defaultValue;
  };

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
      {/* We don't need to check roles here because users without permissions
            cannot hold roles */}
      {Object.keys(permissions).length > 0 && (
        <CardContent>
          <List dense>
            {Object.entries(permissions).map(([permission, details]) => (
              <ListItem key={permission} disableGutters>
                <ListItemIcon>
                  <KeyVariantIcon />
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Fragment>
                      {getPermissionString(
                        permission,
                        returnOptionIfExists(details.options, 'actions', []),
                        returnOptionIfExists(details.options, 'products', []),
                      )}
                      {scheduledPermissions[permission] && (
                        <span className={classes.propertyWithScheduledChange} />
                      )}
                    </Fragment>
                  }
                />
              </ListItem>
            ))}
            {roles.length > 0 && (
              <ListItem disableGutters>
                <ListItemIcon>
                  <AccountGroupIcon />
                </ListItemIcon>
                <ListItemText>holds the {getRolesString(roles)}</ListItemText>
              </ListItem>
            )}
          </List>
        </CardContent>
      )}
      {Object.keys(scheduledPermissions).length > 0 &&
        Object.entries(scheduledPermissions).map(([permission, details]) => (
          <Fragment key={permission}>
            {Object.keys(permissions).length > 0 && <Divider />}
            <CardContent className={classes.scheduled}>
              <div className={classes.scheduledChangeContainer}>
                {permissions[permission] && (
                  <Fragment>
                    <Typography
                      variant="body2"
                      className={classes.permissionText}
                    >
                      <em>
                        {getPermissionString(
                          permission,
                          returnOptionIfExists(
                            permissions[permission].options,
                            'actions',
                            [],
                          ),
                          returnOptionIfExists(
                            permissions[permission].options,
                            'products',
                            [],
                          ),
                        )}
                      </em>
                    </Typography>
                    <ArrowRightIcon className={classes.arrowRightIcon} />
                  </Fragment>
                )}
                <Typography variant="body2" className={classes.permissionText}>
                  <em>
                    {getPermissionString(
                      permission,
                      returnOptionIfExists(details.options, 'actions', []),
                      returnOptionIfExists(details.options, 'products', []),
                      details.change_type,
                    )}
                  </em>
                </Typography>
              </div>
              <div className={classes.statusLabelDiv}>
                <StatusLabel state={getStatus(details.change_type)} />
              </div>
              {Object.keys(details.required_signoffs).length > 0 && (
                <SignoffSummary
                  className={classes.signoffSummary}
                  requiredSignoffs={details.required_signoffs}
                  signoffs={details.signoffs}
                />
              )}
            </CardContent>
            {Object.keys(details.required_signoffs).length > 0 && (
              <CardActions className={classes.cardActions}>
                {auth0.user && auth0.user.email in details.signoffs ? (
                  <Button color="secondary" onClick={() => onRevoke(details)}>
                    Revoke Signoff
                  </Button>
                ) : (
                  <Button color="secondary" onClick={() => onSignoff(details)}>
                    Signoff
                  </Button>
                )}
              </CardActions>
            )}
          </Fragment>
        ))}
    </Card>
  );
}

User.propTypes = {
  username: string.isRequired,
  roles: arrayOf(object),
  permissions: object,
  scheduledPermissions: object,
  onSignoff: func.isRequired,
  onRevoke: func.isRequired,
};

User.defaultProps = {
  roles: [],
  permissions: {},
  scheduledPermissions: {},
};

export default withAuth0(User);
