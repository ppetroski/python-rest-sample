import logging
import sys
import time

from sqlalchemy.orm import joinedload

import config
import sqlalchemy as db
from datetime import datetime
from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.orm.attributes import InstrumentedAttribute

logger = logging.getLogger(__name__)


# BaseController handles all of the basic functionality provided by CRUD to controllers
class BaseController(Resource):
    _model = None
    _query = None
    _session = None
    _relations = []

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
                return self._prepare()
            else:
                self._query = self._query.filter_by(uuid=uuid)
                return self._prepare()
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
                    return self._prepare()
                else:
                    model = type(self._model()).__name__
                    return self._message(f'"{model}" record not found for "{uuid}"', 'failure')
        else:
            return self._message('The API endpoint has been improperly configured. Please contact support.', 'failure')

    def post(self, uuid=None):
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
                    model = type(self._model()).__name__
                    return self._message(f'Please use the correct method to create a "{model}" record', 'failure')
                self._session.commit()
                return make_response(jsonify({'status': 'success', 'count': 1, 'timestamp': time.time(), 'data': data.serialize()}))
            else:
                return self._message('The API endpoint has been improperly configured. Please contact support.',
                                     'failure')
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

    def put(self, uuid=None):
        # Create and save a new model
        try:
            if self._model != None:
                post = request.get_json()
                if uuid:
                    model = type(self._model()).__name__
                    return self._message(f'Please use the correct method to update the "{model}" record for "{uuid}"', 'failure')
                else:
                    data = self._model(post)
                    self._session.add(data)
                self._session.commit()
                return make_response(jsonify({'status': 'success', 'count': 1, 'timestamp': time.time(), 'data': data.serialize()}))
            else:
                return self._message('The API endpoint has been improperly configured. Please contact support.',
                                     'failure')
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

    def _prepare(self):
        expand = self._expand()
        # join must called be after expand, filter and sort as that builds join table list
        self._filter()._sort()._join()
        count = self._query.count()

        # Query Data and serialize output to JSON
        data = self._paginate()._query.all()
        if isinstance(data, list):
            data = [m.serialize(expand) for m in data]
        else:
            data = data.serialize(expand)
        return make_response(jsonify({'status': 'success', 'count': count, 'timestamp': time.time(), 'data': data}))

    def _expand(self):
        expand = []
        params = request.args.getlist('expand')
        # let's process params  as an array
        for param in params:
            # if value is comma separated, let's process each of them as a param
            relations = param.split(',')
            for relation in relations:
                relation = relation.strip()
                expand.append(relation)
                if hasattr(self._model, relation):
                    rel = getattr(self._model, relation)
                    # if a table, include Joins for relationship
                    if isinstance(rel, InstrumentedAttribute):
                        if rel not in self._relations:
                            self._relations.append(rel)
        return expand

    def _filter(self):
        rel = ""
        if rel and rel not in self._relations:
            self._relations.append(rel)
        return self

    def _join(self):
        for relation in self._relations:
            if relation:
                self._query = self._query.outerjoin(relation).options(
                            joinedload(relation)
                        )
        return self

    def _sort(self):
        b_desc = False
        param = request.args.get('sort', default=None, type=str)
        if not param:
            return self

        if param.startswith('-'):
            b_desc = True
            param = param[1:]

        namespace = param.split('.')
        sort = self._model
        if len(namespace) == 1:
            sort = getattr(sort, namespace[0])
        else:
            for elem in param.split('.'):
                if hasattr(sort, elem):
                    sort = getattr(sort, elem)
                    if isinstance(sort, InstrumentedAttribute):
                        if sort not in self._relations:
                            self._relations.append(sort)
                else:
                    sort = getattr(sort.property.mapper.class_, elem)

        if b_desc:
            self._query = self._query.order_by(sort.desc())
        else:
            self._query = self._query.order_by(sort)

        return self

    def _paginate(self):
        # Perform Pagination
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per-page', default=25, type=int)
        self._query = self._query.limit(per_page).offset((page - 1) * per_page)
        return self

    @staticmethod
    def _message(data, status='success'):
        if status != 'success':
            if (isinstance(data, str)):
                logger.warning(data)

        return make_response(jsonify({'status': status, 'count': 0, 'timestamp': time.time(), 'data': data}))
