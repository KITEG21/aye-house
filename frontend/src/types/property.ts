// Mirrors the enums and response shape in backend/app/features/properties.

export type PropertyType = 'house' | 'apartment' | 'room' | 'land' | 'commercial' | 'other'
export type ListingType = 'sale' | 'rental'
export type GasType = 'piped' | 'cylinder' | 'none'
export type Currency = 'USD' | 'CUP' | 'EUR'

export interface PropertyCardData {
  id: string
  title: string
  propertyType: PropertyType
  listingType: ListingType
  price: number
  currency: Currency
  areaM2: number | null
  bedrooms: number | null
  bathrooms: number | null
  gasType: GasType
  neighborhood: string
  municipality: string
}

export const PROPERTY_TYPE_LABELS: Record<PropertyType, string> = {
  house: 'Casa',
  apartment: 'Apartamento',
  room: 'Habitación',
  land: 'Terreno',
  commercial: 'Local comercial',
  other: 'Otro',
}

export const LISTING_TYPE_LABELS: Record<ListingType, string> = {
  sale: 'Venta',
  rental: 'Alquiler',
}

export const GAS_TYPE_LABELS: Record<GasType, string> = {
  piped: 'Gas de la calle',
  cylinder: 'Gas de balita',
  none: 'Sin gas',
}
