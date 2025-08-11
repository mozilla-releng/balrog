import { useWindowVirtualizer } from '@tanstack/react-virtual';
import { number } from 'prop-types';
import React, { forwardRef, useEffect } from 'react';

const VariableSizeList = forwardRef((props, ref) => {
  const { scrollToRow, Row, rowCount, rowHeight } = props;

  const virtualizer = useWindowVirtualizer({
    count: rowCount,
    estimateSize: rowHeight,
    overscan: 20,
  });

  const items = virtualizer.getVirtualItems();

  useEffect(() => {
    if (scrollToRow > 0) {
      virtualizer.scrollToIndex(scrollToRow, { align: 'top' });
    }
  }, [scrollToRow, virtualizer]);

  return (
    <div
      ref={ref}
      style={{
        height: virtualizer.getTotalSize(),
        position: 'relative',
      }}
    >
      {items.map((virtualRow) => (
        <Row
          key={virtualRow.key}
          index={virtualRow.index}
          ref={virtualizer.measureElement}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            transform: `translateY(${
              virtualRow.start - virtualizer.options.scrollMargin
            }px)`,
          }}
        />
      ))}
    </div>
  );
});

VariableSizeList.displayName = 'VariableSizeList';

VariableSizeList.propTypes = {
  scrollToRow: number,
};

VariableSizeList.defaultProps = {
  scrollToRow: null,
};

export default VariableSizeList;
