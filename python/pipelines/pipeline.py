import kfp
from kfp import dsl
from kfp.dsl import ContainerOp
from kfp.gcp import use_gcp_secret

def run_module1():
    return ContainerOp(
        name="module1",
        image="python:3.8",
        command=["python", "-c", "print('Hello world.')"],
    )

def run_module2():
    return ContainerOp(
        name="module2",
        image="python:3.8",
        command=["python", "-c", "print('I am alive.')"],
    )

@dsl.pipeline(
    name="Python Modules Orchestrated",
    description="A pipeline that orchestrates two Python modules.",
)
def python_modules_pipeline():
    module1_task = run_module1()
    module2_task = run_module2()
    
    module2_task.after(module1_task)

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(python_modules_pipeline, "python_modules_pipeline.yaml")
