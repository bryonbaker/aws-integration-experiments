import kfp.dsl as dsl
import kfp.components as comp

# Define container ops for module1, module2, and module3
module1_op = comp.load_component_from_url('https://raw.githubusercontent.com/your-username/repo-name/master/module1.py')
module2_op = comp.load_component_from_url('https://raw.githubusercontent.com/your-username/repo-name/master/module2.py')
module3_op = comp.load_component_from_url('https://raw.githubusercontent.com/your-username/repo-name/master/module3.py')

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
