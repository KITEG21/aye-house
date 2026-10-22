import type { CSSProperties, ReactNode } from 'react'
import { Icon, type IconName } from '../../components/Icon'
import { PropertyCard } from '../../components/PropertyCard'
import { FEATURED_PROPERTIES, POPULAR_ZONES } from '../../data/home'
import { useInView } from '../../hooks/useInView'
import { PROPERTY_TYPE_LABELS } from '../../types/property'
import { formatPrice } from '../../utils/format'
import { SearchPanel } from './SearchPanel'
import './Home.css'

const STEPS: { icon: IconName; title: string; text: string }[] = [
  {
    icon: 'search',
    title: 'Busca sin prisa',
    text: 'Filtra por municipio, reparto, precio o tipo de gas. Toda la información, a la vista.',
  },
  {
    icon: 'chat',
    title: 'Habla con el dueño',
    text: 'Contacta directamente y resuelve tus dudas antes de visitar la vivienda.',
  },
  {
    icon: 'key',
    title: 'Múdate tranquilo',
    text: 'Visita, compara y decide a tu ritmo, sin presiones ni sorpresas.',
  },
]

const PROMISES: { icon: IconName; title: string; text: string }[] = [
  {
    icon: 'shield',
    title: 'Anuncios revisados',
    text: 'Revisamos cada publicación para que lo que ves sea lo que encuentras.',
  },
  {
    icon: 'leaf',
    title: 'Información honesta',
    text: 'Precio, metros, gas y estado claros desde el principio.',
  },
]

// Shared Havana colonial window: a stained-glass fan (mediopunto) on top and two
// louvered shutters that swing open over whatever is passed as children.
function ColonialWindow({ children }: { children: ReactNode }) {
  return (
    <>
      <span className="window__fan" aria-hidden="true" />
      <span className="window__pane">
        {children}
        <span className="window__leaf window__leaf--left" aria-hidden="true" />
        <span className="window__leaf window__leaf--right" aria-hidden="true" />
      </span>
      <span className="window__sill" aria-hidden="true" />
    </>
  )
}

const HERO_LISTING = FEATURED_PROPERTIES[1]

function Hero() {
  return (
    <section className="hero animate-in">
      <div className="container hero__inner">
        <div className="hero__copy">
          <span className="eyebrow">Casas y apartamentos en La Habana</span>
          <h1 className="hero__title">
            Cada ventana, <em>un hogar posible</em>
          </h1>
          <p className="hero__lead">
            Viviendas en venta y alquiler con información clara, para que encuentres sin prisas la
            casa que te espera.
          </p>
          <div className="hero__actions">
            <a href="#destacadas" className="btn btn--primary">
              Explorar viviendas
            </a>
            <a href="#zonas" className="btn btn--secondary">
              Ver zonas
            </a>
          </div>
          <ul className="hero__trust">
            <li>
              <Icon name="shield" size={18} />
              Anuncios revisados
            </li>
            <li>
              <Icon name="flame" size={18} />
              Precio, metros y gas claros
            </li>
          </ul>
        </div>

        <div className="hero__visual">
          <div className="window window--hero">
            <ColonialWindow>
              <span
                className="window__inside hero-view"
                role="img"
                aria-label="Vista del mar, el Malecón y el faro del Morro desde una ventana habanera"
              >
                <span className="hero-view__sun" />
                <span className="hero-view__sea">
                  <span className="hero-view__glint" />
                  <span className="hero-view__wave" />
                  <span className="hero-view__wave hero-view__wave--far" />
                </span>
                <span className="hero-view__morro">
                  <span className="hero-view__beam" />
                  <span className="hero-view__lamp" />
                </span>
                <span className="hero-view__malecon" />
                <span className="hero-view__railing" />
              </span>
            </ColonialWindow>
          </div>

          <a href="#destacadas" className="hero__listing">
            <span className="hero__listing-icon">
              <Icon name="pin" size={20} />
            </span>
            <span className="hero__listing-text">
              <span className="hero__listing-place">
                {HERO_LISTING.neighborhood} · {PROPERTY_TYPE_LABELS[HERO_LISTING.propertyType]}
              </span>
              <span className="hero__listing-price">
                {formatPrice(HERO_LISTING.price, HERO_LISTING.currency)}
                {HERO_LISTING.listingType === 'rental' && <small> / mes</small>}
              </span>
            </span>
          </a>
        </div>
      </div>
    </section>
  )
}

function SearchBand() {
  return (
    <div className="search-band">
      <div className="container">
        <SearchPanel />
      </div>
    </div>
  )
}

function Zones() {
  // The shutters wait until the street scrolls into view, then open one after another
  const [ref, inView] = useInView<HTMLDivElement>()

  return (
    <section id="zonas" className="section zones">
      <div className="container">
        <header className="section__header section__header--center">
          <span className="eyebrow">Zonas populares</span>
          <h2 className="section__title">Asómate a los barrios más buscados</h2>
          <p className="section__lead">
            Cada reparto tiene su ritmo. Abre una ventana y mira lo que hay disponible.
          </p>
        </header>
      </div>

      <div ref={ref} className={`facade ${inView ? 'animate-in' : 'animate-pending'}`}>
        <ul className="facade__windows">
          {POPULAR_ZONES.map((zone, index) => (
            <li key={zone.name} className="facade__item" style={{ '--i': index } as CSSProperties}>
              <a href="#" className="window">
                <ColonialWindow>
                  <span className={`window__inside window__inside--${zone.tone}`}>
                    <span className="window__municipality">{zone.municipality}</span>
                    <span className="window__name">{zone.name}</span>
                    <span className="window__cta">
                      Ver viviendas
                      <Icon name="arrow" size={14} />
                    </span>
                  </span>
                </ColonialWindow>
              </a>
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}

function FeaturedProperties() {
  return (
    <section id="destacadas" className="section">
      <div className="container">
        <header className="section__header section__header--row">
          <div>
            <span className="eyebrow">Destacadas</span>
            <h2 className="section__title">Viviendas para empezar a mirar</h2>
          </div>
          <a href="#" className="link-arrow">
            Ver todas
            <Icon name="arrow" size={18} />
          </a>
        </header>

        <div className="property-grid">
          {FEATURED_PROPERTIES.map((property, index) => (
            <PropertyCard key={property.id} property={property} index={index} />
          ))}
        </div>
      </div>
    </section>
  )
}

function HowItWorks() {
  return (
    <section id="como-funciona" className="section section--tinted">
      <div className="container">
        <header className="section__header section__header--center">
          <span className="eyebrow">Cómo funciona</span>
          <h2 className="section__title">Tres pasos, a tu ritmo</h2>
        </header>

        <ol className="steps">
          {STEPS.map((step, index) => (
            <li key={step.title} className="step">
              <span className="step__icon">
                <Icon name={step.icon} size={24} />
              </span>
              <span className="step__number">0{index + 1}</span>
              <h3 className="step__title">{step.title}</h3>
              <p className="step__text">{step.text}</p>
            </li>
          ))}
        </ol>

        <ul className="promises">
          {PROMISES.map((promise) => (
            <li key={promise.title} className="promise">
              <Icon name={promise.icon} size={22} />
              <div>
                <p className="promise__title">{promise.title}</p>
                <p className="promise__text">{promise.text}</p>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}

function PublishCta() {
  return (
    <section id="publicar" className="section section--flush">
      <div className="container">
        <div className="cta">
          <div>
            <h2 className="cta__title">¿Quieres vender o alquilar tu vivienda?</h2>
            <p className="cta__text">
              Publica tu anuncio en minutos y llega a personas que buscan justo lo que ofreces.
            </p>
          </div>
          <div className="cta__actions">
            <a href="#" className="btn btn--primary">
              Publicar inmueble
            </a>
            <a href="#como-funciona" className="btn btn--outline-light">
              Saber más
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}

export function Home() {
  return (
    <>
      <Hero />
      <SearchBand />
      <Zones />
      <FeaturedProperties />
      <HowItWorks />
      <PublishCta />
    </>
  )
}
