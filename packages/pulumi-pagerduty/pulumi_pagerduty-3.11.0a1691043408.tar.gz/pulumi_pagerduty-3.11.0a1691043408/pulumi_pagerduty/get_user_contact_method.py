# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetUserContactMethodResult',
    'AwaitableGetUserContactMethodResult',
    'get_user_contact_method',
    'get_user_contact_method_output',
]

@pulumi.output_type
class GetUserContactMethodResult:
    """
    A collection of values returned by getUserContactMethod.
    """
    def __init__(__self__, address=None, blacklisted=None, country_code=None, device_type=None, enabled=None, id=None, label=None, send_short_email=None, type=None, user_id=None):
        if address and not isinstance(address, str):
            raise TypeError("Expected argument 'address' to be a str")
        pulumi.set(__self__, "address", address)
        if blacklisted and not isinstance(blacklisted, bool):
            raise TypeError("Expected argument 'blacklisted' to be a bool")
        pulumi.set(__self__, "blacklisted", blacklisted)
        if country_code and not isinstance(country_code, int):
            raise TypeError("Expected argument 'country_code' to be a int")
        pulumi.set(__self__, "country_code", country_code)
        if device_type and not isinstance(device_type, str):
            raise TypeError("Expected argument 'device_type' to be a str")
        pulumi.set(__self__, "device_type", device_type)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if label and not isinstance(label, str):
            raise TypeError("Expected argument 'label' to be a str")
        pulumi.set(__self__, "label", label)
        if send_short_email and not isinstance(send_short_email, bool):
            raise TypeError("Expected argument 'send_short_email' to be a bool")
        pulumi.set(__self__, "send_short_email", send_short_email)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_id and not isinstance(user_id, str):
            raise TypeError("Expected argument 'user_id' to be a str")
        pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter
    def address(self) -> str:
        """
        The "address" to deliver to: `email`, `phone number`, etc., depending on the type.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter
    def blacklisted(self) -> bool:
        """
        If true, this phone has been blacklisted by PagerDuty and no messages will be sent to it. (Phone and SMS contact methods only.)
        """
        return pulumi.get(self, "blacklisted")

    @property
    @pulumi.getter(name="countryCode")
    def country_code(self) -> int:
        """
        The 1-to-3 digit country calling code. (Phone and SMS contact methods only.)
        """
        return pulumi.get(self, "country_code")

    @property
    @pulumi.getter(name="deviceType")
    def device_type(self) -> str:
        """
        Either `ios` or `android`, depending on the type of the device receiving notifications. (Push notification contact method only.)
        """
        return pulumi.get(self, "device_type")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        If true, this phone is capable of receiving SMS messages. (Phone and SMS contact methods only.)
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def label(self) -> str:
        """
        The label (e.g., "Work", "Mobile", "Ashley's iPhone", etc.).
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter(name="sendShortEmail")
    def send_short_email(self) -> bool:
        """
        Send an abbreviated email message instead of the standard email output. (Email contact method only.)
        """
        return pulumi.get(self, "send_short_email")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the found contact method. May be (`email_contact_method`, `phone_contact_method`, `sms_contact_method`, `push_notification_contact_method`).
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> str:
        return pulumi.get(self, "user_id")


class AwaitableGetUserContactMethodResult(GetUserContactMethodResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserContactMethodResult(
            address=self.address,
            blacklisted=self.blacklisted,
            country_code=self.country_code,
            device_type=self.device_type,
            enabled=self.enabled,
            id=self.id,
            label=self.label,
            send_short_email=self.send_short_email,
            type=self.type,
            user_id=self.user_id)


def get_user_contact_method(label: Optional[str] = None,
                            type: Optional[str] = None,
                            user_id: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserContactMethodResult:
    """
    Use this data source to get information about a specific [contact method](https://developer.pagerduty.com/api-reference/b3A6Mjc0ODIzOQ-list-a-user-s-contact-methods) of a PagerDuty [user](https://developer.pagerduty.com/api-reference/b3A6Mjc0ODIzMw-list-users) that you can use for other PagerDuty resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    me = pagerduty.get_user(email="me@example.com")
    phone_push = pagerduty.get_user_contact_method(user_id=me.id,
        type="push_notification_contact_method",
        label="iPhone (John)")
    low_urgency_sms = pagerduty.UserNotificationRule("lowUrgencySms",
        user_id=me.id,
        start_delay_in_minutes=5,
        urgency="high",
        contact_method={
            "type": "push_notification_contact_method",
            "id": phone_push.id,
        })
    ```


    :param str label: The label (e.g., "Work", "Mobile", "Ashley's iPhone", etc.).
    :param str type: The contact method type. May be (`email_contact_method`, `phone_contact_method`, `sms_contact_method`, `push_notification_contact_method`).
    :param str user_id: The ID of the user.
    """
    __args__ = dict()
    __args__['label'] = label
    __args__['type'] = type
    __args__['userId'] = user_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('pagerduty:index/getUserContactMethod:getUserContactMethod', __args__, opts=opts, typ=GetUserContactMethodResult).value

    return AwaitableGetUserContactMethodResult(
        address=pulumi.get(__ret__, 'address'),
        blacklisted=pulumi.get(__ret__, 'blacklisted'),
        country_code=pulumi.get(__ret__, 'country_code'),
        device_type=pulumi.get(__ret__, 'device_type'),
        enabled=pulumi.get(__ret__, 'enabled'),
        id=pulumi.get(__ret__, 'id'),
        label=pulumi.get(__ret__, 'label'),
        send_short_email=pulumi.get(__ret__, 'send_short_email'),
        type=pulumi.get(__ret__, 'type'),
        user_id=pulumi.get(__ret__, 'user_id'))


@_utilities.lift_output_func(get_user_contact_method)
def get_user_contact_method_output(label: Optional[pulumi.Input[str]] = None,
                                   type: Optional[pulumi.Input[str]] = None,
                                   user_id: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserContactMethodResult]:
    """
    Use this data source to get information about a specific [contact method](https://developer.pagerduty.com/api-reference/b3A6Mjc0ODIzOQ-list-a-user-s-contact-methods) of a PagerDuty [user](https://developer.pagerduty.com/api-reference/b3A6Mjc0ODIzMw-list-users) that you can use for other PagerDuty resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    me = pagerduty.get_user(email="me@example.com")
    phone_push = pagerduty.get_user_contact_method(user_id=me.id,
        type="push_notification_contact_method",
        label="iPhone (John)")
    low_urgency_sms = pagerduty.UserNotificationRule("lowUrgencySms",
        user_id=me.id,
        start_delay_in_minutes=5,
        urgency="high",
        contact_method={
            "type": "push_notification_contact_method",
            "id": phone_push.id,
        })
    ```


    :param str label: The label (e.g., "Work", "Mobile", "Ashley's iPhone", etc.).
    :param str type: The contact method type. May be (`email_contact_method`, `phone_contact_method`, `sms_contact_method`, `push_notification_contact_method`).
    :param str user_id: The ID of the user.
    """
    ...
