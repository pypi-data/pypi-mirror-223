import json
from datetime import datetime, timedelta
from typing import Dict, Any, Literal, Optional, Union

import backoff
from arcane.core.exceptions import GOOGLE_EXCEPTIONS_TO_RETRY
from google.cloud.tasks_v2 import CloudTasksClient, CreateTaskRequest, Task, HttpRequest, OAuthToken, OidcToken
from google.protobuf import duration_pb2, timestamp_pb2
from google.oauth2 import service_account


class Client(CloudTasksClient):
    def __init__(self, adscale_key: str, project: str):
        self.project = project
        self.credentials = service_account.Credentials.from_service_account_file(
            adscale_key)
        self.adscale_key = adscale_key
        super().__init__(credentials=self.credentials)

    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def publish_task(self,
                     queue: str,
                     method: str = "POST",
                     queue_region: str = "europe-west1",
                     url: Optional[str] = None,
                     # if rounded to the closest second. If not precised, use cloud task default value
                     max_response_time: Optional[timedelta] = None,
                     task_name: Optional[str] = None,
                     body: Optional[Union[Dict[str, Any], str, int]] = None,
                     raw_body: Optional[bytes] = None,
                     schedule_time: Optional[datetime] = None,
                     auth_method: Literal['oidc', 'oauth'] = 'oidc'
                     ) -> Task:
        _task_queue = self.queue_path(
            project=self.project, location=queue_region, queue=queue)
        with open(self.adscale_key) as _credentials_file:
            _credentials = json.load(_credentials_file)
        _client_email = _credentials['client_email']
        http_request = HttpRequest(
            http_method=method,
            url=url,
            headers={'Content-Type': "application/json"}
        )

        if auth_method == 'oidc':
            http_request.oidc_token = OidcToken(
                service_account_email=_client_email)
        elif auth_method == 'oauth':
            http_request.oauth_token = OAuthToken(
                service_account_email=_client_email)

        if body is not None:
            if raw_body is not None:
                raise ValueError(
                    "either body or raw_body should be specified, not both at ")

            http_request.body = json.dumps(body).encode('utf-8')
        elif raw_body is not None:
            http_request.body = raw_body

        task = Task(http_request=http_request)
        if max_response_time is not None:
            task.dispatch_deadline = duration_pb2.Duration(
                seconds=max_response_time.seconds)
        if task_name:
            task.name = self.task_path(
                self.project, queue_region, queue, task_name)
        if schedule_time:
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(schedule_time)

            task.schedule_time = timestamp
        created_task = self.create_task(
            request=CreateTaskRequest(parent=_task_queue, task=task)
        )
        print(f'Queuing task: {created_task.name}')
        return created_task
