import type { PropertyCardData } from '../types/property'

// Placeholder content for the home page until it is wired to the API.

// Municipalities of La Habana, as seeded in backend/app/features/zones/seed_data.py
export const HAVANA_MUNICIPALITIES = [
  'Playa',
  'Plaza de la Revolución',
  'Centro Habana',
  'La Habana Vieja',
  'Regla',
  'La Habana del Este',
  'Guanabacoa',
  'San Miguel del Padrón',
  'Diez de Octubre',
  'Cerro',
  'Marianao',
  'La Lisa',
  'Boyeros',
  'Arroyo Naranjo',
  'Cotorro',
]

export const FEATURED_PROPERTIES: PropertyCardData[] = [
  {
    id: 'sample-1',
    title: 'Casa con portal y patio arbolado',
    propertyType: 'house',
    listingType: 'sale',
    price: 68000,
    currency: 'USD',
    areaM2: 180,
    bedrooms: 3,
    bathrooms: 2,
    gasType: 'piped',
    neighborhood: 'Miramar',
    municipality: 'Playa',
  },
  {
    id: 'sample-2',
    title: 'Apartamento luminoso cerca del Malecón',
    propertyType: 'apartment',
    listingType: 'rental',
    price: 450,
    currency: 'USD',
    areaM2: 75,
    bedrooms: 2,
    bathrooms: 1,
    gasType: 'cylinder',
    neighborhood: 'Vedado',
    municipality: 'Plaza de la Revolución',
  },
  {
    id: 'sample-3',
    title: 'Planta baja tranquila con jardín',
    propertyType: 'house',
    listingType: 'sale',
    price: 42000,
    currency: 'USD',
    areaM2: 120,
    bedrooms: 2,
    bathrooms: 1,
    gasType: 'piped',
    neighborhood: 'Nuevo Vedado',
    municipality: 'Plaza de la Revolución',
  },
]

// `tone` picks the soft background shown behind the opened shutters in the hero
export const POPULAR_ZONES: {
  name: string
  municipality: string
  tone: 'sand' | 'sky' | 'linen'
}[] = [
  { name: 'Vedado', municipality: 'Plaza de la Revolución', tone: 'sand' },
  { name: 'Miramar', municipality: 'Playa', tone: 'sky' },
  { name: 'Catedral', municipality: 'La Habana Vieja', tone: 'linen' },
  { name: 'Alamar', municipality: 'La Habana del Este', tone: 'sky' },
  { name: 'Nuevo Vedado', municipality: 'Plaza de la Revolución', tone: 'sand' },
]
