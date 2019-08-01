import React, { Fragment, useState } from 'react';
import { stringify } from 'qs';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import DataTable from '../../components/DataTable';
import HistoryFilter from '../../components/HistoryFilter';
import Dashboard from '../../components/Dashboard';
import ErrorPanel from '../../components/ErrorPanel';
import { getHistory } from '../../utils/History';
import tryCatch from '../../utils/tryCatch';

function History(props) {
  const [error, setError] = useState(null);

  async function handleFormSubmit(data) {
    const qs = stringify(
      {
        changed_by: data.changedBy,
        timestamp_from: data.dateTimeStart,
        timestamp_to: data.dateTimeEnd,
        product: data.product,
        channel: data.channel,
      },
      { addQueryPrefix: true }
    );
    // eslint-disable-next-line no-unused-vars
    const [err, history] = await tryCatch(getHistory(data.object, qs));

    if (err) {
      setError(err);
    } else {
      props.history.push(`/history/${data.object}${qs}`);
    }
  }

  return (
    <Dashboard title="History">
      <Fragment>
        {error && <ErrorPanel fixed error={error} />}
        <HistoryFilter onSubmit={handleFormSubmit} />
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
