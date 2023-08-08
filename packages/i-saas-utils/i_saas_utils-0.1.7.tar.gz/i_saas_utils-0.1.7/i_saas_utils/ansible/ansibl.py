import subprocess


class Ansible:
    @staticmethod
    def run(playbook: str, hosts: str = "", *args, **kwargs):
        if hosts:
            args = ("-i", hosts, *args)

        result = subprocess.run(
            [
                "ansible-playbook",
                playbook,
                *args,
                *(f"{key}={value}" for key, value in kwargs.items()),
            ]
        )

        if result.returncode != 0:
            raise Exception("Error playbook code", result)
        return result
