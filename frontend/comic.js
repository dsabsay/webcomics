import { LitElement, html, css } from  'https://unpkg.com/lit-element@latest/lit-element.js?module';
import './strip.js';

class Comic extends LitElement {
  static get properties() {
    return {
      name: {
        type: String,
        reflect: true
      },
      link: {
        type: String,
        reflect: true
      },
      iconUrl: {
        type: String,
        reflect: true,
      },
      numUnread: {
        type: Number,
        reflect: true
      },
      strips: {
        type: Array
      },
      isOpen: { type: Boolean, reflect: true }
    }
  }

  constructor() {
    super();
  }

  render() {
    return html`
      <link rel="stylesheet" href="css/skeleton.css">
      <link rel="stylesheet" href="css/normalize.css">
      <div class="container">
        <div class="row">
          <div class="one column">
            <img src=${this.iconUrl} alt="Icon">
          </div>
          <div class="ten columns">
            <a href=${this.link}>${this.name}</a>
          </div>
          <div class="one column">
            <p>${this.numUnread}</p>
          </div>
        </div>
        ${this.isOpen
          ? this.strips.map(strip => html`
            <webcomics-strip
              title=${strip.title}
              link=${strip.link}
              datePublished=${strip.datePublished}
              .wasRead=${strip.wasRead}>
            </webcomics-strip>`)
          : ''}
      </div>
    `;
  }
}

window.customElements.define('webcomics-comic', Comic);
