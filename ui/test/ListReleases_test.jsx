import React from 'react'
import highlightMatchedRelease from "../src/utils/highlightMatchedRelease";

describe('highlighting release', () => {
    test('should return a React Fragment', () => {
        const result = highlightMatchedRelease(
            [
                [0, 17],
                [2, 4],
                [6, 8],
                [16, 17]
            ],
            'Widevine-4.10.2557.0-with-aarch'
        )
        expect(result.type).toBe(React.Fragment)
    });
})
