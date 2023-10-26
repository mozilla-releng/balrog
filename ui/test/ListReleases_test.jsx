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
    test('should highlight when only one matching substring', () => {
        const result = highlightMatchedRelease(
            [
                [0, 17],
                [15, 17]
            ],
            'Windows-7-8-81-Desupport'
        );
        const highlighted = [
            'Windows-7-8-81-',
            <mark key={1}>De</mark>,
            'support'
        ]
        expect(result.props).toStrictEqual({
                children: highlighted
        })
    });
    test('should highlight when two matching substrings', () => {
        const result = highlightMatchedRelease(
            [
                [0, 8],
                [2, 4],
                [6, 8]
            ],
            'Widevine-4.10.2710.0'
        );
        const highlighted = [
            'Wi',
            <mark key={1}>de</mark>,
            'vi',
            <mark key={2}>ne</mark>,
            '-4.10.2710.0'
        ]
        expect(result.props).toStrictEqual({
                children: highlighted
        })
    });
    test('should highlight when release name ends with last matching substring', () => {
        const result = highlightMatchedRelease(
            [
                [0, 33],
                [30, 33]
            ],
            'Firefox-102.15.1esr-build1-No-WNP'
        );
        const highlighted = [
            'Firefox-102.15.1esr-build1-No-',
            <mark key={1}>WNP</mark>
        ]
        expect(result.props).toStrictEqual({
                children: highlighted
        })
    });
})
