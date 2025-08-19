import CloseIcon from '@mui/icons-material/Close';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import MuiSpeedDial from '@mui/material/SpeedDial';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import classNames from 'classnames';
import { arrayOf, node, object, oneOfType } from 'prop-types';
import React, { useState } from 'react';
import { makeStyles } from 'tss-react/mui';

const useStyles = makeStyles()((theme) => ({
  speedDial: {
    ...theme.mixins.fab,
  },
}));

function SpeedDial({ children, className, FabProps, ...props }) {
  const { classes } = useStyles();
  const [open, setOpen] = useState(false);
  const handleClick = () => setOpen(!open);
  const handleClose = () => setOpen(false);
  const handleOpen = () => setOpen(true);

  return (
    <MuiSpeedDial
      ariaLabel="speed-dial"
      icon={<SpeedDialIcon icon={<MoreVertIcon />} openIcon={<CloseIcon />} />}
      FabProps={{ color: 'secondary', ...FabProps }}
      className={classNames(classes.speedDial, className)}
      onBlur={handleClose}
      onClick={handleClick}
      onClose={handleClose}
      onFocus={handleOpen}
      onMouseEnter={handleOpen}
      onMouseLeave={handleClose}
      open={open}
      {...props}
    >
      {children}
    </MuiSpeedDial>
  );
}

SpeedDial.propTypes = {
  /**
   * A set of `SpeedDialAction`s which will be rendered upon interaction
   * with the base `SpeedDial` floating action button.
   */
  children: oneOfType([arrayOf(node), node]).isRequired,
  FabProps: object,
};

SpeedDial.defaultProps = {
  FabProps: {},
};

export default SpeedDial;
