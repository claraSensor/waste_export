from dataclasses import dataclass, field


class ConnectionBuilder:
    host: str = field(init=False)
    port: str = field(init=False, default=5432)
    database: str = field(init=False)
    username: str = field(init=False)
    password: str = field(init=False)

    def __str__(self):
        return f"host={self.host} port={self.port} dbname={self.database} user={self.username} password={self.password}"
