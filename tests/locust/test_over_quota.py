from locust import HttpUser, task, constant, LoadTestShape, TaskSet


class UserTasks(TaskSet):
    @task
    def hit_endpoint(self):
        with self.client.get("/_ping") as response:
            if (response.status_code == "429"):
                raise AssertionError("Unexpected 429")


class WebsiteUser(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]


class OverQuotaLoadShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 30, "spawn_rate": 20},
        {"duration": 120, "users": 90, "spawn_rate": 30},
        {"duration": 240, "users": 30, "spawn_rate": 10}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None