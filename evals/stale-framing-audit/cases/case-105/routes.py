"""URL routing (excerpt)."""
import admin_override_panel
import order_service


ROUTES = {
    "POST /orders/<id>/cancel": order_service.cancel_order,
    "POST /admin/orders/<id>/force-cancel": admin_override_panel.force_cancel,
}
