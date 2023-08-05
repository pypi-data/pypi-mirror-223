from datetime import timedelta

from azure.mgmt.security import SecurityCenter
from pydantic import BaseModel

from prowler.lib.logger import logger
from prowler.providers.azure.lib.service.service import AzureService


########################## Defender
class Defender(AzureService):
    def __init__(self, audit_info):
        super().__init__(__class__.__name__, audit_info)

        self.clients = self.__set_clients__(
            audit_info.identity.subscriptions, audit_info.credentials
        )
        self.pricings = self.__get_pricings__()

    def __set_clients__(self, subscriptions, credentials):
        clients = {}
        try:
            for display_name, id in subscriptions.items():
                clients.update(
                    {
                        display_name: SecurityCenter(
                            credential=credentials, subscription_id=id
                        )
                    }
                )
        except Exception as error:
            logger.error(
                f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}]: {error}"
            )
        else:
            return clients

    def __get_pricings__(self):
        logger.info("Defender - Getting pricings...")
        pricings = {}
        for subscription, client in self.clients.items():
            try:
                pricings_list = client.pricings.list()
                pricings.update({subscription: {}})
                for pricing in pricings_list.value:
                    pricings[subscription].update(
                        {
                            pricing.name: Defender_Pricing(
                                resource_id=pricing.id,
                                pricing_tier=pricing.pricing_tier,
                                free_trial_remaining_time=pricing.free_trial_remaining_time,
                            )
                        }
                    )
            except Exception as error:
                logger.error(f"Subscription name: {subscription}")
                logger.error(
                    f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}]: {error}"
                )
        return pricings


class Defender_Pricing(BaseModel):
    resource_id: str
    pricing_tier: str
    free_trial_remaining_time: timedelta
