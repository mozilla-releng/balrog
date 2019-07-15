import React from 'react';
import classNames from 'classnames';
import { object, func, arrayOf, string } from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import Chip from '@material-ui/core/Chip';
import CloseIcon from 'mdi-react/CloseIcon';

const useStyles = makeStyles(theme => ({
  container: {
    display: 'flex',
  },
  chip: {
    marginRight: theme.spacing(1),
    fontSize: theme.typography.caption.fontSize,
  },
}));

function ChipList(props) {
  const { selectedItems, className, onItemDelete, chipProps, ...rest } = props;
  const classes = useStyles();

  return (
    <div className={classNames(classes.container, className)} {...rest}>
      {selectedItems.map(item => (
        <Chip
          key={item}
          className={classes.chip}
          size="small"
          deleteIcon={<CloseIcon />}
          label={item}
          onDelete={() => onItemDelete(item)}
          onClick={() => onItemDelete(item)}
          {...chipProps}
        />
      ))}
    </div>
  );
}

ChipList.propTypes = {
  selectedItems: arrayOf(string).isRequired,
  onItemDelete: func.isRequired,
  chipProps: object,
};

ChipList.defaultProps = {
  chipProps: null,
};

export default ChipList;
