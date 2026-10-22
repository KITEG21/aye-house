import { useState } from 'react'
import { Icon } from './Icon'
import './Header.css'

const NAV_LINKS = [
  { href: '#destacadas', label: 'Comprar' },
  { href: '#destacadas', label: 'Alquilar' },
  { href: '#zonas', label: 'Zonas' },
  { href: '#como-funciona', label: 'Cómo funciona' },
]

export function Header() {
  const [open, setOpen] = useState(false)

  return (
    <header className="site-header">
      <div className="container site-header__inner">
        <a href="/" className="brand" aria-label="Aye House, inicio">
          <img src="/favicon.svg" alt="" width={34} height={34} />
          <span className="brand__name">Aye House</span>
        </a>

        <button
          type="button"
          className="site-header__toggle btn btn--ghost"
          aria-expanded={open}
          aria-controls="site-nav"
          onClick={() => setOpen((value) => !value)}
        >
          <Icon name={open ? 'close' : 'menu'} />
          <span className="visually-hidden">{open ? 'Cerrar menú' : 'Abrir menú'}</span>
        </button>

        <nav
          id="site-nav"
          className={`site-nav${open ? ' site-nav--open' : ''}`}
          aria-label="Principal"
        >
          <ul className="site-nav__links">
            {NAV_LINKS.map((link) => (
              <li key={link.label}>
                <a href={link.href} onClick={() => setOpen(false)}>
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
          <div className="site-nav__actions">
            <a href="#" className="btn btn--ghost">
              Iniciar sesión
            </a>
            <a href="#publicar" className="btn btn--primary">
              Publicar inmueble
            </a>
          </div>
        </nav>
      </div>
    </header>
  )
}
