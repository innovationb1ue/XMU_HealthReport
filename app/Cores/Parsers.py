from flask_restplus import reqparse

apply_parser = reqparse.RequestParser()
# apply_parser.add_argument()
apply_parser.add_argument('username')
apply_parser.add_argument('password')
apply_parser.add_argument('N', int)
apply_parser.add_argument('timed')






