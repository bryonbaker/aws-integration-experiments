import kfp.dsl as dsl
import kfp.components as comp

# Define container ops for module1, module2, and module3
module1_op = comp.load_component_from_url('https://raw.githubusercontent.com/bryonbaker/rhods-experiments/main/python/pipelines/module1.py?token=GHSAT0AAAAAACBNBHNAY3JC6LSTKCES32Y6ZF6PS5Q')
module2_op = comp.load_component_from_url('https://raw.githubusercontent.com/bryonbaker/rhods-experiments/main/python/pipelines/module2.py?token=GHSAT0AAAAAACBNBHNBDPXKNWXYM66EN7SEZF6PTVA')
module3_op = comp.load_component_from_url('https://raw.githubusercontent.com/bryonbaker/rhods-experiments/main/python/pipelines/module3.py?token=GHSAT0AAAAAACBNBHNBAHDZG25QVTX4HLUGZF6PUEQ')

@dsl.pipeline(
    name="Python Modules Orchestrated Pipeline",
    description="A pipeline to orchestrate three Python modules (module1 and module2 in parallel, followed by module3)."
)
def python_modules_pipeline():
    # Task to run module1
    module1_task = module1_op()

    # Task to run module2
    module2_task = module2_op()

    # Define parallel execution for module1 and module2
    parallel_tasks = [module1_task, module2_task]

    # Task to run module3 after both module1 and module2 complete
    module3_task = module3_op()
    module3_task.after(*parallel_tasks)

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(python_modules_pipeline, "python_modules_pipeline.yaml")
