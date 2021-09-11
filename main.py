
from linebotapp import create_app

app = create_app()

@app.cli.command()
def test():
    import unittest
    import sys

    tests = unittest.TestLoader().discover("linebottest")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)

# from argparse import ArgumentParser

# if __name__ == "__main__":
#     arg_parser = ArgumentParser(
#         usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
#     )
#     arg_parser.add_argument('-p', '--port', default=8000, help='port')
#     arg_parser.add_argument('-d', '--debug', default=False, help='debug')
#     options = arg_parser.parse_args()

#     app.run(debug=options.debug, port=options.port)
