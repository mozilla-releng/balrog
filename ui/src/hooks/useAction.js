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
export default (action) => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const state = { loading, data, error };
  const performAction = async (...body) => {
    try {
      setLoading(true);
      setData(null);
      setError(null);
      const data = await action(...body);

      setData(data);

      // If we don't explicitly overwrite `error` here, any previous errors
      // will remain when the caller receives the return value, which
      // prevents them from accurately detecting success/failure
      return { loading: false, data, error: null };
    } catch (e) {
      setError(e);

      // Similarly, the caller will not see the error immediately without
      // explicitly setting it.
      return { ...state, loading: false, error: e };
    } finally {
      setLoading(false);
    }
  };

  return [state, performAction];
};
