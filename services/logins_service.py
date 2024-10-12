from services.base_service import BaseService


class LoginsService(BaseService):
    prefix: str = "logins"

    def credentials(self):
        endpoint = "credentials"
        return self.fetch_data(endpoint)

    def commit_credentials(self, data):
        endpoint = "credentials_commit"
        return self.post_data(endpoint, data={"credentials": data})
