import cx_Freeze
#to export to exe: python setup.py bdist_msi
executables = [cx_Freeze.Executable("New_World.py")]

cx_Freeze.setup(
    name = "New Worlds!",
    options= {"build_exe":{"packages":["pygame"],"include_files":["Sprites/test.png", "Sprites/Grass.png", "Sprites/Dirt.png", "Sprites/Bedrock.png"]}},
    description = "Terraria Like",
    executables = executables
    )
