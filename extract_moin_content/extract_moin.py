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
import subprocess
import sys


def create_directory(path):
    """Create directory at specified path if it does not exist."""
    try:
        os.makedirs(path)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise RuntimeError('Failed to create directory "{}".'.format(path))


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
        create_directory(dst)
        if os.listdir(dst):
            raise RuntimeError('Destination directory is not empty.')
    except RuntimeError as ex:
        print 'Usage: python extract_moin.py src-directory dst-directory'
        print
        print ex.message
        sys.exit(-1)
    return src, dst


def create_subdirectories(dst_base):
    """Create destination subdirectories for different kinds of content."""
    subdirs = {}
    for subdir in ['text', 'attachments', 'revisions']:
        subdirs[subdir] = os.path.join(dst_base, subdir)
        create_directory(subdirs[subdir])
    return subdirs


def normalized_page_name(name):
    """Return more readable filename without moinmoin parens escapes."""
    name = name.replace('(26)', '-and-')  # Using '-and-' rather than '&'
    name = name.replace('(2f)', '--')     # Using '--' rather than '/'
    name = name.replace('(2d)', '-')
    if '(' in name or ')' in name:
        print 'Unexpected moinmoin page name paren escape code in "{}".'.format(name)
        sys.exit(-1)
    return name


def get_pages(src_base):
    """Return dict of source revisions -> destination filename prefix."""
    pages_base = os.path.join(src_base, 'data', 'pages')
    pages = {}
    for page_dir in os.listdir(pages_base):
        pages[os.path.join(pages_base, page_dir)] = normalized_page_name(page_dir)
    return pages


def process_page_revisions(page_base, page_filename, dst_dirs):
    """Copy page revisions to destination directories with better filenames."""
    src_revisions = os.path.join(page_base, 'revisions')
    if not os.path.isdir(src_revisions):
        print 'Warning: revisions directory not found for "{0}".'.format(page_base)
        return

    max_index = -1
    for rname in os.listdir(src_revisions):
        # Track max_index
        index = int(rname.lstrip('0') or '0')
        if index > max_index:
            max_index = index

        # Construct filename with path
        src_file = os.path.join(src_revisions, rname)
        four_digits = rname[-4:]  # Copy will fail if more than 10,000 revisions
        dst_file = '{0}.{1}.moin'.format(page_filename, four_digits)
        dst_file = os.path.join(dst_dirs['revisions'], dst_file)

        # Copy, failing on overwrite, preserving timestamp
        subprocess.check_call(['cp', '-n', '-p', src_file, dst_file])
        subprocess.check_call(['diff', src_file, dst_file])

    # copy max_index revision file to text directory
    src_file = os.path.join(src_revisions, '{:08d}'.format(max_index))
    dst_file = '{0}.moin'.format(page_filename)
    dst_file = os.path.join(dst_dirs['text'], dst_file)
    subprocess.check_call(['cp', '-n', '-p', src_file, dst_file])
    subprocess.check_call(['diff', src_file, dst_file])


def process_attachments(page_base, dst_page_dirname, dst_dirs):
    """Copy any attachments over."""
    src_attachments = os.path.join(page_base, 'attachments')
    if os.path.isdir(src_attachments):
        attachments = os.listdir(src_attachments)
        if attachments:
            dst_attachments = os.path.join(dst_dirs['attachments'], dst_page_dirname)
            create_directory(dst_attachments)
        for attachment in attachments:
            src_file = os.path.join(src_attachments, attachment)
            subprocess.check_call(['cp', '-n', '-p', src_file, dst_attachments])
            subprocess.check_call(['diff', src_file, dst_attachments])


def main():
    """Extract content from command-line-specified moin src to specified dst directory."""
    src, dst = parse_args()
    dst_dirs = create_subdirectories(dst)
    pages = get_pages(src)
    for page_base, page_filename in pages.iteritems():
        process_page_revisions(page_base, page_filename, dst_dirs)
        process_attachments(page_base, page_filename, dst_dirs)
    print 'Done.'


if __name__ == '__main__':
    main()
