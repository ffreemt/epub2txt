"""Convert tmx to epub."""
from pathlib import Path

import logzero
from logzero import logger

# from pyquery import PyQuery as pq
from absl import app, flags

# from tmx2epub.xml_iter import xml_iter
from .browse_filename import browse_filename
from .gen_filename import gen_filename
from .epub2txt import epub2txt

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "filename",
    "",  # browse to file if empty
    "tmx filename (can be gzip or bz2)",
    short_name="f",
)
flags.DEFINE_string(
    "dest",
    "",  # filename dir if empty
    "destintioin folder to save the epub file, if left empty, set to the same folder where tmx file is located",
    short_name="d",
)
flags.DEFINE_boolean(
    "detailed-info",
    False,
    "print more detailed book info and exit",
    short_name="m",
)
flags.DEFINE_boolean("info", False, "print book info and exit", short_name="i")
flags.DEFINE_boolean("debug", False, "print verbose debug messages")
flags.DEFINE_boolean("version", False, "print version and exit", short_name="V")


def proc_argv(_):  # pylint: disable=too-many-branches  # noqa: C901
    """Proc_argv in absl."""
    # version = "0.1.0"

    if FLAGS.version:
        from epub2txt import __version__
        print("tmx2epub %s 20210208, brought to you by mu@qq41947782" % __version__)
        raise SystemExit(0)

    if FLAGS.debug:
        logzero.loglevel(10)  # logging.DEBUG
    else:
        logzero.loglevel(20)  # logging.INFO

    # args = dict((elm, getattr(FLAGS, elm)) for elm in FLAGS)
    logger.debug(
        "\n\t available args: %s", dict((elm, getattr(FLAGS, elm)) for elm in FLAGS)
    )

    # browse to the filename's folder if the file does not exists
    filename = FLAGS.filename
    # if not Path(filename).exists():
    if not Path(filename).is_file():
        try:
            filename = browse_filename(Path(filename))
        except Exception as exc:
            logger.error(exc)
            filename = ""
        logger.debug(" file selected: %s", filename)

    if not filename:
        logger.info("\n\t Operation canceled or no filename provided, unable to proceed, exiting...")
        raise SystemExit(1)

    # filename = getattr(FLAGS, "filename")
    # filename not specified
    if not filename:
        # print("\t **filename not give**n, set to", Path(FLAGS.filename).absolute().parent))
        try:
            filename = browse_filename(Path(filename))
        except Exception as exc:
            logger.error(exc)
            filename = ""
        logger.debug(" file selected: %s", filename)

    FLAGS.filename = filename
    stem = Path(filename).stem
    if not FLAGS.dest:
        destfile = Path(FLAGS.filename).absolute().parent / f"{stem}.txt"
    else:
        destfile = Path(FLAGS.filename).absolute().parent / FLAGS.dest
        logger.debug(" FLAGS.filename: %s, destfle: %s", FLAGS.filename, destfile)

    destfile = gen_filename(destfile)

    FLAGS.dest = destfile
    if Path(FLAGS.dest).suffix not in ["txt"]:
        stem = Path(FLAGS.dest).stem
        FLAGS.dest = Path(FLAGS.dest).parent / f"{stem}.txt"
    FLAGS.dest = str(FLAGS.dest)

    args = ["filename", "dest", "debug"]

    debug = FLAGS.debug
    if debug:
        logger.debug("\n\t args: %s", [[elm, getattr(FLAGS, elm)] for elm in args])

    # raise SystemExit("quit by intention...")

    try:
        text = epub2txt(
            FLAGS.filename,
            debug=FLAGS.debug,
        )
    except Exception as exc:
        logger.error("epub2txt exc: %s", exc)
        raise SystemExit(1)

    if FLAGS.i:
        print(f"""
            {epub2txt.title}
            {epub2txt.toc}""")
        raise SystemExit(0)
    if FLAGS.m:
        print(f"""
            {epub2txt.title}
            {epub2txt.toc}
            {epub2txt.metadata}
            {epub2txt.spine}""")
        raise SystemExit(0)

    logger.debug(" epub generated **%s**", text[:200])

    try:
        Path(FLAGS.dest).write_text(text, encoding="utf8")
    except Exception as exc:
        logger.error("Path(FLAGS.dest).write_text exc: %s", exc)
        raise SystemExit(1)

    logger.info(" epub file: %s", FLAGS.filename)
    logger.info(" text file: %s", FLAGS.dest)


def main():
    """ main. """
    app.run(proc_argv)


if __name__ == "__main__":
    main()
