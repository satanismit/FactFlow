import os

root_dir = r"d:\D\sem_6\SGP-II\AXIOMAI"
exclude_dirs = {"myenv", ".git", "node_modules", ".venv", "__pycache__", "dist"}

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        new_content = new_content.replace('AXIOMAI', 'AXIOMAI')
        new_content = new_content.replace('axiomai', 'axiomai')
        new_content = new_content.replace('AXIOMAI', 'AXIOMAI')
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated content: {filepath}")
    except Exception as e:
        print(f"Skipping {filepath}: {e}")

def rename_files_and_dirs(root):
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        # We process bottom-up (topdown=False) so we don't invalidate paths
        for filename in filenames:
            if 'axiomai' in filename.lower() and filename != 'rename.py':
                old_path = os.path.join(dirpath, filename)
                new_name = filename.replace('AXIOMAI', 'AXIOMAI').replace('axiomai', 'axiomai').replace('AXIOMAI', 'AXIOMAI')
                new_path = os.path.join(dirpath, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed file: {filename} -> {new_name}")
                
        for dirname in dirnames:
            if dirname in exclude_dirs:
                continue
            if 'axiomai' in dirname.lower():
                old_path = os.path.join(dirpath, dirname)
                new_name = dirname.replace('AXIOMAI', 'AXIOMAI').replace('axiomai', 'axiomai').replace('AXIOMAI', 'AXIOMAI')
                new_path = os.path.join(dirpath, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed directory: {dirname} -> {new_name}")

print("--- Starting Content Replacement ---")
for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
    for filename in filenames:
        if filename.endswith(('.py', '.html', '.js', '.jsx', '.css', '.md', '.json', '.env', '.txt')):
            replace_in_file(os.path.join(dirpath, filename))

print("\n--- Starting File/Directory Renames ---")
rename_files_and_dirs(root_dir)
print("Done.")
