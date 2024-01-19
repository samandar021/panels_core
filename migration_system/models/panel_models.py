from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.types import JSON

from migration_system.models.db import Base


class UserAgentList(Base):
    __tablename__ = 'user_agent_list'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    user_agent_name: str | None = Column(String(300))


class Panels(Base):
    __tablename__ = 'panels'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    domain: str = Column(String(1000))
    created_at: int = Column(Integer)
    expired_at: int = Column(Integer)
    currency: str = Column(String(3), nullable=False, index=True)
    plan_id: int = Column(Integer, nullable=False, index=True)
    db_name: str = Column(String(45), nullable=False)
    status: int = Column(Integer, CheckConstraint('status > 0 AND age < 4'),
                         comment='1 - active, 2 - paused, 3 - deleted')
    timezone: int = Column(Integer, nullable=False, default=0)


class PanelDomains(Base):
    __tablename__ = 'panel_domains'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    panel_id: int = Column(
        Integer,
        ForeignKey('panels.panels.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    domain: str = Column(String(300), index=True, unique=True)
    domain_type: int = Column(
        Integer,
        CheckConstraint('domain_type > 0 AND age < 4'),
        comment='Тип домена: 1 - основной, 2 - системный, 3 - дополнительный',
        index=True
    )

    panel: Mapped[Panels] = relationship(Panels)


class PanelOptions(Base):
    __tablename__ = 'panel_options'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    panel_id: int = Column(
        Integer,
        ForeignKey('panels.panels.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    signup_page: int = Column(Integer)

    panel: Mapped[Panels] = relationship(Panels)


class PanelAdminHash(Base):
    __tablename__ = 'panel_admin_hash'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    panel_admin_id: int = Column(Integer, nullable=False, index=True)
    hash: str = Column(String(128), index=True)
    rand_string: str = Column(String(128))
    ip: str = Column(String(39))
    remember: int = Column(Integer, default=0)
    super_admin: int = Column(Integer, default=0)
    created_at: int = Column(Integer)
    updated_at: int = Column(Integer)
    is_2fa_step: bool = Column(Boolean)


class PanelAdmin(Base):
    __tablename__ = 'panel_admin'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    panel_id: int = Column(
        Integer,
        ForeignKey('panels.panels.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    email: str = Column(String(300))
    password: str = Column(String(300))
    password_salt: str = Column(String(300))
    authorization_at: int = Column(Integer)
    status: int = Column(Integer, CheckConstraint('status > 0 AND age < 3'), comment='1 - Active, 2 - Suspended')
    created_at: int = Column(Integer)
    updated_at: int = Column(Integer)
    dark_mode: int = Column(Integer, CheckConstraint('dark_mode >= 0 AND age < 2'), comment='0 - disabled, 1 - enabled')
    rules: dict = Column(JSON)
    lang_code: str = Column(String(2), default='en')
    lastip: str = Column(String(39))
    timezone: int = Column(Integer, nullable=True, default=None)

    panel: Mapped[Panels] = relationship(Panels)


class PlanList(Base):
    __tablename__ = 'plan_list'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(45))


class PanelUserCustomFields(Base):
    __tablename__ = 'panel_user_custom_fields'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    variable_name: str = Column(String(100))
    translation_code: str = Column(String(50))
    rules: dict = Column(JSON)
    position: int = Column(Integer)
    default: int = Column(
        Integer,
        CheckConstraint('has_extra_fee > -1 AND age < 2'),
    )
    created_at: int = Column(Integer)


class PaymentMethods(Base):
    __tablename__ = 'payment_methods'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100))
    addfunds_form: dict = Column(JSON)
    settings_form: dict = Column(JSON)
    settings_form_description: str = Column(String(300))
    has_take_fee: int = Column(
        Integer,
        CheckConstraint('has_take_fee > -1 AND age < 2'),
    )
    has_extra_fee: int = Column(
        Integer,
        CheckConstraint('has_extra_fee > -1 AND age < 2'),
    )
    created_at: int = Column(Integer)
    updated_at: int = Column(Integer)


class PaymentMethodsCurrencies(Base):
    __tablename__ = 'payment_methods_currencies'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    method_id: int = Column(
        Integer,
        ForeignKey('panels.payment_methods.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        unique=True,
        index=True
    )
    currency = Column(String(3), unique=True, index=True)
    position: int = Column(Integer)
    settings_form: dict = Column(JSON)
    settings_form_description: str = Column(String(300))
    is_available: int = Column(
        Integer,
        CheckConstraint('is_available > -1 AND age < 2'),
    )
    created_at: int = Column(Integer)
    updated_at: int = Column(Integer)

    method: Mapped[PaymentMethods] = relationship(PaymentMethods)


class PanelPaymentMethods(Base):
    __tablename__ = 'panel_payment_methods'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    panel_id: int = Column(
        Integer,
        ForeignKey('panels.panels.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    )
    method_id: int = Column(
        Integer,
        ForeignKey('panels.payment_methods.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    )
    currency_id: int = Column(
        Integer,
        ForeignKey('panels.payment_methods_currencies.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    )
    is_visible: bool = Column(Boolean)
    webhook_url: str = Column(String(500))
    is_test_mode: bool = Column(Boolean)
    min_amount: int = Column(Integer)
    max_amount: int = Column(Integer)
    is_deleted: int = Column(
        Integer,
        CheckConstraint('is_deleted > -1 AND age < 2'),
    )
    amount_currency: int = Column(Integer)
    has_available_for_new_user: int = Column(
        Integer,
        CheckConstraint('has_available_for_new_user > -1 AND age < 2'),
    )
    position: int = Column(Integer)
    has_extra_fee: int = Column(
        Integer,
        CheckConstraint('has_extra_fee > -1 AND age < 2'),
    )
    has_take_from_user: int = Column(
        Integer,
        CheckConstraint('has_take_from_user > -1 AND age < 2'),
    )
    created_at: int = Column(Integer)
    updated_at: int = Column(Integer)

    panel: Mapped[Panels] = relationship(Panels)
    method: Mapped[PaymentMethods] = relationship(PaymentMethods)
    currency: Mapped[PaymentMethodsCurrencies] = relationship(PaymentMethodsCurrencies)


class PanelPaymentMethodsOptions(Base):
    __tablename__ = 'panel_payment_methods_options'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    panel_payment_methods_id: int = Column(
        Integer,
        ForeignKey('panels.panel_payment_methods.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    )
    options: str = Column(Text(5000))

    panel_payment_methods: Mapped[PanelPaymentMethods] = relationship(PanelPaymentMethods)


class PanelPaymentMethodsBonuses(Base):
    __tablename__ = 'panel_payment_methods_bonuses'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    panel_payment_methods_id: int = Column(
        Integer,
        ForeignKey('panels.panel_payment_methods.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    )
    amount_percent: int = Column(Integer)
    deposit_from: int = Column(Integer)
    is_available: int = Column(
        Integer,
        CheckConstraint('has_take_from_user > -1 AND age < 2'),
    )
    created_at: int = Column(Integer)
    updated_at: int = Column(Integer)

    panel_payment_methods: Mapped[PanelPaymentMethods] = relationship(PanelPaymentMethods)


class PanelAdminAuthCodes(Base):
    __tablename__ = 'panel_admin_auth_codes'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True)
    panel_admin_id: int = Column(
        Integer,
        ForeignKey('panels.panel_admin.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    panel_admin_hash_id: int = Column(
        Integer,
        ForeignKey('panels.panel_admin_hash.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        index=True
    )
    auth_code: int = Column(Integer)
    attempts: int = Column(Integer)
    created_at: int = Column(Integer)

    panel_admin: Mapped[PanelAdmin] = relationship(PanelAdmin)


class PanelLanguages(Base):
    __tablename__ = 'panel_languages'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    code: str = Column(String(2), nullable=False, unique=True)
    name: str = Column(String(30), nullable=False, unique=True)
    direction: str = Column(
        Enum('ltr', 'rtl'),
        nullable=False,
        comment='ltr - Left to Right, rtl - Right to Left')
    default: int = Column(
        Integer,
        CheckConstraint('default >= 0 AND default <= 1'), comment='0 - No, 1 - Yes')


class PanelLanguageMessages(Base):
    __tablename__ = 'panel_language_messages'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    lang_code: str = Column(String(2), nullable=False, index=True)
    section: str = Column(String(50), nullable=False, index=True)
    code: str = Column(String(50), nullable=False, index=True)
    value: str = Column(Text(500), nullable=False)


class Providers(Base):
    __tablename__ = 'providers'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(300), nullable=False)
    domain: str = Column(String(300), nullable=False, unique=True)
    currency: str = Column(String(3), nullable=False)
    settings_form: dict = Column(JSON)
    created_at: int = Column(Integer)
    updated_at: int = Column(Integer)


class PanelProviders(Base):
    __tablename__ = 'panel_providers'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    panel_id: int = Column(
        Integer,
        ForeignKey('panels.panels.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        nullable=False
    )
    provider_id: int = Column(
        Integer,
        ForeignKey('panels.providers.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        nullable=False
    )
    auth_field_1: str = Column(String(256), nullable=True)
    auth_field_2: str = Column(String(256), nullable=True)
    auth_field_3: str = Column(String(256), nullable=True)
    created_at: int = Column(Integer)
    updated_at: int = Column(Integer)

    panel: Mapped[Panels] = relationship(Panels)
    provider: Mapped[Providers] = relationship(Providers)


class PanelProviderHistory(Base):
    __tablename__ = 'panel_provider_history'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    panel_id: int = Column(
        Integer,
        ForeignKey('panels.panels.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        nullable=False)
    string: str = Column(String(256))
    has_found: int = Column(
        Integer,
        CheckConstraint('has_found >= 0 AND has_found < 2'), comment='0 - No, 1 - Yes')
    created_at: int = Column(Integer)

    panel: Mapped[Panels] = relationship(Panels)


class PanelProviderAPIKeyLog(Base):
    __tablename__ = 'panel_provider_apikey_log'
    __table_args__ = {'mysql_engine': 'InnoDB', 'schema': 'panels'}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    panel_id: int = Column(
        Integer,
        ForeignKey('panels.panels.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        nullable=False)
    provider_id: int = Column(
        Integer,
        ForeignKey('panels.providers.id', ondelete='NO ACTION', onupdate='NO ACTION'),
        nullable=False)
    auth_field_1: str = Column(String(256), nullable=True)
    auth_field_2: str = Column(String(256), nullable=True)
    auth_field_3: str = Column(String(256), nullable=True)

    panel: Mapped[Panels] = relationship(Panels)
    provider: Mapped[Providers] = relationship(Providers)
