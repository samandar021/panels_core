from pydantic import BaseModel


class PayloadsMainRequest(BaseModel):
    title: str
    sidebar: dict
    help: dict
    notifications: dict
    account: dict
    dark_mode: bool
    language: str


class ReqponseMainRequest(BaseModel):
    status: str
    payloads: PayloadsMainRequest


class OrdersKeys(BaseModel):
    orders: bool = False
    subscriptions: bool = False
    drip_feed: bool = False


class SettingsKeys(BaseModel):
    settings_general: bool = False
    settings_providers: bool = False
    settings_add_provider: bool = False
    settings_payments: bool = False
    settings_modules: bool = False
    settings_integrations: bool = False
    settings_notifications: bool = False
    settings_bonuses: bool = False
    settings_signup_form: bool = False


class MainRequestPanelAdmin(BaseModel):
    settings: SettingsKeys
    orders: OrdersKeys
    users: bool = False
    refill: bool = False
    cancel: bool = False
    services: bool = False
    payments: bool = False
    tickets: bool = False
    affiliates: bool = False
    child_panels: bool = False


class PanelAdminRules(MainRequestPanelAdmin):
    updates: bool = False
    reports: bool = False

    reports_payments: bool = False
    reports_orders: bool = False
    reports_tickets: bool = False
    reports_profits: bool = False

    appearance_pages: bool = False
    appearance_blog: bool = False
    appearance_menu: bool = False
    appearance_themes: bool = False
    appearance_languages: bool = False
    appearance_files: bool = False

    users_add_user: bool = False
    users_edit_user: bool = False
    users_change_status: bool = False
    users_edit_discount: bool = False
    users_export_users: bool = False
    users_sign_in_history: bool = False
    orders_see_external_id: bool = False
    orders_see_user: bool = False
    orders_see_charge: bool = False
    orders_see_cost: bool = False
    orders_view_details: bool = False
    orders_resend_order: bool = False
    orders_edit_link: bool = False
    orders_set_start_count: bool = False
    orders_set_remains: bool = False
    orders_change_status: bool = False
    orders_set_partial: bool = False
    orders_update_from_provider: bool = False
    orders_cancel_and_refund: bool = False
    orders_export_orders: bool = False
    subscription_see_external_id: bool = False
    subscription_view_details: bool = False
    subscription_edit_expiry: bool = False
    subscription_change_status: bool = False
    dripfeed_change_status: bool = False
    dripfeed_cancel_refund: bool = False
    tasks_view_details: bool = False
    tasks_change_status: bool = False
    cancel_view_details: bool = False
    cancel_resend_task: bool = False
    cancel_change_status: bool = False
    services_see_provider_column: bool = False
    services_import_services: bool = False
    services_add_services: bool = False
    services_add_subscription: bool = False
    services_edit_services: bool = False
    services_edit_services_description: bool = False
    services_change_service_status: bool = False
    services_reset_custom_rates: bool = False
    services_delete_service: bool = False
    services_duplicate_service: bool = False
    services_add_category: bool = False
    services_edit_category: bool = False
    services_change_category_status: bool = False
    services_restore: bool = False
    payments_add_payment: bool = False
    payments_see_payment: bool = False
    payments_view_details: bool = False
    payments_edit_payment: bool = False
    payments_report_a_fraud: bool = False
    payments_accept_payment: bool = False
    payments_complete_payment: bool = False
    payments_export_payments: bool = False
    tickets_create_new_ticket: bool = False
    tickets_view_ticket: bool = False
    tickets_change_status: bool = False
    tickets_close_ticket: bool = False
    tickets_close_and_lock_ticket: bool = False
    tickets_delete_ticket: bool = False
    tickets_mark_as_unread: bool = False
    tickets_submit_message: bool = False
    tickets_edit_message: bool = False
    tickets_delete_message: bool = False
    tickets_mark_as_spam: bool = False
    affiliates_see_affiliates: bool = False
    affiliates_change_affiliate_status: bool = False
    affiliates_see_referrals: bool = False
    affiliates_see_payouts: bool = False
    affiliates_approve_or_reject_payout: bool = False
    child_panels_cancel_refund: bool = False
    updates_delete: bool = False
