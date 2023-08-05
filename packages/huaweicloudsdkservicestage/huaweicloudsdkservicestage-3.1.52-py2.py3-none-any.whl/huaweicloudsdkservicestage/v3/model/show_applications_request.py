# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ShowApplicationsRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'limit': 'int',
        'offset': 'int',
        'order_by': 'str',
        'order': 'str'
    }

    attribute_map = {
        'limit': 'limit',
        'offset': 'offset',
        'order_by': 'order_by',
        'order': 'order'
    }

    def __init__(self, limit=None, offset=None, order_by=None, order=None):
        """ShowApplicationsRequest

        The model defined in huaweicloud sdk

        :param limit: 指定个数，明确指定的时候用于分页，取值[0, 100]。不指定的时候表示不分页，最多查询1000条记录。
        :type limit: int
        :param offset: 指定查询偏移量，默认偏移量为0.
        :type offset: int
        :param order_by: 排序字段，默认按创建时间排序。  排序字段支持枚举值：create_time、name、update_time。 
        :type order_by: str
        :param order: desc/asc，默认desc。
        :type order: str
        """
        
        

        self._limit = None
        self._offset = None
        self._order_by = None
        self._order = None
        self.discriminator = None

        if limit is not None:
            self.limit = limit
        if offset is not None:
            self.offset = offset
        if order_by is not None:
            self.order_by = order_by
        if order is not None:
            self.order = order

    @property
    def limit(self):
        """Gets the limit of this ShowApplicationsRequest.

        指定个数，明确指定的时候用于分页，取值[0, 100]。不指定的时候表示不分页，最多查询1000条记录。

        :return: The limit of this ShowApplicationsRequest.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ShowApplicationsRequest.

        指定个数，明确指定的时候用于分页，取值[0, 100]。不指定的时候表示不分页，最多查询1000条记录。

        :param limit: The limit of this ShowApplicationsRequest.
        :type limit: int
        """
        self._limit = limit

    @property
    def offset(self):
        """Gets the offset of this ShowApplicationsRequest.

        指定查询偏移量，默认偏移量为0.

        :return: The offset of this ShowApplicationsRequest.
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this ShowApplicationsRequest.

        指定查询偏移量，默认偏移量为0.

        :param offset: The offset of this ShowApplicationsRequest.
        :type offset: int
        """
        self._offset = offset

    @property
    def order_by(self):
        """Gets the order_by of this ShowApplicationsRequest.

        排序字段，默认按创建时间排序。  排序字段支持枚举值：create_time、name、update_time。 

        :return: The order_by of this ShowApplicationsRequest.
        :rtype: str
        """
        return self._order_by

    @order_by.setter
    def order_by(self, order_by):
        """Sets the order_by of this ShowApplicationsRequest.

        排序字段，默认按创建时间排序。  排序字段支持枚举值：create_time、name、update_time。 

        :param order_by: The order_by of this ShowApplicationsRequest.
        :type order_by: str
        """
        self._order_by = order_by

    @property
    def order(self):
        """Gets the order of this ShowApplicationsRequest.

        desc/asc，默认desc。

        :return: The order of this ShowApplicationsRequest.
        :rtype: str
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this ShowApplicationsRequest.

        desc/asc，默认desc。

        :param order: The order of this ShowApplicationsRequest.
        :type order: str
        """
        self._order = order

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
        if not isinstance(other, ShowApplicationsRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
