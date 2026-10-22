import {
  GAS_TYPE_LABELS,
  LISTING_TYPE_LABELS,
  PROPERTY_TYPE_LABELS,
  type PropertyCardData,
} from '../types/property'
import { formatPrice } from '../utils/format'
import { Icon } from './Icon'
import './PropertyCard.css'

// Soft backdrops for cards without photos yet, picked by position in the list
const PLACEHOLDER_TONES = ['tone-sand', 'tone-slate', 'tone-mist'] as const

interface PropertyCardProps {
  property: PropertyCardData
  index?: number
}

export function PropertyCard({ property, index = 0 }: PropertyCardProps) {
  const tone = PLACEHOLDER_TONES[index % PLACEHOLDER_TONES.length]

  return (
    <article className="property-card">
      <div className={`property-card__media ${tone}`} aria-hidden="true">
        <svg viewBox="0 0 200 120" preserveAspectRatio="xMidYMax slice">
          <circle cx="160" cy="30" r="14" className="sun" />
          <path d="M0 120V92c30-10 60-12 100-6s70 4 100-4v38Z" className="hill" />
          <path d="M62 120V74l38-28 38 28v46Z" className="house" />
          <path d="M90 120V96h20v24Z" className="door" />
        </svg>
        <span className="property-card__badge">{LISTING_TYPE_LABELS[property.listingType]}</span>
      </div>

      <div className="property-card__body">
        <p className="property-card__location">
          <Icon name="pin" size={16} />
          {property.neighborhood}, {property.municipality}
        </p>
        <h3 className="property-card__title">
          <a href="#">{property.title}</a>
        </h3>
        <p className="property-card__type">{PROPERTY_TYPE_LABELS[property.propertyType]}</p>

        <ul className="property-card__features">
          {property.bedrooms != null && (
            <li>
              <Icon name="bed" size={18} />
              {property.bedrooms} hab.
            </li>
          )}
          {property.bathrooms != null && (
            <li>
              <Icon name="bath" size={18} />
              {property.bathrooms} baño{property.bathrooms === 1 ? '' : 's'}
            </li>
          )}
          {property.areaM2 != null && (
            <li>
              <Icon name="area" size={18} />
              {property.areaM2} m²
            </li>
          )}
          <li>
            <Icon name="flame" size={18} />
            {GAS_TYPE_LABELS[property.gasType]}
          </li>
        </ul>

        <p className="property-card__price">
          {formatPrice(property.price, property.currency)}
          {property.listingType === 'rental' && <span> / mes</span>}
        </p>
      </div>
    </article>
  )
}
