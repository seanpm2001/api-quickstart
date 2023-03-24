from api_object import ApiObject

from pinterest.ads.campaigns import Campaign
from pinterest.ads.ad_groups import AdGroup
from pinterest.ads.ads import Ad


class Advertisers(ApiObject):
    def __init__(self, _user_id, api_config, access_token):
        super().__init__(api_config, access_token)

    # https://developers.pinterest.com/docs/api/v5/#operation/ad_accounts/list
    def get(self, query_parameters=None):
        """
        Get the advertisers shared with the specified user_id.
        """
        return self.get_iterator("/v5/ad_accounts", query_parameters)

    @classmethod
    def summary(cls, element, kind):
        """
        Return a string with a summary of an element returned by this module.
        """
        id = cls.field(element, 'id')
        name = cls.field(element, 'name')
        summary = f"{kind} ID: {id} | Name: {name}"
        status = cls.field(element, 'status')
        if status:
            summary += f" ({status})"
        return summary

    @classmethod
    def print_summary(cls, element, kind):
        """
        Prints the summary of an object returned by this module.
        Similar to print_summary for other classes.
        """
        print(cls.summary(element, kind))

    @classmethod
    def print_enumeration(cls, data, kind):
        """
        Print a numbered list of elements returned by this module.
        """
        for idx, element in enumerate(data):
            summary = f"[{idx+1}] {cls.summary(element, kind)}"
            print(summary)

    # https://developers.pinterest.com/docs/api/v5/#operation/campaigns/list
    def get_campaigns(self, ad_account_id, query_parameters=None):
        """
        Get the campaigns associated with an Ad Account.
        """
        """
        return self.get_iterator(
            f"/v5/ad_accounts/{ad_account_id}/campaigns", query_parameters
        )
        """
        qp = dict(query_parameters or {})
        qp["ad_account_id"] = ad_account_id
        qp["client"] = self.access_token.sdk_client
        return self.get_sdk_iterator(Campaign.get_all, qp)

    # https://developers.pinterest.com/docs/api/v5/#operation/ad_groups/listp
    def get_ad_groups(self, ad_account_id, campaign_id, query_parameters=None):
        """
        Get the ad groups associated with an Ad Account and Campaign.
        """
        """
        return self.get_iterator(
            f"/v5/ad_accounts/{ad_account_id}/ad_groups?campaign_ids={campaign_id}",
            query_parameters,
        )
        """
        qp = dict(query_parameters or {})
        qp["ad_account_id"] = ad_account_id
        qp["campaign_ids"] = [campaign_id]
        qp["client"] = self.access_token.sdk_client
        return self.get_sdk_iterator(AdGroup.get_all, qp)

    # https://developers.pinterest.com/docs/api/v5/#operation/ads/list
    def get_ads(self, ad_account_id, campaign_id, ad_group_id, query_parameters=None):
        """
        Get the ads associated with an Ad Account, Campaign, and Ad Group.
        """
        """
        return self.get_iterator(
            f"/v5/ad_accounts/{ad_account_id}/ads"
            f"?campaign_ids={campaign_id}&ad_group_ids={ad_group_id}",
            query_parameters,
        )
        """
        qp = dict(query_parameters or {})
        qp["ad_account_id"] = ad_account_id
        qp["campaign_ids"] = [campaign_id]
        qp["ad_group_ids"] = [ad_group_id]
        qp["client"] = self.access_token.sdk_client
        return self.get_sdk_iterator(Ad.get_all, qp)