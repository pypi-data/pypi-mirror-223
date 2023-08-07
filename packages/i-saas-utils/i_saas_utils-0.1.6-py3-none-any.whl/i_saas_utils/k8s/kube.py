from kubernetes import client, config


class Kube:
    config.load_config()

    @staticmethod
    def create_job(uniq_name: str, action: str, data: dict, namespace: str = "default"):
        batch_v1_api = client.BatchV1Api()

        container = client.V1Container(
            name="saas",
            image="my-image",
            env=[client.V1EnvVar(name="SAAS_DATA", value=data)],
            args=[action],
        )

        job_spec = client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(restart_policy="Never", containers=[container])
            )
        )

        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=uniq_name),
            spec=job_spec,
        )

        response = batch_v1_api.create_namespaced_job(body=job, namespace=namespace)

        return response
