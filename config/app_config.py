from config.cloudinary_config import CloudinarySettings
from config.database_config import DatabaseSettings
from config.firebase_config import FirebaseSettings
from config.mailersend_config import MailerSendSettings
from config.project_config import ProjectSettings
from config.redis_config import RedisSettings
from config.vnpay_config import VNPaySettings


class AppSettings:
    project: ProjectSettings = ProjectSettings()
    database: DatabaseSettings = DatabaseSettings()
    firebase: FirebaseSettings = FirebaseSettings()
    redis: RedisSettings = RedisSettings()
    cloudinary: CloudinarySettings = CloudinarySettings()
    mailersend: MailerSendSettings = MailerSendSettings()
    vnpay: VNPaySettings = VNPaySettings()
