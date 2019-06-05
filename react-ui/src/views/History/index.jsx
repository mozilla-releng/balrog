import React, { Fragment, useState } from 'react';
import ErrorPanel from '@mozilla-frontend-infra/components/ErrorPanel';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import DataTable from '../../components/DataTable';
import HistoryForm from '../../components/HistoryForm';
import Dashboard from '../../components/Dashboard';
import { getHistory } from '../../utils/History';
import tryCatch from '../../utils/tryCatch';

function History() {
  const [error, setError] = useState(null);

  async function handleFormSubmit(data) {
    // eslint-disable-next-line no-unused-vars
    const [err, history] = await tryCatch(getHistory(data));

    if (err) {
      setError(err);
    }
  }

  return (
    <Dashboard title="History">
      <Fragment>
        {error && <ErrorPanel error={error} />}
        <HistoryForm onSubmit={handleFormSubmit} />
        <DataTable
          headers={['sno', 'Object', 'Changed By', 'Date', 'Data Version']}
          items={[]}
          renderRow={() => (
            <TableRow>
              <TableCell>1</TableCell>
              <TableCell>2</TableCell>
              <TableCell>3</TableCell>
              <TableCell>4</TableCell>
              <TableCell>5</TableCell>
            </TableRow>
          )}
        />
      </Fragment>
    </Dashboard>
  );
}

export default History;
