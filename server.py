from flask import Flask
from flask import request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import timedelta
import json

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class NewsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(500), nullable=False)
    img_src = db.Column(db.String(500), nullable=False)
    #published_date = db.Column(db.String(500), nullable=False)
    #parsed_date = db.Column(db.String(500), nullable=False)
    published_date = db.Column(db.DateTime, nullable=False)
    parsed_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"News(header = {header}, img_src = {img_src}, published_date = {published_date}, parsed_date = {parsed_date})"

#db.create_all()
try:
	db.create_all()
except Exception:
	print("DB is already existed!")

news_put_args = reqparse.RequestParser()
news_put_args.add_argument("header", type=str, help="Header is required", required=True)
news_put_args.add_argument("img_src", type=str, help="Image source is required", required=True)
news_put_args.add_argument("published_date", type=lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'), help="Published date is required", required=True)
news_put_args.add_argument("parsed_date", type=lambda x: datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), help="Parsed date is required", required=True)

news_update_args = reqparse.RequestParser()
news_update_args.add_argument("header", type=str, help="Header is required")
news_update_args.add_argument("img_src", type=str, help="Image source is required")
news_update_args.add_argument("published_date", type=lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'), help="Published date is required")
news_update_args.add_argument("parsed_date", type=lambda x: datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'), help="Parsed date is required")

resource_fields = {
    'id': fields.Integer,
    'header': fields.String,
    'img_src': fields.String,
    'published_date': fields.DateTime,
    'parsed_date': fields.DateTime
}

class News(Resource):
    @marshal_with(resource_fields)
    def get(self, news_id):
        date_days_ago = datetime.datetime.now() - timedelta(days=news_id)
        result = NewsModel.query.filter(NewsModel.published_date <= datetime.datetime.now().strftime('%Y-%m-%d')).filter(NewsModel.published_date >= date_days_ago.strftime('%Y-%m-%d'))
        lst = []
        for elem in result:
            lst.append(elem)

        if not result:
            abort(404, message="Could not find news in this period")
        return lst

    @marshal_with(resource_fields)
    def put(self, news_id):
        args = news_put_args.parse_args()
        result = NewsModel.query.filter_by(id=news_id).first()
        if result:
            abort(409, message="News id taken...")

        news = NewsModel(id=news_id, header=args['header'], img_src=args['img_src'], published_date=args['published_date'], parsed_date=args['parsed_date'])

        db.session.add(news)
        db.session.commit()
        return news, 201

    @marshal_with(resource_fields)
    def patch(self, news_id):
        args = news_update_args.parse_args()
        result = NewsModel.query.filter_by(id=news_id).first()
        if not result:
            abort(404, message="News doesn't exist, cannot update")

        if args['header']:
            result.header = args['header']
        if args['img_src']:
            result.img_src = args['img_src']
        if args['published_date']:
            result.published_date = args['published_date']
        if args['parsed_date']:
            result.parsed_date = args['parsed_date']

        db.session.commit()

        return result


    def delete(self, news_id):
        abort_if_news_id_doesnt_exist(news_id)
        del newses[news_id]
        return '', 204


api.add_resource(News, "/metro/news/<int:news_id>")

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
