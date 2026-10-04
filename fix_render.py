with open('render.yaml', 'r') as f:
    content = f.read()

old_env = """      - key: AUTH_MODE
        value: firebase"""

new_env = """      - key: AUTH_MODE
        value: firebase
      - key: CORS_ORIGINS
        value: "https://salesbrain-frontend-c4q0.onrender.com,http://localhost:3000,http://127.0.0.1:3000" """

content = content.replace(old_env, new_env)

with open('render.yaml', 'w') as f:
    f.write(content)
