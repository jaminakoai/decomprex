import os

def remove_frida_detection(smali_dir):
    for root, _, files in os.walk(smali_dir):
        for file in files:
            if file.endswith('.smali'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                content = content.replace('frida', 'fr1da')
                with open(path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)

def inject_frida_agent(output_dir):
    agent_code = """\
/*
 * Frida agent örneği: (Frida ile test için)
 * Java.perform(function() {
 *     // Hook kodları buraya eklenebilir
 * });
 */
"""
    with open(os.path.join(output_dir, 'frida_hook.js'), 'w') as f:
        f.write(agent_code)
