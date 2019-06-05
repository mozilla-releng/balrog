import React, { Fragment } from 'react';
import { string, node } from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import menuItems from './menuItems';
import Link from '../../utils/Link';
import UserMenu from './UserMenu';
import SettingsMenu from './SettingsMenu';

const useStyles = makeStyles(theme => ({
  appbar: {
    height: theme.spacing(8),
  },
  title: {
    textDecoration: 'none',
  },
  main: {
    maxWidth: 980,
    height: window.innerHeight - theme.spacing(8),
    margin: `${theme.spacing(10)}px auto`,
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
  buttonWithIcon: {
    paddingLeft: theme.spacing(2),
  },
}));

export default function Dashboard(props) {
  const classes = useStyles();
  const { title, children } = props;

  return (
    <Fragment>
      <AppBar className={classes.appbar}>
        <Toolbar>
          <Typography
            className={classes.title}
            color="inherit"
            variant="h6"
            noWrap
            component={Link}
            to="/">
            Balrog Admin ┃ {title}
          </Typography>
          <nav className={classes.nav}>
            {menuItems.main.map(menuItem => (
              <Link
                key={menuItem.value}
                className={classes.link}
                nav
                to={menuItem.path}>
                <Button color="inherit">{menuItem.value}</Button>
              </Link>
            ))}
            <SettingsMenu />
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
};
