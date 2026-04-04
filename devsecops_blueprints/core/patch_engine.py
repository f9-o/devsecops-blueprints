import os
import re

def patch_dockerfile(filepath: str) -> bool:
    """Attempts to apply security patches to a Dockerfile in-place. Returns True if patched."""
    if not os.path.exists(filepath):
        return False
        
    with open(filepath, "r") as f:
        content = f.read()
        
    original = content
    
    # Patch 1: Enforce non-root user if missing
    if "USER " not in content.upper():
        # Add USER appuser step before CMD or ENTRYPOINT
        if re.search(r'(CMD|ENTRYPOINT)', content):
            content = re.sub(r'(CMD|ENTRYPOINT)', r'RUN addgroup -S appuser && adduser -S appuser -G appuser\nUSER appuser\n\n\1', content, count=1)
        else:
            content += '\nRUN addgroup -S appuser && adduser -S appuser -G appuser\nUSER appuser\n'
            
    # Patch 2: Strongly tag with alpine instead of latest when generic
    content = re.sub(r'^FROM (node|python|ubuntu)(:latest)?(\s+AS\s+\w+)?$', r'FROM \1:alpine\3', content, flags=re.MULTILINE)

    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        return True
    return False

def run_auto_patcher(directory: str) -> list:
    """Scans Directory for patchable files and returns a list of applied patches."""
    applied_patches = []
    
    for root, dirs, files in os.walk(directory):
        # Skip git or build dirs
        if '.git' in root or '.github' in root:
            continue
            
        for f in files:
            if "Dockerfile" in f:
                path = os.path.join(root, f)
                if patch_dockerfile(path):
                    applied_patches.append({"File": path, "Action": "Hardened Base Image & Set Non-Root User"})
                    
    return applied_patches
