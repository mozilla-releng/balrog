import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import {
  arrayOf,
  func,
  number,
  object,
  oneOf,
  oneOfType,
  string,
} from 'prop-types';
import React from 'react';

/**
 * A table to display a set of data elements.
 */
export default function DataTable(props) {
  const {
    items,
    columnsSize,
    renderRow,
    headers,
    sortByHeader,
    sortDirection,
    noItemsMessage,
    tableHeadCellProps,
    onHeaderClick: _,
    ...rest
  } = props;
  const colSpan = columnsSize || headers?.length || 0;
  const handleHeaderClick = ({ target }) => {
    const { onHeaderClick } = props;

    if (onHeaderClick) {
      onHeaderClick(target.id);
    }
  };

  return (
    <Table {...rest}>
      {headers && (
        <TableHead>
          <TableRow>
            {headers.map((header) => (
              <TableCell key={`table-header-${header}`} {...tableHeadCellProps}>
                <TableSortLabel
                  id={header}
                  active={header === sortByHeader}
                  direction={sortDirection || 'desc'}
                  onClick={handleHeaderClick}
                >
                  {header}
                </TableSortLabel>
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
      )}
      <TableBody>
        {items.length === 0 ? (
          <TableRow>
            <TableCell colSpan={colSpan}>
              <em>{noItemsMessage}</em>
            </TableCell>
          </TableRow>
        ) : (
          items.map(renderRow)
        )}
      </TableBody>
    </Table>
  );
}

DataTable.propTypes = {
  /**
   * The number of columns the table contains.
   * */
  columnsSize: number,
  /**
   * A function to execute for each row to render in the table.
   * Will be passed a datum from the table data. The function
   * should return the JSX necessary to render the given row.
   */
  renderRow: func.isRequired,
  /**
   * A function to execute when a column header is clicked.
   * Will receive a single argument which is the column name.
   * This can be used to handle sorting.
   */
  onHeaderClick: func,
  /**
   * A header name to sort on.
   */
  sortByHeader: string,
  /**
   * The sorting direction.
   */
  sortDirection: oneOf(['desc', 'asc']),
  /**
   * A list of header names to use on the table starting from the left.
   */
  headers: arrayOf(string),
  /**
   * A list of objects or strings to display. Each element in
   * the list is represented by a row and each element represents a column.
   */
  items: arrayOf(oneOfType([object, string])).isRequired,
  /**
   * A message to display when there is no items to display.
   */
  noItemsMessage: string,
  /**
   * Props given to each table head cell.
   */
  tableHeadCellProps: object,
};

DataTable.defaultProps = {
  columnsSize: null,
  headers: null,
  onHeaderClick: null,
  sortByHeader: null,
  sortDirection: 'desc',
  noItemsMessage: 'No items for this page.',
  tableHeadCellProps: null,
};
