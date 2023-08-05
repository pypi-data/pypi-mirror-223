# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListPostgresqlDatabaseSchemasRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'x_language': 'str',
        'instance_id': 'str',
        'db_name': 'str',
        'page': 'int',
        'limit': 'int'
    }

    attribute_map = {
        'x_language': 'X-Language',
        'instance_id': 'instance_id',
        'db_name': 'db_name',
        'page': 'page',
        'limit': 'limit'
    }

    def __init__(self, x_language=None, instance_id=None, db_name=None, page=None, limit=None):
        """ListPostgresqlDatabaseSchemasRequest

        The model defined in huaweicloud sdk

        :param x_language: 语言
        :type x_language: str
        :param instance_id: 实例ID。
        :type instance_id: str
        :param db_name: 数据库名称。
        :type db_name: str
        :param page: 分页页码，从1开始。
        :type page: int
        :param limit: 每页数据条数。取值范围[1, 100]。
        :type limit: int
        """
        
        

        self._x_language = None
        self._instance_id = None
        self._db_name = None
        self._page = None
        self._limit = None
        self.discriminator = None

        if x_language is not None:
            self.x_language = x_language
        self.instance_id = instance_id
        self.db_name = db_name
        self.page = page
        self.limit = limit

    @property
    def x_language(self):
        """Gets the x_language of this ListPostgresqlDatabaseSchemasRequest.

        语言

        :return: The x_language of this ListPostgresqlDatabaseSchemasRequest.
        :rtype: str
        """
        return self._x_language

    @x_language.setter
    def x_language(self, x_language):
        """Sets the x_language of this ListPostgresqlDatabaseSchemasRequest.

        语言

        :param x_language: The x_language of this ListPostgresqlDatabaseSchemasRequest.
        :type x_language: str
        """
        self._x_language = x_language

    @property
    def instance_id(self):
        """Gets the instance_id of this ListPostgresqlDatabaseSchemasRequest.

        实例ID。

        :return: The instance_id of this ListPostgresqlDatabaseSchemasRequest.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ListPostgresqlDatabaseSchemasRequest.

        实例ID。

        :param instance_id: The instance_id of this ListPostgresqlDatabaseSchemasRequest.
        :type instance_id: str
        """
        self._instance_id = instance_id

    @property
    def db_name(self):
        """Gets the db_name of this ListPostgresqlDatabaseSchemasRequest.

        数据库名称。

        :return: The db_name of this ListPostgresqlDatabaseSchemasRequest.
        :rtype: str
        """
        return self._db_name

    @db_name.setter
    def db_name(self, db_name):
        """Sets the db_name of this ListPostgresqlDatabaseSchemasRequest.

        数据库名称。

        :param db_name: The db_name of this ListPostgresqlDatabaseSchemasRequest.
        :type db_name: str
        """
        self._db_name = db_name

    @property
    def page(self):
        """Gets the page of this ListPostgresqlDatabaseSchemasRequest.

        分页页码，从1开始。

        :return: The page of this ListPostgresqlDatabaseSchemasRequest.
        :rtype: int
        """
        return self._page

    @page.setter
    def page(self, page):
        """Sets the page of this ListPostgresqlDatabaseSchemasRequest.

        分页页码，从1开始。

        :param page: The page of this ListPostgresqlDatabaseSchemasRequest.
        :type page: int
        """
        self._page = page

    @property
    def limit(self):
        """Gets the limit of this ListPostgresqlDatabaseSchemasRequest.

        每页数据条数。取值范围[1, 100]。

        :return: The limit of this ListPostgresqlDatabaseSchemasRequest.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListPostgresqlDatabaseSchemasRequest.

        每页数据条数。取值范围[1, 100]。

        :param limit: The limit of this ListPostgresqlDatabaseSchemasRequest.
        :type limit: int
        """
        self._limit = limit

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ListPostgresqlDatabaseSchemasRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
