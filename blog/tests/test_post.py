# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

import unittest.mock

from django.test import TestCase
import os
import pytest
from unittest.mock import Mock, patch
from blog.utils import ProductionClass
from mock import MagicMock

import json
from django.contrib.auth.models import User

class ClientRequest:
    def __init__(self, client):
        self.client = client

    def __call__(self, type, url, data=None):
        content_type = "application/json"

        if type == "get":
            res = self.client.get(
                url, {}, content_type=content_type
            )
        elif type == "post":
            res = self.client.post(
                url,
                json.dumps(data),
                content_type=content_type
            )
        elif type == "del":
            res = self.client.delete(
                url, {}, content_type=content_type
            )
        else:
            res = self.client.put(
                url,
                json.dumps(data),
                content_type=content_type
            )
        return res



@patch('blog.utils.ProductionClass.foo')
def test_patch(mock_foo):
    mock_foo.return_value = 'mocked return value'
    pc = ProductionClass()
    return pc.foo(10)


class TestView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.c = ClientRequest(self.client)
        # 유저 더미 생성
        self.password = "password"
        self.user = User.objects.create_user(
            username='uiandwe',
            email='uiandwe@test.com',
            password=self.password,
        )
        self.user.set_password(self.password)
        self.user.save()

        url = '/api/auth/'
        res = self.client.post(
            url,
            json.dumps({"username": "uiandwe", "password": "password"}),
            content_type="application/json"
        )
        self.token = res.data['token']

    def test_run_process_case_success(self):

        thing = ProductionClass()

        self.assertEqual(thing.foo(2), 4)

        mock_foo = Mock(thing.foo, return_value='text')
        self.assertEqual(mock_foo(2), 'text')
        self.assertEqual(mock_foo(100), 'text')

        mock_side_effect = Mock(thing.foo, return_value='text', side_effect=Exception('error'))
        with pytest.raises(Exception) as e:
            mock_side_effect(2)
            assert "error" in str(e)

        thing.method = MagicMock(return_value=3)
        thing.method(3, 4, 5, key='value')

        thing.method.assert_called_with(3, 4, 5, key='value')
        self.assertEqual(thing.method(), 3)
        self.assertNotEqual(thing.method(), 0)

    def test_patch_result(self):
        assert test_patch() == 'mocked return value'
        pc = ProductionClass()
        assert pc.foo(2) == 4

    def test_post_token_error(self):
        url = "/api/v1/post/"
        res = self.client.get(
            url, {}, content_type="application/json"
        )

        assert res.status_code == 401

    def test_post_get_success(self):
        url = "/api/v1/post/"
        http_author = 'Token {}'.format(self.token)
        res = self.client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200
        assert res.data['results'] == []

    def test_post_create_success(self):
        url = "/api/v1/post/"
        http_author = 'Token {}'.format(self.token)
        res = self.client.post(
            url, json.dumps({"message": "message 1"}), content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 201
        assert res.data['id'] == 1
        assert res.data['message'] == "message 1"

        res = self.client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )

        assert res.status_code == 200

        assert res.data['results'][0]['message'] == "message 1"
        assert res.data['results'][0]['owner'] == "uiandwe"


