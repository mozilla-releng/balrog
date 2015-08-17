#!/usr/bin/env python

import itertools


DEFAULT_UPDATE_DATA = {
    'products': ['Firefox'],
    'versions': ['10.0a1', '12.0a1', '17.0a1'],
    'buildids': ['20120222174716', '20111201231412'],
    'platforms': {
        'Linux_x86-gcc3': ['GTK 2.17.'],
        'Darwin_x86-gcc3-u-i386-x86_64': ['Darwin 8', 'Darwin 9'],
        'WINNT_x86-msvc': ['Windows_NT 5.0', 'Windows_NT 6.2']
    },
    'locales': ['en-US', 'af', 'de', 'ru', 'zh-TW', 'zu'],
    'channels': ['nightly', 'aurora'],
    'distributions': ['default'],
    'distribution_versions': ['default'],
}


def generate_paths(update_data, schema_version='3', force=False):
    """Generate request paths for all intersections of the update URL data
       provided. If 'force' is True, paths with '?force=1' appended to them
       will be generated in addition to the non-forced ones."""
    paths = []
    for platform, os_versions in update_data['platforms'].items():
        url_parts = [
            # Including an empty string as the first URL part gives us the
            # leading slash we want when we join the parts later.
            [''],
            # The first part of an AUS update URL is always 'update'.
            ['update'],
            [schema_version],
            # Most of the URL parts come from the data.
            update_data['products'],
            update_data['versions'],
            update_data['buildids'],
            [platform],
            update_data['locales'],
            update_data['channels'],
            os_versions,
            update_data['distributions'],
            update_data['distribution_versions'],
            # Update URLs always end with update.xml
            ['update.xml'],
        ]
        for combo in itertools.product(*url_parts):
            path = '/'.join(combo)
            paths.append(path)
            if force:
                paths.append('%s?force=1' % path)

    return paths


if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentError

    parser = ArgumentParser()
    parser.add_argument('--product', dest='products', default=list(), action='append')
    parser.add_argument('--version', dest='versions', default=list(), action='append')
    parser.add_argument('--buildid', dest='buildids', default=list(), action='append')
    parser.add_argument('--locale', dest='locales', default=list(), action='append')
    parser.add_argument('--channel', dest='channels', default=list(), action='append')
    parser.add_argument('--distribution', dest='distributions', default=list(), action='append')
    parser.add_argument('--distribution-version', dest='distribution_versions', default=list(), action='append')
    parser.add_argument('--platform', dest='platforms', default=list(), nargs='*', action='append')
    parser.add_argument('--force', dest='force', default=False, action='store_true')

    args = parser.parse_args()

    update_data = {'platforms': {}}
    for arg in DEFAULT_UPDATE_DATA:
        if getattr(args, arg):
            if arg == 'platforms':
                allPlatforms = getattr(args, arg)
                for platformArg in allPlatforms:
                    platform, os_versions = platformArg[0], platformArg[1:]
                    if not os_versions:
                        raise ArgumentError('Found platform "%s", but no OS versions were specified for it.' % platform)
                    update_data['platforms'][platform] = os_versions
            else:
                update_data[arg] = getattr(args, arg)
        else:
            update_data[arg] = DEFAULT_UPDATE_DATA[arg]

    paths = generate_paths(update_data, force=args.force)

    print "\n".join(paths)
