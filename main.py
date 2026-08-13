import os
import time
import random
import pickle
import threading
import ast

fc = 0
feedmeter = 100
pettype = 0
dogname = 0
catname = 0
birdname = 0
petname = 0


try:
    with open("save.pkl", "rb") as box:
        data = pickle.load(box)
        pettype = data["pettype"]
        petname = data["petname"]
except:
    pass

def feedmeter_count():
    global feedmeter
    global pettype
    while True:
        if feedmeter == 20:
            print(f"!!!!!!!!!!!!!!!!!!!!!Your {pettype} is hungry!!!!!!!!!!!!!!!!!!!!!!!!!")
        feedmeter -= 1
        time.sleep(1)

threading.Thread(target=feedmeter_count, daemon=True).start()

def intromenu():
    global fc
    fc = input('''What do you want to do? 
    1. Get a pet
    2. Play with your pet
    3. Feed your pet
    4. Save your progress
    5. Load your progress
    6. Exit
    
    ''')

def firstc():
    global pettype
    global petname
    pettype = input('''What type of pet you want?
1. Dog
2. Cat
3. Bird
0. Exit

''')

    if pettype == '1':
        petname = input("What do you want to name your dog? ")
        pettype = 'dog'
    elif pettype == '2':
        petname = input("What do you want to name your cat? ")
        pettype = 'cat'
    elif pettype == '3':
        petname = input("What do you want to name your bird? ")
        pettype = 'bird'
    elif pettype == '0':
        intromenu()
    else:
        print("Pick Again, you didn't pick a valid option.")
        firstc()
    print(f"Congratulations! You have a new {pettype} named {petname}!")
    time.sleep(1.5)

def secndc():
    path = input("Enter the path to a Python file to analyze: ").strip()
    if not path:
        print("No path provided.")
        return
    # Strip surrounding quotes, e.g. "main.py" or 'main.py'
    if len(path) >= 2 and path[0] == path[-1] and path[0] in ('"', "'"):
        path = path[1:-1]
    path = os.path.expanduser(os.path.expandvars(path))
    if not os.path.isfile(path):
        # Fall back to resolving relative to this script's folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alt = os.path.join(script_dir, path)
        if os.path.isfile(alt):
            path = alt
        else:
            print(f"File not found: {path}")
            print(f"  Tried absolute: {os.path.abspath(path)}")
            print(f"  Tried script dir: {alt}")
            return

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError as e:
        print("Syntax error parsing file:", e)
        return

    func_defs = {}  # name -> set(linenos)
    assigned = {}   # name -> set(linenos)
    used = {}       # name -> set(linenos)
    called = {}     # name -> set(linenos)

    class Analyzer(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            func_defs.setdefault(node.name, set()).add(node.lineno)
            self.generic_visit(node)

        def visit_Call(self, node):
            fn = node.func
            if isinstance(fn, ast.Name):
                called.setdefault(fn.id, set()).add(node.lineno)
                used.setdefault(fn.id, set()).add(node.lineno)
            elif isinstance(fn, ast.Attribute):
                called.setdefault(fn.attr, set()).add(node.lineno)
                used.setdefault(fn.attr, set()).add(node.lineno)
            self.generic_visit(node)

        def visit_Assign(self, node):
            for target in node.targets:
                for n in self._names_in_target(target):
                    assigned.setdefault(n, set()).add(node.lineno)
            self.generic_visit(node)

        def visit_AugAssign(self, node):
            for n in self._names_in_target(node.target):
                assigned.setdefault(n, set()).add(node.lineno)
            self.generic_visit(node)

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                used.setdefault(node.id, set()).add(node.lineno)
            self.generic_visit(node)

        def _names_in_target(self, node):
            names = set()
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, (ast.Tuple, ast.List)):
                for elt in node.elts:
                    names |= self._names_in_target(elt)
            elif isinstance(node, ast.Attribute):
                names.add(node.attr)
            return names

    Analyzer().visit(tree)

    # compute unused variables and unused functions with line numbers
    unused_vars = [(n, sorted(lines)) for n, lines in assigned.items() if n not in used and not n.startswith("__")]
    unused_funcs = [(n, sorted(lines)) for n, lines in func_defs.items() if n not in called and not n.startswith("__")]

    print("\nAnalysis report for:", path)
    if unused_funcs:
        print("Functions defined but never called:")
        for f, lines in unused_funcs:
            print(f" - {f} (defined at line {lines[0]})")
    else:
        print("No unused function definitions found.")

    if unused_vars:
        print("\nVariables assigned but never used:")
        for v, lines in unused_vars:
            print(f" - {v} (assigned at line(s) {', '.join(map(str, lines))})")
    else:
        print("No unused variables found.")

    # quick summary of calls and defs
    print(f"\nSummary: {len(func_defs)} function(s) defined, {sum(len(s) for s in called.values())} call(s) detected, {len(unused_vars)} unused var(s)")
    time.sleep(1.5)

def thrdc():
    global feedmeter
    if feedmeter <= 70:
        print(f"You fed your {pettype}!")
        feedmeter = 100
    else:
        print(f"{petname} is not hungry yet!")
    time.sleep(1.5)

def frthc():
    global feedmeter
    global pettype
    global petname
    with open("save.pkl", "wb") as box:
        data = {
            "pettype": pettype,
            "petname": petname,
        }
        pickle.dump(data, box)
    print("Your progress has been saved!")
    time.sleep(1.5)

def fifthc():
    global feedmeter
    global pettype
    global petname
    if not os.path.isfile("save.pkl"):
        print("Não existe nenhum save file. Crie um pet primeiro e salve o progresso!")
        time.sleep(1.5)
        return
    with open("save.pkl", "rb") as box:
        data = pickle.load(box)
        pettype = data["pettype"]
        petname = data["petname"]
    print("Your progress has been loaded!")
    print(f"DEBUG: pettype={pettype}, petname={petname}")
    time.sleep(1.5)

def sixthc():
    print("Goodbye!")
    exit()

print("Hello user, your pet has been waiting for you for a long time!")
time.sleep(1)

while True:
    intromenu()
    if fc == '1':
        firstc()
    elif fc == '2':
        secndc()
    elif fc == '3':
        thrdc()
    elif fc == '4':
        frthc()
    elif fc == '5':
        fifthc()
    elif fc == '6':
        sixthc()
