import { useState, type FormEvent } from 'react'
import { Icon } from '../../components/Icon'
import { HAVANA_MUNICIPALITIES } from '../../data/home'
import { PROPERTY_TYPE_LABELS, type ListingType } from '../../types/property'

const LISTING_OPTIONS: { value: ListingType; label: string }[] = [
  { value: 'sale', label: 'Comprar' },
  { value: 'rental', label: 'Alquilar' },
]

export function SearchPanel() {
  const [listingType, setListingType] = useState<ListingType>('sale')

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    // TODO: navigate to the listings page with these filters once it exists
  }

  return (
    <form className="search-panel" onSubmit={handleSubmit} role="search">
      <div className="search-panel__tabs" role="radiogroup" aria-label="Tipo de operación">
        {LISTING_OPTIONS.map((option) => (
          <label
            key={option.value}
            className={`search-panel__tab${listingType === option.value ? ' is-active' : ''}`}
          >
            <input
              type="radio"
              name="listing_type"
              value={option.value}
              checked={listingType === option.value}
              onChange={() => setListingType(option.value)}
              className="visually-hidden"
            />
            {option.label}
          </label>
        ))}
      </div>

      <div className="search-panel__fields">
        <label className="field">
          <span className="field__label">Municipio</span>
          <select name="municipality" defaultValue="">
            <option value="">Toda La Habana</option>
            {HAVANA_MUNICIPALITIES.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span className="field__label">Tipo de inmueble</span>
          <select name="property_type" defaultValue="">
            <option value="">Cualquiera</option>
            {Object.entries(PROPERTY_TYPE_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span className="field__label">Habitaciones</span>
          <select name="min_bedrooms" defaultValue="">
            <option value="">Indiferente</option>
            {[1, 2, 3, 4].map((n) => (
              <option key={n} value={n}>
                {n}+
              </option>
            ))}
          </select>
        </label>

        <button type="submit" className="btn btn--primary search-panel__submit">
          <Icon name="search" size={18} />
          Buscar
        </button>
      </div>
    </form>
  )
}
