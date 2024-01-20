import React, { Fragment } from 'react';
import { string, node, bool } from 'prop-types';
import { Helmet } from 'react-helmet';
import { makeStyles } from '@material-ui/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Box from '@material-ui/core/Box';
import menuItems from './menuItems';
import Link from '../../utils/Link';
import UserMenu from './UserMenu';
import Button from '../Button';
import SettingsMenu from './SettingsMenu';
import { CONTENT_MAX_WIDTH, APP_BAR_HEIGHT } from '../../utils/constants';

const useStyles = makeStyles(theme => ({
  appbar: {
    height: APP_BAR_HEIGHT,
  },
  title: {
    textDecoration: 'none',
  },
  main: {
    maxWidth: CONTENT_MAX_WIDTH,
    height: '100%',
    margin: '0 auto',
    padding: `${theme.spacing(12)}px ${APP_BAR_HEIGHT}px`,
  },
  nav: {
    display: 'flex',
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  link: {
    textDecoration: 'none',
    color: 'inherit',
  },
  disabledLink: {
    textDecoration: 'none',
    color: theme.palette.grey[500],
    pointerEvents: 'none',
  },
  buttonWithIcon: {
    paddingLeft: theme.spacing(2),
  },
  protocolLogo: {
    margin: '0px',
    marginRight: '.7%',
  },
  extensionIcon: {
    margin: '0px',
    marginRight: '.5%',
  },
}));

function Logo() {
  const classes = useStyles();

  return (
    <Box
      component="div"
      className={`mzp-c-logo mzp-t-logo-md mzp-t-product-firefox ${classes.protocolLogo}`}
    />
  );
}

export default function Dashboard(props) {
  const classes = useStyles();
  const { title, children, disabled } = props;

  return (
    <Fragment>
      <Helmet>
        <title>{title} - Balrog Admin</title>
      </Helmet>
      <AppBar className={classes.appbar}>
        <Toolbar>
          <Logo />
          <nav className={classes.nav}>
            {menuItems.main.map(menuItem => (
              <Link
                key={menuItem.value}
                className={disabled ? classes.disabledLink : classes.link}
                nav
                to={
                  window.location.pathname === menuItem.path
                    ? `${window.location.pathname}${window.location.search}`
                    : menuItem.path
                }>
                <Button color="inherit">{menuItem.value}</Button>
              </Link>
            ))}
            <SettingsMenu disabled={disabled} />
            <UserMenu />
          </nav>
        </Toolbar>
      </AppBar>
      <main className={classes.main}>{children}</main>
    </Fragment>
  );
}

Dashboard.prototype = {
  children: node.isRequired,
  // A title for the view.
  title: string.isRequired,
  disabled: bool,
};
