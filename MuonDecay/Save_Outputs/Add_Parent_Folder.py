import sys, os, inspect

def Add_Parent_Folder():
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

Add_Parent_Folder()

print('\n')
for i in range(len(sys.path)):
    print(sys.path[i])
print('\n')

'''
    Usually, Python automatically adds the current directory to the sys.path and deletes that after finishing the script.
    In order to add the parent folder, you can run this code which will add not only the current folder,
but the parent folder. After the execution, it'll be deleted from the path.
    If you want to make that in a defenitive way, you need to add the path manually on the environment variable.
 '''

#from Configs import cfg_scope