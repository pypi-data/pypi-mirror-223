from robotcloud.api import APIEndPointAuthenticated


class ApplicationRegisterListAPICall(APIEndPointAuthenticated):
    def __init__(self, token: str):
        super().__init__(token)

    def get_endpoint(self):
        return f"application/register/"


class ApplicationRegisterItemAPICall(APIEndPointAuthenticated):
    def __init__(self, token: str, application_id: str):
        self.application_id = application_id
        super().__init__(token)

    def get_endpoint(self):
        return f"application/register/{self.application_id}"


def create_application(token, data):
    return ApplicationRegisterListAPICall(token).post(data)


def get_applications(token):
    return ApplicationRegisterListAPICall(token).get()


def get_application(token, application_id):
    return ApplicationRegisterItemAPICall(token, application_id).get()


def update_application(token, application_id, data):
    return ApplicationRegisterItemAPICall(token, application_id).put(data)


def delete_application(token, application_id):
    return ApplicationRegisterItemAPICall(token, application_id).delete()
