from modulefinder import ModuleFinder


def print_tree(file_name, indent=""):
    finder = ModuleFinder()
    #finder.run_script("{}.py".format(file_name))
    finder.run_script(file_name)
    for name, mod in finder.modules.items():
        f_name = str(mod.__file__)
        if ("Pirate" in f_name and "settings" not in f_name and "support" not in f_name and "__" not in name):
            print(indent, name)
            print_tree(f_name, indent + "----")

print("\n\nmain")
print_tree("main.py", "--")