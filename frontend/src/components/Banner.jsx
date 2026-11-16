export default function Banner({ title, subtitle, children, meta }) {
  return (
    <section className="banner">
      <div className="container banner-inner">
        <div className="banner-text">
          {meta && <div className="banner-meta">{meta}</div>}
          <h1>{title}</h1>
          {subtitle && <p>{subtitle}</p>}
        </div>
        {children && <div className="banner-actions">{children}</div>}
      </div>
    </section>
  );
}
