import re
import logging

def parse_title(string, incl_ser=True, incl_ep=True):
    """
    Returns a dictionary with series information parsed from string:

    ser_title: series title
    ser_no:    series number
    ep_no:     episode number
    ep_title:  episode title
    name: suggested name for renaming (see below)

    Try to create a name as suggestion for renaming. Hereby, the
    format 0x00 will be transformed into S00E00:

    <ser_title> - S<ser_no>E<ep_no> - <ep_title>

    incl_ser: include series title in name (default: True)
    incl_ep: include episode title in name (default: True)

    Seperators automatically will be omitted if one of the incl
    parameters is set to False.
    """

    FULL_PATTERN = re.compile(r"""
                                (.*?)       # Group 1: Series Title
                                [S]*        # Series Prefix (S)
                                (\d+)       # Group 2: Series No.
                                [Ex]{1}     # Episode Prefix (E/x)
                                (\d+)       # Group 3: Episode No.
                                (.*)        # Group 4: Episode Title
                                """, re.UNICODE | re.I | re.VERBOSE)

    # check if string match FULL_PATTERN
    r = FULL_PATTERN.search(string)

    if not r:

        logging.warning(f"{string}: no pattern detected.")

    else:
        logging.info("MATCH: {r}")

        # extract parts
        ser_title = r.group(1).replace('.', ' ').strip('- ')
        ser_no = f"{int(r.group(2)):02}"
        ep_no = f"{int(r.group(3)):02}"
        ep_title = r.group(4).replace('.', ' ').strip('- ')

        # create new filename
        if incl_ser and ser_title:
            ser_title_sep = f"{ser_title} - "
        else:
            ser_title_sep = ""
        if incl_ep and ep_title:
            sep_ep_title = f" - {ep_title}"
        else:
            sep_ep_title = ""
        name = f"{ser_title_sep}S{ser_no}E{ep_no}{sep_ep_title}"

        return {'ser_title': ser_title,
                'ser_no': ser_no,
                'ep_no': ep_no,
                'ep_title': ep_title,
                'name': name}
