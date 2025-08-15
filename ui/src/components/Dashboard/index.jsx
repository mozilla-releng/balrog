import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { bool, node, string } from 'prop-types';
import React, { Fragment } from 'react';
import { useLocation } from 'react-router-dom';
import { makeStyles } from 'tss-react/mui';
import { APP_BAR_HEIGHT, CONTENT_MAX_WIDTH } from '../../utils/constants';
import Link from '../../utils/Link';
import Button from '../Button';
import menuItems from './menuItems';
import SettingsMenu from './SettingsMenu';
import UserMenu from './UserMenu';

const useStyles = makeStyles()((theme) => ({
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
    padding: `${theme.spacing(12)} ${APP_BAR_HEIGHT}px`,
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
}));

export default function Dashboard(props) {
  const { classes } = useStyles();
  const { title, children, disabled } = props;
  const location = useLocation();

  return (
    <Fragment>
      <title>{`${title} - Balrog Admin`}</title>
      <AppBar className={classes.appbar}>
        <Toolbar>
          <Typography
            className={classes.title}
            color="inherit"
            variant="h6"
            noWrap
            component={Link}
            to="/"
          >
            Balrog Admin ┃ {title}
          </Typography>
          <nav className={classes.nav}>
            {menuItems.main.map((menuItem) => (
              <Link
                key={menuItem.value}
                className={disabled ? classes.disabledLink : classes.link}
                nav
                to={
                  location.pathname === menuItem.path
                    ? `${location.pathname}${location.search}`
                    : menuItem.path
                }
              >
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
