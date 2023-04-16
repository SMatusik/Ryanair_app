from dataclasses import dataclass
from pprint import pprint
from messente_api import OmnimessageApi, SMS, Omnimessage
from messente_api.rest import ApiException


@dataclass
class MessenteService:
    api: OmnimessageApi
    sender: str
    to: str

    def send_alert(self, price: float) -> None:
        sms = SMS(sender=self.sender, text=f"Price is now lower and it's {price}")
        omnimessage = Omnimessage(messages=tuple([sms]), to=self.to)

        try:
            response = self.api.send_omnimessage(omnimessage)
            for message in response.messages:
                pprint(message)

        except ApiException as exception:
            print("Exception when sending an omnimessage: %s\n" % exception)
