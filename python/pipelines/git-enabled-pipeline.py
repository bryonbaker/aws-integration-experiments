# Note: This pipeline depends upon a secret. Generate it using:
# kubectl create secret generic git-credentials --from-literal=access-token=<YOUR_ACCESS_TOKEN>

import kfp.dsl as dsl
import kfp.components as comp
import kfp.dsl as dsl
import kfp.components as comp
from kubernetes.client import V1Volume, V1VolumeMount
from kfp_tekton.compiler import TektonCompiler
from kfp_tekton.k8s_client_helper import env_from_secret

# Define container ops for module1, module2, and module3
module1_op = comp.load_component_from_url('https://github.com/bryonbaker/rhods-experiments/blob/main/python/pipelines/module1.py')
module2_op = comp.load_component_from_url('https://github.com/bryonbaker/rhods-experiments/blob/main/python/pipelines/module2.py')
module3_op = comp.load_component_from_url('https://github.com/bryonbaker/rhods-experiments/blob/main/python/pipelines/module3.py')

# Define a Kubernetes secret to store the access key/token
access_token_secret = dsl.SecretVolume(name="git-credentials", secret_name="git-credentials")

@dsl.pipeline(
    name="Python Modules Orchestrated Pipeline",
    description="A pipeline to orchestrate three Python modules (module1 and module2 in parallel, followed by module3)."
)
def python_modules_pipeline():
    # Task to run module1
    # Load the secret as a persistent volume into the container.
    module1_task = module1_op().add_pvolumes({"/root/.git-credentials": access_token_secret})

    # Task to run module2
    # Load the secret as a persistent volume into the container.
    module2_task = module2_op().add_pvolumes({"/root/.git-credentials": access_token_secret})

    # Define parallel execution for module1 and module2
    parallel_tasks = [module1_task, module2_task]

    # Task to run module3 after both module1 and module2 complete
    # Load the secret as a persistent volume into the container.
    module3_task = module3_op().add_pvolumes({"/root/.git-credentials": access_token_secret})
    module3_task.after(*parallel_tasks)

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(python_modules_pipeline, "python_modules_pipeline.yaml")
