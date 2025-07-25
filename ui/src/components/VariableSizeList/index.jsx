import { number } from 'prop-types';
import React, {
  forwardRef,
  useEffect,
  useImperativeHandle,
  useRef,
} from 'react';
import { AutoSizer, List, WindowScroller } from 'react-virtualized';
import { APP_BAR_HEIGHT } from '../../utils/constants';

const VariableSizeList = forwardRef((props, ref) => {
  const { scrollToRow, pathname, ...rest } = props;
  const listRef = useRef(null);

  useEffect(() => {
    const rowOffset = listRef.current.getOffsetForRow({ index: scrollToRow });

    if (pathname === '/rules') {
      listRef.current.scrollToPosition(
        rowOffset - APP_BAR_HEIGHT - rest.searchFieldHeight,
      );
    } else {
      listRef.current.scrollToPosition(rowOffset - APP_BAR_HEIGHT);
    }
  }, [scrollToRow]);

  useImperativeHandle(ref, () => ({
    recomputeRowHeights: (index) => listRef.current.recomputeRowHeights(index),
  }));

  return (
    <WindowScroller>
      {({ height, onChildScroll, isScrolling, scrollTop }) => (
        <AutoSizer disableHeight>
          {({ width }) => (
            <List
              autoHeight
              ref={listRef}
              isScrolling={isScrolling}
              onScroll={onChildScroll}
              scrollToAlignment="start"
              height={height}
              width={width}
              estimatedRowSize={400}
              overscanRowCount={5}
              scrollTop={scrollTop}
              {...rest}
            />
          )}
        </AutoSizer>
      )}
    </WindowScroller>
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
