import { withAuth0 } from '@auth0/auth0-react';
import React, { useState, Fragment } from 'react';
import { makeStyles } from '@material-ui/styles';
import Avatar from '@material-ui/core/Avatar';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import IconButton from '@material-ui/core/IconButton';
import LogoutVariantIcon from 'mdi-react/LogoutVariantIcon';
import ContentCopyIcon from 'mdi-react/ContentCopyIcon';
import copy from 'clipboard-copy';
import Button from '../Button';

const useStyles = makeStyles(theme => ({
  avatar: {
    height: theme.spacing(6),
    width: theme.spacing(6),
    padding: 0,
  },
}));

function UserMenu(props) {
  const { auth0 } = props;
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);
  const handleMenuOpen = e => setAnchorEl(e.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);
  const handleLogoutClick = () => {
    handleMenuClose();
    auth0.logout({
      openUrl: false,
    });
  };

  const handleCopyAccessToken = async () => {
    const accessToken = await auth0.getAccessTokenSilently();

    copy(accessToken);
    handleMenuClose();
  };

  const handleLogin = auth0.loginWithPopup;

  return (
    <Fragment>
      {auth0.user ? (
        <IconButton
          className={classes.avatar}
          aria-haspopup="true"
          aria-controls="user-menu"
          aria-label="user menu"
          onClick={handleMenuOpen}>
          {auth0.user.picture ? (
            <Avatar alt={auth0.user.nickname} src={auth0.user.picture} />
          ) : (
            <Avatar alt={auth0.user.name}>{auth0.user.name[0]}</Avatar>
          )}
        </IconButton>
      ) : (
        <Button
          onClick={handleLogin}
          size="small"
          variant="contained"
          color="secondary">
          Login
        </Button>
      )}
      <Menu
        id="user-menu"
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        getContentAnchorEl={null}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        onClose={handleMenuClose}>
        <MenuItem title="Copy Access Token" onClick={handleCopyAccessToken}>
          <ContentCopyIcon />
          Copy Access Token
        </MenuItem>
        <MenuItem title="Logout" onClick={handleLogoutClick}>
          <LogoutVariantIcon />
          Logout
        </MenuItem>
      </Menu>
    </Fragment>
  );
}

export default withAuth0(UserMenu);
