import type { Currency } from '../types/property'

export function formatPrice(price: number, currency: Currency) {
  return new Intl.NumberFormat('es-CU', {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).format(price)
}
