import { LitElement, html, css } from  'https://unpkg.com/lit-element@latest/lit-element.js?module';

class Strip extends LitElement {
  static get properties() {
    return {
      title: { type: String },
      link: { type: String },
      datePublished: { type: Date },
      wasRead: { type: Boolean }
    }
  }

  constructor() {
    super();
  }

  static get styles() {
    return css`
      .was-read {
        opacity: 0.5;
      }
    `;
  }

  render() {
    console.log(this.wasRead);
    return html`
      <link rel="stylesheet" href="css/skeleton.css">
      <link rel="stylesheet" href="css/normalize.css">
      <div class="container">
        <div class="row">
          <div class="seven columns">
            <a
              href=${this.link}
              class=${this.wasRead ? 'was-read' : ''}>
              ${this.title}
            </a>
          </div>
          <div class="three columns">${this.publishedDate}</div>
        </div>
      </div>
    `;
  }
}

window.customElements.define('webcomics-strip', Strip);
