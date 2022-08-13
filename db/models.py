from dataclasses import dataclass, field, asdict


class DBException(Exception):
    pass


class BaseModel:
    id: int = field(default=None)

    __table: str = field(default='')

    def __post_init__(self):
        if not self.__table:
            raise DBException('Table name did not define')

    def asdict(self):
        return asdict(self)

    @property
    def columns(self):
        return self.asdict().keys()


@dataclass
class NewsModel(BaseModel):
    source: str = field(default='')
    title: str = field(default='')
    link: str = field(default='')
    details: str = field(default='')
    published: str = field(default='')
    __table = 'news'


@dataclass
class MediaModel(BaseModel):
    link: str = field(default='')
    news_id: int = field(default=None)
