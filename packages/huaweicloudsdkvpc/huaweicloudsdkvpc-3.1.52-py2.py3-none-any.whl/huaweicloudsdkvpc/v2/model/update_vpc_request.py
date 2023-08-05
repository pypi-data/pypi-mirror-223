# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class UpdateVpcRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'vpc_id': 'str',
        'body': 'UpdateVpcRequestBody'
    }

    attribute_map = {
        'vpc_id': 'vpc_id',
        'body': 'body'
    }

    def __init__(self, vpc_id=None, body=None):
        """UpdateVpcRequest

        The model defined in huaweicloud sdk

        :param vpc_id: 虚拟私有云ID
        :type vpc_id: str
        :param body: Body of the UpdateVpcRequest
        :type body: :class:`huaweicloudsdkvpc.v2.UpdateVpcRequestBody`
        """
        
        

        self._vpc_id = None
        self._body = None
        self.discriminator = None

        self.vpc_id = vpc_id
        if body is not None:
            self.body = body

    @property
    def vpc_id(self):
        """Gets the vpc_id of this UpdateVpcRequest.

        虚拟私有云ID

        :return: The vpc_id of this UpdateVpcRequest.
        :rtype: str
        """
        return self._vpc_id

    @vpc_id.setter
    def vpc_id(self, vpc_id):
        """Sets the vpc_id of this UpdateVpcRequest.

        虚拟私有云ID

        :param vpc_id: The vpc_id of this UpdateVpcRequest.
        :type vpc_id: str
        """
        self._vpc_id = vpc_id

    @property
    def body(self):
        """Gets the body of this UpdateVpcRequest.

        :return: The body of this UpdateVpcRequest.
        :rtype: :class:`huaweicloudsdkvpc.v2.UpdateVpcRequestBody`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this UpdateVpcRequest.

        :param body: The body of this UpdateVpcRequest.
        :type body: :class:`huaweicloudsdkvpc.v2.UpdateVpcRequestBody`
        """
        self._body = body

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
        if not isinstance(other, UpdateVpcRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
