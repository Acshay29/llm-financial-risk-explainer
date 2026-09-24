import os

def fix():
    # 1. Ensure all required directories exist
    dirs = ["ml/src", "ml/data", "ml/models", "app/api", "app/core", "app/services", "docker", "tests"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # 2. Fix hardcoded paths in all files
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".sh", ".mmd", ".md", "Dockerfile", "yml")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # This removes the old prefix if it exists
                    if "" in content:
                        print(f"Fixing paths in: {path}")
                        new_content = content.replace("", "")
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                except:
                    pass

if __name__ == "__main__":
    fix()
