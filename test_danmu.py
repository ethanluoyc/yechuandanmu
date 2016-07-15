#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
from danmu import initdb, app, db, socketio, Danmaku, STATUS_FLAGS, FeatureFlag
import config


class Test(unittest.TestCase):
    def setUp(self):
        app.config.from_object(config.TestConfig)
        self._app = app
        self.app = app.test_client()
        self.db = db
        with app.app_context():
            initdb()

    def test_post_danmaku(self):
        # Post empty danmaku
        rv = self.app.post('/post', data=dict(message=''))
        assert 'empty' in rv.data

        # Post danmaku that is too long
        rv = self.app.post('/post', data=dict(message='a'*400))
        assert 'max length' in rv.data

        # Post valid danmaku
        res = self.app.post('/post', data=dict(message='abcd'))
        assert 'succeeded' in res.data

    def _post_valid_danmaku(self, msg):
        self.app.post('/post',
                      data=dict(message=msg),
                      headers=[('X-Requested-With',
                                'XMLHttpRequest')])

    def test_post_danmaku_ajax(self):
        res = self.app.post('/post',
                            data=dict(message='abcd'),
                            headers=[('X-Requested-With',
                                      'XMLHttpRequest')])
        import json
        json.loads(res.data)

        res = self.app.post('/post',
                            data=dict(message='abcd'))
        with self.assertRaises(ValueError):
            json.loads(res.data)

    def test_get_post_page(self):
        res = self.app.get('/post')
        assert str(self._app.config['YEAR']) in res.data

    def test_approve_danmaku(self):
        client = socketio.test_client(self._app, namespace='/check')
        self._post_valid_danmaku('test1')  # id should be 1
        assert Danmaku.get_by_id(1).status == STATUS_FLAGS['waiting']

        self._post_valid_danmaku('test2')  # id should be 1
        msgs = client.get_received('/check')
        assert len(msgs) == 2

        approved_dmk = msgs[0]['args'][0]
        client.emit('approve danmu', approved_dmk, json=True, namespace='/check')
        assert Danmaku.get_by_id(1).status == STATUS_FLAGS['approved']

    def test_disapprove_danmaku(self):
        client = socketio.test_client(self._app, namespace='/check')
        self._post_valid_danmaku('test1')  # id should be 1
        assert Danmaku.get_by_id(1).status == STATUS_FLAGS['waiting']

        msgs = client.get_received('/check')

        dmk = msgs[0]['args'][0]
        client.emit('disprove danmu', dmk, json=True, namespace='/check')
        assert Danmaku.get_by_id(1).status == STATUS_FLAGS['disproved']

    def test_bypass_with_supervise_off(self):
        # Feature flag should be toggled
        client = socketio.test_client(self._app, namespace='/check')
        FeatureFlag.toggle_flag('supervise', status=False)
        assert FeatureFlag.get_flag('supervise').status == False

        self._post_valid_danmaku('test1')  # id should be 1
        assert Danmaku.get_by_id(1).status == STATUS_FLAGS['approved']

        # TODO this needs to be investigated, it should not have any msgs
        # msgs = client.get_received('/check')
        # assert len(msgs) == 0


    # TODO
    def test_bypass_with_master(self):
        pass

    def test_get_board(self):
        recv = self.app.get('/')
        assert 'with' in recv.data

    def tearDown(self):
        self.db.drop_all()


if __name__ == '__main__':
    print "Running with arguments: {0}".format(sys.argv[1:])
    try:
        import pytest
    except ImportError:
        unittest.main(sys.argv)
    else:
        pytest.main(sys.argv)
