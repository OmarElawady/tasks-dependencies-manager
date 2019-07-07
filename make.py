from functools import reduce
class Task:
    """A class to keep track of the task's command and dependencies"""
    def __init__(self, dependencies, command):
        """Base for Task class
        
        Arguments:
            dependecies {list[str]} -- list of tasks names that the task depends on
            
            command {str} -- the command associated with the task
        """
        self.dependencies = dependencies
        self.command = command
    def get_dependencies(self):
        """Getter for dependencies"""
        return self.dependencies
    def get_command(self):
        """Getter for command"""
        return self.command
class Make:
    """A class to maintain apps and their depndencies"""
    def __init__(self):
        """Base for Make class
        
        tasks {dict} -- a dict of tasks that is maintained by the class
        """
        self.tasks = {}
    def add_task(self, name, dependencies, command):
        """Adds a new task

        Arguments:
            name {str} -- A descriptive name of the task

            dependencies {list[str]} -- The names of the tasks that it depends on
            command {str} -- The command to be executed to run the task
        """
        self.tasks[name] = Task(dependencies, command)
    def run_task(self, task_name):
        """Prints the commands to run the given task or reports that a cycle occued
        
        Arguments:
            task_name {str} -- the task to be executed
        """
        self.vis = {""}
        self.commands = []
        self.parent = {}
        result = self.traverse_depends(task_name)
        if result != None:
            self.print_cycle(result)
        else:
            print(reduce(lambda x, y: x + y + '\n', self.commands, ""))
    def traverse_depends(self, task_name):
        """Execute all the dependencies of the given task before it
        
        Arguments:
            task_name {str} -- the name of the task

        Returns:
            one of:
                
                None -- If the depencies are traversed correctly

                str  -- If a cycle is detected, a task in the cycle is returned.
        """
        ds = self.tasks[task_name].get_dependencies()
        com = self.tasks[task_name].get_command()
        self.vis.add(task_name)
        for d in ds:
            self.parent[d] = task_name
            if d in self.vis:
                return d
            else:
                x = self.traverse_depends(d)
                if x != None:
                    return x
        self.commands.append(com)

    def print_cycle(self, node):
        """Print the cycle in which the node is in

        node {str} -- the name of a task in the cycle
        """
        print("The tasks:")
        current = self.parent[node]
        print(node)
        while current != node:
            print(current)
            current = self.parent[current]
        print("forms a cycle")
    def print_out_to_string(self, task):
        import sys
        from io import StringIO
        result = StringIO()
        sys.stdout = result
        self.run_task(task)
        sys.stdout = sys.__stdout__
        return result.getvalue()
if __name__ == "__main__":
    print("Normal usage:")
    b = Make()
    b.add_task("publish", ["build-release"], "print publish")
    b.add_task("build-release", ["nim-installed"], "print exec command to build release mode")
    b.add_task("nim-installed", ["curl-installed"], "print curl LINK | bash")
    b.add_task("curl-installed", ["apt-installed"], "apt-get install curl")
    b.add_task("apt-installed", [], "code to install apt...")
    b.run_task("publish")

    print("Cyclic dependencies:")
    b = Make()
    b.add_task("publish", ["build-release"], "print publish")
    b.add_task("build-release", ["nim-installed"], "print exec command to build release mode")
    b.add_task("nim-installed", ["curl-installed"], "print curl LINK | bash")
    b.add_task("curl-installed", ["publish", "apt-installed"], "apt-get install curl")
    b.add_task("apt-installed", [], "code to install apt...")
    b.run_task("publish")
    
