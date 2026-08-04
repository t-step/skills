import { formatCurrency } from "@acme/core";

export function PriceButton({ cents }: { cents: number }) {
  return <button>{formatCurrency(cents)}</button>;
}
