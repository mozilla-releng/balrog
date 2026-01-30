import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
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

DataTable.defaultProps = {
  columnsSize: null,
  headers: null,
  onHeaderClick: null,
  sortByHeader: null,
  sortDirection: 'desc',
  noItemsMessage: 'No items for this page.',
  tableHeadCellProps: null,
};
