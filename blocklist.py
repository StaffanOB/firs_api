'''
BLOCK LIST

    This file contains the bloklist of JWT tokens. It will be imported by the
    app and the logout resourdce so that tokens can be added to the blocklist
    when the user logs out.

    # TODO:  <18-10-23, sob> #
    # add this list to a database or a redise server
'''

BLOCKLIST = set()
