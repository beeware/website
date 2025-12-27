def define_env(env):
    @env.macro
    def fa(*tags):
        tags = " ".join(f"fa-{tag}" for tag in tags)
        return f'<i class="{tags}"></i>'
