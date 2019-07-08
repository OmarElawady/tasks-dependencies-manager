import pytest
import make

@pytest.fixture
def task():
    return make.Task(["apt", "report", "publish"], "say hello")

def test_get_dependcies(task):
    assert task.get_dependencies() == ["apt", "report", "publish"], "get the depencies of the task"

def test_get_command(task):
    assert task.get_command() == "say hello", "get the command of the task"

@pytest.fixture
def normal_task_list():
    x = make.Make()
    x.add_task("a", ["b", "c"], "a")
    x.add_task("b", ["d"], "b")
    x.add_task("c", [], "c")
    x.add_task("d", [], "d")
    return x
@pytest.fixture
def cyclic_task_list():
    x = make.Make()
    x.add_task("a", ["b", "c"], "a")
    x.add_task("b", ["d"], "b")
    x.add_task("c", [], "c")
    x.add_task("d", ["a"], "d")
    return x
def satisfies_order(constrains, execution):
    order = {}

    for i in range(0, len(execution)):
        order[execution[i]] = i
    for task in constrains:
        for dep in constrains[task]:
            if order[dep] > order[task]:
                return False
    return True
def correct_cycle(reference_cycle, out_cycle):
    return len(reference_cycle) == len(out_cycle) and set(reference_cycle) == set(out_cycle)

class OutTest:
    def __init__(self):
        self.out = ""
    def print(self, x):
        self.out += x + "\n"
    def get(self):
        return self.out

def test_normal_commands(normal_task_list, monkeypatch):
    out = OutTest() 
    monkeypatch.setattr("builtins.print", out.print)
    normal_task_list.run_task("a")
    result = out.get()
    tree = {"a": ["b", "c"],
            "b": ["d"],
            "c": [],
            "d": []}
    assert satisfies_order(tree, result.strip()), "Print commands in the correct order"

def test_cyclic_commands(cyclic_task_list, monkeypatch):
    out = OutTest()
    monkeypatch.setattr("builtins.print", out.print)
    cyclic_task_list.run_task("a")
    result = out.get()
    cycle = ["a", "b", "d"]
    assert correct_cycle(cycle, result.strip().split('\n')[1:-1]), "Print out the task cycle"

