import { useState } from 'react';

/**
 * A hook to perform asynchronous calls.
 *
 * Hook value:
 * {
 *   loading - true if the action was triggered but
 *   has not yet been resolved/rejected
 *
 *   data - the response
 *   error - true if the action throws an error
 * }
 */
export default action => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const state = { loading, data, error };
  const performAction = async body => {
    try {
      setLoading(true);
      setData(null);
      setError(null);
      const data = await action(body);

      setData(data);

      return { ...state, data };
    } catch (e) {
      setError(e);
    } finally {
      setLoading(false);
    }
  };

  return [state, performAction];
};
