from sqlalchemy import DECIMAL, Boolean, CheckConstraint, Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.types import JSON

from migration_system.models.db import Base

from .panel_models import PanelAdmin, PanelPaymentMethods, UserAgentList


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(300))
    refferer_id: int = Column(Integer, default=None)
    password: str = Column(String(300))
    password_salt: str = Column(String(300))
    password_method: int = Column(Integer, default=0)
    balance = Column(DECIMAL(precision=21, scale=7), default=0)
    spent = Column(DECIMAL(precision=21, scale=7), default=0)
    created_at: int = Column(Integer, default=None)
    updated_at: int = Column(Integer, default=None)
    auth_at: int = Column(Integer)
    auth_ip: str = Column(String(39))
    apikey: str = Column(String(64), default=None)
    refferal_key: str = Column(String(8), unique=True)
    discount: int = Column(Integer, default=0)
    timezone: int = Column(Integer, default=0)
    terms_confirm: int = Column(Integer, default=None)
    lang_code: str = Column(String(2), default=None)
    email_status: int = Column(
        Integer,
        CheckConstraint('domain_type > 0 AND age < 3'),
        default=0,
        comment='0 - not confirmed, 1 - confirmed'
    )
    status: int = Column(
        Integer,
        CheckConstraint('domain_type > 0 AND age < 3'),
        default=1,
        comment='1 - active, 2 - suspended'
    )
    custom_variables: dict = Column(JSON, default=None)
    currency: str = Column(String(3), default=None)
    has_subscription: int = Column(Integer, default=0)
    has_drip_feed: int = Column(Integer, default=0)
    has_ticket: int = Column(Integer, default=0)
    has_refill_task: int = Column(Integer, default=0)
    custom_rates_quantity: int = Column(Integer, default=0)
    confirmed: int = Column(Integer, default=0)
    cpf_field: str = Column(String(200), default=None)
    two_fa_enabled: int = Column(Integer, default=0)
    two_fa_generated_at: int = Column(Integer, default=None)
    two_fa_generate_blocked: int = Column(Integer, default=None)
    resend_email_at: int = Column(Integer, default=None)
    change_email_at: int = Column(Integer, default=None)
    orders_count: int = Column(Integer, default=0)
    apikey_updated_at: int = Column(Integer, default=None)


class ActivityLog(Base):
    __tablename__ = 'activity_log'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    panel_admin_id: int = Column(
        Integer,
        ForeignKey('panels.panel_admin.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    user_agent_id: int = Column(
        Integer,
        ForeignKey('panels.user_agent_list.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    super_admin: int = Column(Integer)
    created_at: int = Column(Integer)
    ip: str = Column(String(39))
    details_id: int = Column(Integer)
    url: str = Column(String(1000))
    event_id: int = Column(Integer)

    panel_admin: Mapped[PanelAdmin] = relationship(PanelAdmin)
    user_agent: Mapped[UserAgentList] = relationship(UserAgentList)


class ActivityLogDetails(Base):
    __tablename__ = 'activity_log_details'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    request_data: str = Column(Text)
    activity_log_details_id: int = Column(
        Integer,
        ForeignKey('activity_log.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    )

    activity_log_details: Mapped[ActivityLog] = relationship(ActivityLog)


class UsersApikeyHistory(Base):
    __tablename__ = 'users_apikey_history'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    apikey: str = Column(String(128))
    created_at: int = Column(Integer)

    user: Mapped[Users] = relationship(Users)


class UsersActivityLog(Base):
    __tablename__ = 'users_activity_log'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    user_agent_id: int = Column(
        Integer,
        ForeignKey('panels.user_agent_list.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    ip: str = Column(String(39))
    event: int = Column(Integer)
    location: str = Column(String(1000))
    created_at: int = Column(Integer)

    user: Mapped[Users] = relationship(Users)
    user_agent: Mapped[UserAgentList] = relationship(UserAgentList)


class UserDetails(Base):
    __tablename__ = 'user_details'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    field_name: str = Column(String(300))
    field_value: str = Column(String(300))

    user: Mapped[Users] = relationship(Users)


class UserCustomFields(Base):
    __tablename__ = 'user_custom_fields'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    default_field_id: int = Column(Integer)
    position: int = Column(Integer)
    rules: dict = Column(JSON)
    updated_at: int = Column(Integer)
    created_at: int = Column(Integer)

    user: Mapped[Users] = relationship(Users)


class UsersPasswordHistory(Base):
    __tablename__ = 'users_password_history'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    password: str = Column(String(300))
    password_salt: str = Column(String(300))
    created_at: int = Column(Integer)

    user: Mapped[Users] = relationship(Users)


class UsersCustomRates(Base):
    __tablename__ = 'users_custom_rates'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    service_id: int = Column(
        Integer,
        index=True
    )
    rate = Column(DECIMAL(precision=21, scale=4), default=0)
    is_percent: int = Column(
        Integer,
        CheckConstraint('domain_type > 0 AND age < 3'),
        default=0,
        comment='0 - fixed service rate, 1 - percent  of service rate'
    )

    user: Mapped[Users] = relationship(Users)


class UsersAuthCodes(Base):
    __tablename__ = 'users_auth_codes'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    event: str = Column(String(45))

    user: Mapped[Users] = relationship(Users)


class PaymentMethodsTranslations(Base):
    __tablename__ = 'payment_methods_translations'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    panel_payment_methods_id: int = Column(
        Integer,
        ForeignKey('panels.panel_payment_methods.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    )
    lang_code: str = Column(String(2))
    name: str = Column(String(50))
    descriptions: str = Column(String(200))
    created_at: int = Column(Integer)
    updated_at: int = Column(Integer)

    panel_payment_methods: Mapped[PanelPaymentMethods] = relationship(PanelPaymentMethods)


class UserPaymentMethods(Base):
    __tablename__ = 'user_payment_methods'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer,
        ForeignKey('users.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    )
    panel_payment_method_id: int = Column(
        Integer,
        ForeignKey('panels.panel_payment_methods.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    )
    is_enabled: bool = Column(Boolean)

    user: Mapped[Users] = relationship(Users)
    panel_payment_methods: Mapped[PanelPaymentMethods] = relationship(PanelPaymentMethods)


class Languages(Base):
    __tablename__ = 'languages'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    lang_code = Column(String(2), nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    position = Column(Integer)
    default = Column(
        Integer,
        CheckConstraint('default >= 0 AND default <= 1'), comment='0 - No, 1 - Yes'
    )
    is_visible = Column(
        Integer,
        CheckConstraint('is_visible >= 0 AND is_visible <= 1'), comment='0 - Hidden, 1 - Visible'
    )
    direction: str = Column(
        Enum('ltr', 'rtl'),
        nullable=False,
        comment='ltr - Left to Right, rtl - Right to Left')
    created_at = Column(Integer)
    updated_at = Column(Integer)


class LanguageMessages(Base):
    __tablename__ = 'language_messages'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    lang_code = Column(String(2), nullable=False)
    code = Column(String(50), nullable=False)
    value = Column(Text(500), nullable=False)
