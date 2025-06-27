import { withAuth0 } from '@auth0/auth0-react';
import React, { useState, Fragment } from 'react';
import { makeStyles } from '@material-ui/styles';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import IconButton from '@material-ui/core/IconButton';
import SettingsOutlineIcon from 'mdi-react/SettingsOutlineIcon';
import Link from '../../utils/Link';
import menuItems from './menuItems';

const useStyles = makeStyles(theme => ({
  settings: {
    height: theme.spacing(6),
    width: theme.spacing(6),
    padding: 0,
    margin: `0 ${theme.spacing(1)}px`,
  },
  settingsIcon: {
    fill: '#fff',
  },
  settingsIconDisabled: {
    fill: theme.palette.grey[500],
  },
  link: {
    ...theme.mixins.link,
  },
}));

function SettingsMenu({ auth0, disabled }) {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);
  const handleMenuOpen = e => setAnchorEl(e.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);

  return (
    <Fragment>
      <IconButton
        disabled={!auth0.user || disabled}
        className={classes.settings}
        aria-haspopup="true"
        aria-controls="user-menu"
        aria-label="user menu"
        onClick={handleMenuOpen}>
        <SettingsOutlineIcon
          size={24}
          className={
            auth0.user && !disabled
              ? classes.settingsIcon
              : classes.settingsIconDisabled
          }
        />
      </IconButton>
      <Menu
        id="user-menu"
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        getContentAnchorEl={null}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        onClose={handleMenuClose}>
        {menuItems.settings.map(navItem => (
          <MenuItem dense key={navItem.value} title={navItem.value}>
            <Link
              className={classes.link}
              to={
                window.location.pathname === navItem.path
                  ? `${window.location.pathname}${window.location.search}`
                  : navItem.path
              }>
              {navItem.value.toUpperCase()}
            </Link>
          </MenuItem>
        ))}
      </Menu>
    </Fragment>
  );
}

export default withAuth0(SettingsMenu);
