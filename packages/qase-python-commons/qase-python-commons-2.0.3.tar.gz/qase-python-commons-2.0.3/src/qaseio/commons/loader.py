from qaseio.api_client import ApiClient
from qaseio.configuration import Configuration
from qaseio.api.plans_api import PlansApi
from qaseio.rest import ApiException
import certifi

class TestOpsPlanLoader:
    def __init__(self, api_token, host = 'qase.io'):
        configuration = Configuration()
        configuration.api_key['TokenAuth'] = api_token
        configuration.host = f'https://api.{host}/v1'

        self.client = ApiClient(configuration)
        self.case_list = []

        configuration.ssl_ca_cert = certifi.where()

    def load(self, code: str, plan_id: int) -> list:
        api_instance = PlansApi(self.client)
        try:
            response = api_instance.get_plan(code=code, id=plan_id)
            if hasattr(response, 'result'):
                self.case_list = [c.case_id for c in response.result.cases]
                return self.case_list
            raise ValueError("Unable to find given plan")
        except ApiException as e:
            print("Unable to load test plan data: %s\n" % e)
        return []