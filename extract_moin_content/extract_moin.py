"""
Extract content from old moinmoin wikis.

Extract:
  1. Latest version of each page into single directory.
     This is to have something suitable for easy grepping of old notes.
  2. Complete revision history into separate single directory.
     This is so I still have the old data if I want it.
  3. Attachments into another directory, with parent directories based
     on page names.

Primarly tested with 1.5.5a wikis.

"""
import errno
import os
import sys


def parse_args():
    """Check args. Return src and dst directories."""
    try:
        # num arguments
        if len(sys.argv) != 3:
            raise RuntimeError('Two arguments required. Received {}.'.format(len(sys.argv)-1))

        # source directory
        src = sys.argv[1]
        if not os.path.isdir(os.path.join(src, 'underlay')) \
        or not os.path.isdir(os.path.join(src, 'data', 'pages')):
            raise RuntimeError('Source does not have expected "underlay" or "data/pages" directories.')

        # destination directory
        dst = sys.argv[2]
        try:
            os.makedirs(dst)
        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(dst):
                pass
            else:
                raise RuntimeError('Failed to create destination directory.')
        if os.listdir(dst):
            raise RuntimeError('Destination directory is not empty.')
    except RuntimeError as ex:
        print 'Usage: python extract_moin.py src-directory dst-directory'
        print
        print ex.message
        sys.exit(-1)
    return src, dst


def main():
    """Extract content from command-line-specified moin src to specified dst directory."""
    src, dst = parse_args()
    # see if I can preserve file modification time!
    # this seems to be what ls -l shows
    # seems like cp -p will give that

if __name__ == '__main__':
    main()
