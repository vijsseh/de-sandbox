import os

c = get_config()

# -------------------------
# JupyterHub
# -------------------------

c.JupyterHub.bind_url = "http://0.0.0.0:8000"

# Адрес, по которому студенческие контейнеры
# смогут обращаться к Hub внутри Docker-сети.
c.JupyterHub.hub_bind_url = "http://0.0.0.0:8081"
c.JupyterHub.hub_connect_url = "http://hub:8081"

# База пользователей JupyterHub.
c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/jupyterhub.sqlite"

# -------------------------
# Авторизация (только локальный тест)
# -------------------------

# Авторизация через логин и пароль
c.JupyterHub.authenticator_class = "native"

# Администратор
c.Authenticator.admin_users = {"admin"}

# Новые пользователи должны пройти проверку NativeAuthenticator
c.Authenticator.allow_all = True
c.Authenticator.allow_existing_users = False

# Регистрация доступна, но требуется подтверждение
c.NativeAuthenticator.enable_signup = True
c.NativeAuthenticator.open_signup = False

# Пароли и защита от перебора
c.NativeAuthenticator.minimum_password_length = 12
c.NativeAuthenticator.allowed_failed_logins = 5
c.NativeAuthenticator.seconds_before_next_try = 600
# c.Authenticator.allowed_users = {
#     "admin",
# }

c.Authenticator.admin_users = {"admin"}

# -------------------------
# DockerSpawner
# -------------------------

c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

c.DockerSpawner.image = "de-student:s3a"

c.DockerSpawner.network_name = "de-sandbox-net"
c.DockerSpawner.use_internal_ip = True

c.DockerSpawner.name_template = "de-{username}"

c.DockerSpawner.environment = {
    "SPARK_LOCAL_HOSTNAME": lambda spawner: spawner.name,
}

# Удаляем контейнер после остановки,
# но пользовательские файлы сохраняем.
c.DockerSpawner.remove = True

# Отдельный Docker volume для каждого студента.
c.DockerSpawner.volumes = {
    "de-sandbox-user-{username}": "/home/jovyan/work"
}

c.DockerSpawner.notebook_dir = "/home/jovyan/work"

# Сразу открываем JupyterLab.
c.Spawner.default_url = "/lab"

# -------------------------
# Ограничения ресурсов
# -------------------------

c.Spawner.mem_limit = "1.5G"
c.Spawner.cpu_limit = 1.0
