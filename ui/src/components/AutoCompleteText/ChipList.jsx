import React from 'react';
import classNames from 'classnames';
import { object, func, arrayOf, string } from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import Chip from '@material-ui/core/Chip';
import CloseIcon from 'mdi-react/CloseIcon';

const useStyles = makeStyles(theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    width: '200rem',
    flexGrow: '1',
    gap: '0.25rem',
    padding: '0.5rem 0',
  },
  chip: {
    marginRight: theme.spacing(0.5),
    fontSize: '0.60rem',
  },
  closeIcon: {
    height: 12,
    width: 24,
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
          deleteIcon={<CloseIcon className={classes.closeIcon} />}
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
