from pydantic_settings import BaseSettings  # change import


class Settings(BaseSettings):
    SQLSERVER_SERVER: str = r"PRABHAKAR\SQLEXPRESS"
    SQLSERVER_USER: str = "sa"
    SQLSERVER_PASSWORD: str = "Thilak@938"
    SQLSERVER_DB: str = "I_campus"
    SQLSERVER_DRIVER: str = "ODBC Driver 17 for SQL Server"

    # NEW: JWT settings
    JWT_SECRET_KEY: str = "change_this_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        from urllib.parse import quote_plus

        odbc_str = (
            f"DRIVER={{{self.SQLSERVER_DRIVER}}};"
            f"SERVER={self.SQLSERVER_SERVER};"
            f"DATABASE={self.SQLSERVER_DB};"
            f"UID={self.SQLSERVER_USER};"
            f"PWD={self.SQLSERVER_PASSWORD}"
        )
        return f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_str)}"


settings = Settings()
