from dotenv import load_dotenv, find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".env"))


class ProjectSettings(BaseSettings):

    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: int = Field(alias="POSTGRES_PORT")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(alias="POSTGRES_DB")

    postgres_engine: str = Field(alias="POSTGRES_ENGINE")

    log_topic: str = Field(alias="LOG_TOPIC", default="log_topic")

    kafka_host: str = Field(alias="KAFKA_HOST")
    kafka_port: str = Field(alias="KAFKA_PORT")

    @property
    def get_sql_url(self):
        return "postgresql+{}://{}:{}@{}:{}/{}".format(
            self.postgres_engine,
            self.postgres_user,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_db,
        )

    @property
    def bootstrap_server_kafka(self):
        return "{}:{}".format(self.kafka_host, self.kafka_port)


def get_settings() -> ProjectSettings:
    return ProjectSettings()
