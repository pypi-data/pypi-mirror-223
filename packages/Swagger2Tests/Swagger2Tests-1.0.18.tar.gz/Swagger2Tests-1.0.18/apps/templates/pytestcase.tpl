import pytest
from apps.constants.base_constants import *
import requests
import logging
import json

class {{ pytestCaseName }}Case:

    @staticmethod
    def {{ swaggerPathObject.operationId }}():
        # {{ swaggerPathObject.summary }}
        requestUrl = BASE_URL+'{{ swaggerPathObject.url }}'
        {% for obj in parameters -%}
            {% if obj['in'] == 'body' -%}
        requestBody = {
            "appid": REQUEST_APPID,
            "bizContent": {{ obj.params.bizContent }},
            "sign": "string",
            "timestamp": Helper.get_random_datetime()
        }
        sign: str
        sign = Helper.generate_sign(requestBody.copy(), REQUEST_SECRECT)
        requestBody.update({"sign": sign})
            {% endif -%}
        {% endfor %}
        logging.info("请求数据: url %s 参数 %s" % (requestUrl,json.dumps(requestBody)))
        response = requests.post(requestUrl, json= requestBody)
        logging.info("请求返回: %s" % (response.content.decode("utf-8")))
        assert response.status_code == 200
        assert response.json()["ret"] == 0
        return response
        
