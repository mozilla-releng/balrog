import { func, node, number } from 'prop-types';
import React from 'react';
import { AutoSizer, Table } from 'react-virtualized';
import 'react-virtualized/styles.css';
import { makeStyles } from '@material-ui/styles';

const useStyles = makeStyles((theme) => ({
  tableHeader: {
    textTransform: 'none',
    color: theme.palette.text.secondary,
    fontSize: theme.typography.pxToRem(12),
    lineHeight: theme.typography.pxToRem(21),
    fontWeight: theme.typography.fontWeightMedium,
    '& > [title="Compare"]': {
      marginLeft: theme.spacing(2),
    },
  },
}));

function RevisionsTable(props) {
  const classes = useStyles();
  const { rowCount, rowGetter, children } = props;
  const rowHeight = 40;
  const headerHeight = 20;
  const tableHeight = Math.min(rowCount * rowHeight + headerHeight, 300);

  return (
    <AutoSizer disableHeight>
      {({ width }) => (
        <Table
          headerClassName={classes.tableHeader}
          overscanRowCount={100}
          width={width}
          height={tableHeight}
          headerHeight={headerHeight}
          estimatedRowSize={40}
          rowHeight={rowHeight}
          rowCount={rowCount}
          rowGetter={rowGetter}
        >
          {children}
        </Table>
      )}
    </AutoSizer>
  );
}

RevisionsTable.propTypes = {
  rowCount: number.isRequired,
  rowGetter: func.isRequired,
  children: node.isRequired,
};

export default RevisionsTable;
