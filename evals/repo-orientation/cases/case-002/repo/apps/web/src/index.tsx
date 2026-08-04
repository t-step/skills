import { PriceButton } from "@acme/ui";
import type { Order } from "@acme/core";

export function OrderSummary({ order }: { order: Order }) {
  return <PriceButton cents={order.total} />;
}
