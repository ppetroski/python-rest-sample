import logging
import sys
import time
import config
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.orm import joinedload

logger = logging.getLogger(__name__)


# BaseController handles all of the basic functionality provided by CRUD to controllers
class BaseController(Resource):
    _model = None
    _query = None
    _session = None

    def __init__(self):
        # specify connection string from config
        db_driver = config.database.get('driver')
        db_user = config.database.get('user')
        db_pwd = config.database.get('password')
        db_host = config.database.get('host')
        db_port = config.database.get('port')
        db_name = config.database.get('database')

        engine = db.create_engine(
            f'{db_driver}://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}',
            echo=True)
        
        session = db.orm.sessionmaker()
        session.configure(bind=engine)
        self._session = session()

        # automatically filter records that are deleted
        self._query = self._session.query(self._model).filter_by(deleted_at=None)

    def get(self, uuid=None):
        if self._model != None:
            # Return a collection of existing models or a single model.
            if uuid is None:
                return self._paginate()
            else:
                self._query = self._query.filter_by(uuid=uuid)
                return self._paginate()
        else:
            return self._message('The API endpoint has been improperly configured. Please contact support.', 'failure')

    def delete(self, uuid=None):
        if self._model != None:
            if uuid:
                self._query = self._query.filter_by(uuid=uuid)
                data = self._query.first()
                if data and data.id:
                    # I believe in soft deletes, so we'll do an update
                    data.deleted_at = datetime.now()
                    self._session.commit()
                    return self._paginate()
                else:
                    model = type(self._model()).__name__
                    return self._message(f'"{model}" record not found for "{uuid}"', 'failure')
        else:
            return self._message('The API endpoint has been improperly configured. Please contact support.', 'failure')

    def post(self, uuid=None, init=None):
        # Create and save a new model
        try:
            if self._model != None:
                post = request.get_json()
                if uuid:
                    self._query = self._query.filter_by(uuid=uuid)
                    data = self._query.first()
                    if data and data.id:
                        data.load(post)
                    else:
                        model = type(self._model()).__name__
                        return self._message(f'"{model}" record not found for "{uuid}"', 'failure')
                else:
                    data = self._model(post)
                    self._session.add(data)
                self._session.commit()
                return self._paginate()
            else:
                return self._message('The API endpoint has been improperly configured. Please contact support.', 'failure')
        except ValueError as message:
            self._session.rollback()
            self._session.rollback()
            return self._message(str(message), 'failure')
        except:
            self._session.rollback()
            error = ''
            for ele in sys.exc_info():
                error += str(ele)
            logger.error(error)
            return self._message('Unexpected error: ' + str(sys.exc_info()[1]), 'failure')

    def put(self):
        return self.post(self)

    def _paginate(self):
        # include Joins for relations requested via expand parameter
        relations = request.args.getlist('expand')
        for relation in relations:
            if hasattr(self._model, relation):
                self._query = self._query.options(
                    joinedload(getattr(self._model, relation))
                )

        count = self._query.count()

        # Perform Pagination
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per-page', default=25, type=int)
        self._query = self._query.limit(per_page).offset((page-1) * per_page)

        # Query Data and serialize
        data = self._query.all()
        if isinstance(data, list):
            data = [m.serialize(relations) for m in data]
        else:
            data = data.serialize(relations)
        return make_response(jsonify({'status': 'success', 'count': count, 'timestamp': time.time(), 'data': data}))

    @staticmethod
    def _message(data, status='success'):
        if status != 'success':
            if (isinstance(data, str)):
                logger.warning(data)

        return make_response(jsonify({'status': status, 'count': 0, 'timestamp': time.time(), 'data': data}))
