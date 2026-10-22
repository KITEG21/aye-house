import './Footer.css'

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="container site-footer__inner">
        <div className="site-footer__brand">
          <p className="site-footer__name">Aye House</p>
          <p className="site-footer__tagline">
            Encontrar casa en La Habana, con calma y con información clara.
          </p>
        </div>

        <nav className="site-footer__nav" aria-label="Pie de página">
          <div>
            <p className="site-footer__heading">Explorar</p>
            <ul>
              <li><a href="#destacadas">Comprar</a></li>
              <li><a href="#destacadas">Alquilar</a></li>
              <li><a href="#zonas">Zonas</a></li>
            </ul>
          </div>
          <div>
            <p className="site-footer__heading">Aye House</p>
            <ul>
              <li><a href="#como-funciona">Cómo funciona</a></li>
              <li><a href="#publicar">Publicar inmueble</a></li>
              <li><a href="#">Contacto</a></li>
            </ul>
          </div>
        </nav>
      </div>
      <div className="container site-footer__legal">
        <p>© {new Date().getFullYear()} Aye House</p>
      </div>
    </footer>
  )
}
