# ------------------ * Import * ----------------- #
from sqlalchemy import ForeignKey, String, Integer, Column, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, UniqueConstraint

from models.database.database import Base

from typing import List

from sqlalchemy.sql import func

from datetime import datetime
# ----------------------------------------------- #



class Reading(Base):

    __tablename__ = "letture"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prog_msg: Mapped[int] = mapped_column(default=0)
    device: Mapped[str] = mapped_column('terminale', String(8), index=True)
    date_event: Mapped[datetime] = mapped_column('data', DateTime(timezone=True), default=func.now())
    date_event_int: Mapped[int] = mapped_column('data_int', Integer)
    time_event: Mapped[datetime] = mapped_column('ora', DateTime(timezone=True), default=func.now())
    timestamp_event: Mapped[int] = mapped_column('timestamp_data_ora', Integer, index=True)
    datetime_event: Mapped[datetime] = mapped_column('data_ora_utc', DateTime(timezone=True), default=func.now()) #@TODO potremmo cancellare perchè salviamo tutto in UTC
    timestamp_event_utc: Mapped[int] = mapped_column('timestamp_data_ora_utc', Integer, index=True)#@TODO timestamp_event e timestamp_event_utc corrispondono perchè qui salviamo tutto in UTC uno si può cancellare
    latitude: Mapped[str] = mapped_column('latitudine', String(9))
    longitude: Mapped[str] = mapped_column('longitudine', String(10))
    battery: Mapped[str] = mapped_column('batteria', String(2))
    anomaly: Mapped[str] = mapped_column('anomalie', String(2), default='00')
    epc: Mapped[str] = mapped_column(String(60), default='')
    epc_ascii: Mapped[str] = mapped_column(String(60), default='')
    note: Mapped[str] = mapped_column(String(255), default='')
    date_rcv: Mapped[datetime] = mapped_column('dt_rcv', DateTime(timezone=True))
    time_rcv: Mapped[datetime] = mapped_column('tm_rcv', DateTime(timezone=True))
    timestamp_rcv: Mapped[int] = mapped_column('timestamp_rcv', Integer, index=True)
    type: Mapped[str] = mapped_column('msg_type', String(2), index=True)
    tags_in_memory: Mapped[int] = mapped_column(Integer, default=0)
    hwfw: Mapped[str] = mapped_column('hwfw', String(5), default='') #TODO: trigger che aggiorna la tabella dei dispositivi
    ecomat_roll: Mapped[str] = mapped_column('ecomat_rotolo', String(2), default='')
    ecomat_epc_readed: Mapped[str] = mapped_column(String(60), default='')


